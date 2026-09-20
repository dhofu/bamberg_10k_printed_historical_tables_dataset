# Script written with Claude Opus 5
# Per prefix: one tar file (images_<prefix>.tar).
# Per source folder:
# copy PNGs -> staging, optimise with oxipng,
# append to that prefix's .tar, clear staging, log as done.
#
# Disk use stays at roughly one volume's worth, and the run is resumable:
# folders listed in $doneLog are skipped, so just re-run after an interrupt.

# --- settings --------------------------------------------------------------
$src      = 'add_source_folder_here'

# One tar per entry. '*' on its own would mean "everything" -> images_all.tar
$prefixes = @(
    'bsb1021*'
    'bsb1022*'
    'bsb1029*'
    'bsb1031*'
    'bsb1034*'
    'bsb1035*'
    'bsb1038*'
    'bsb1061*'
    'bsb1062*'
    'bsb1068*'
    'bsb107*'
    'bsb109*'
    'bsb110*'
    'bsb111*'
    'bsb113*'
    'bsb114*'
    'bsb1150*'
    'bsb1151*'
    'bsb1157*'
    'bsb11508*'
)

$staging  = 'path_to_folder\_staging'                          # scratch, emptied as we go
$outDir   = 'path_to_folder'            # the tars are written here
$doneLog  = 'path_to_folder\_done.txt'                         # resume record (shared by all prefixes)
$csvLog   = 'path_to_folder\flattening_compression_log.csv'    # per-folder processing record
$csvDelim = ';'

$oxipng   = 'oxipng'                       # or full path to oxipng.exe
$oxiArgs  = @('-r', '-o', '4', '--strip', 'safe', '-q')
$optimise = $true                          # $false to skip oxipng

$ErrorActionPreference = 'Stop'

# --- tar name per prefix ---------------------------------------------------
# 'bsb102*' -> path_to_folder\images_bsb102.tar ; '*' -> path_to_folder\images_all.tar
function Get-TarPath {
    param([Parameter(Mandatory)][string]$Prefix)

    $tag = $Prefix -replace '[\*\?]', '' -replace '[^\w\.\-]', '_'
    if ([string]::IsNullOrWhiteSpace($tag)) { $tag = 'all' }
    Join-Path $outDir "images_$tag.tar"
}

# --- preflight -------------------------------------------------------------
if ($prefixes.Count -eq 0) { throw 'No prefixes configured.' }

foreach ($t in @($doneLog, $csvLog)) {
    New-Item -ItemType Directory (Split-Path $t) -Force | Out-Null
}
New-Item -ItemType Directory $outDir  -Force | Out-Null
New-Item -ItemType Directory $staging -Force | Out-Null

$tarExe = "$env:SystemRoot\System32\tar.exe"
if (-not (Test-Path $tarExe)) { throw "tar.exe not found at $tarExe" }

if ($optimise -and -not (Get-Command $oxipng -ErrorAction SilentlyContinue)) {
    throw "oxipng not found. Install it, reopen PowerShell, or set `$oxipng to the full path."
}

if (-not (Test-Path -LiteralPath $src)) { throw "Source not reachable: $src" }

$done = if (Test-Path $doneLog) { @(Get-Content $doneLog) } else { @() }
Write-Host "$($prefixes.Count) prefix(es) to process. $($done.Count) folder(s) already done."

# csv logging (optional)
# Numbers are written with an invariant decimal point so the file parses the
# same everywhere, regardless of the machine's locale.
function Add-LogRow {
    param([string]$Folder, [int]$Count, [long]$Before, [long]$After, [string]$Tar)

    $inv = [cultureinfo]::InvariantCulture
    $pct = if ($Before -gt 0) { (1 - $After / $Before) * 100 } else { 0 }

    [pscustomobject][ordered]@{
        timestamp    = (Get-Date).ToString('s')
        folder       = $Folder
        tar          = Split-Path $Tar -Leaf
        png_count    = $Count
        bytes_before = $Before
        bytes_after  = $After
        mb_before    = [string]::Format($inv, '{0:F2}', $Before / 1MB)
        mb_after     = [string]::Format($inv, '{0:F2}', $After / 1MB)
        saved_pct    = [string]::Format($inv, '{0:F2}', $pct)
        optimised    = $optimise
    } | Export-Csv -LiteralPath $csvLog -Delimiter $csvDelim -NoTypeInformation -Append -Encoding utf8
}

# --- main loop -------------------------------------------------------------
$grandFolders = 0; $grandFiles = 0; $grandIn = 0L; $grandOut = 0L
$tarsTouched  = [System.Collections.Generic.List[string]]::new()
$p = 0

foreach ($prefix in $prefixes) {
    $p++
    $tar = Get-TarPath $prefix

    Write-Progress -Id 1 -Activity 'prefixes' `
                   -Status "$p/$($prefixes.Count)  $prefix -> $(Split-Path $tar -Leaf)" `
                   -PercentComplete (($p - 1) / $prefixes.Count * 100)

    $all = @(Get-ChildItem -LiteralPath $src -Directory -Filter $prefix |
             Where-Object { $_.Name -notin $done })

    if ($all.Count -eq 0) {
        Write-Warning "$prefix : nothing to do (no match in $src, or all already done)."
        continue
    }

    ""
    "=== $prefix  ->  $(Split-Path $tar -Leaf)   ($($all.Count) folder(s))"

    $i = 0; $files = 0; $bytesIn = 0L; $bytesOut = 0L

    foreach ($d in $all) {
        $i++
        Write-Progress -Id 2 -ParentId 1 -Activity 'flatten + optimise + tar' `
                       -Status "$i/$($all.Count)  $($d.Name)" `
                       -PercentComplete ($i / $all.Count * 100)

        # empty staging (leftovers from an interrupted run are re-made below)
        Get-ChildItem -LiteralPath $staging -File | Remove-Item -Force

        # 1. copy this volume's PNGs in flat
        $png = @(Get-ChildItem -File -LiteralPath $d.FullName -Recurse -Filter *.png)
        if ($png.Count -eq 0) {
            Write-Warning "$($d.Name): no PNGs, skipping."
            Add-LogRow -Folder $d.Name -Count 0 -Before 0 -After 0 -Tar $tar
            Add-Content $doneLog $d.Name
            $done += $d.Name
            continue
        }
        $png | Copy-Item -Destination $staging
        $before = (Get-ChildItem -LiteralPath $staging -File | Measure-Object Length -Sum).Sum

        # 2. optimise in place
        if ($optimise) {
            & $oxipng @oxiArgs $staging
            if ($LASTEXITCODE -ne 0) { throw "$($d.Name): oxipng exited $LASTEXITCODE" }
        }
        $after = (Get-ChildItem -LiteralPath $staging -File | Measure-Object Length -Sum).Sum

        # 3. append to this prefix's tar via a file list (bare names, no cmdline limit)
        $list = Join-Path $env:TEMP 'tar_list.txt'
        (Get-ChildItem -LiteralPath $staging -File).Name | Set-Content $list -Encoding ascii
        & $tarExe -rf $tar -C $staging -T $list
        if ($LASTEXITCODE -ne 0) { throw "$($d.Name): tar exited $LASTEXITCODE" }
        Remove-Item $list -Force

        # 4. record success, free the space
        Add-LogRow -Folder $d.Name -Count $png.Count -Before $before -After $after -Tar $tar
        Add-Content $doneLog $d.Name
        $done += $d.Name
        Get-ChildItem -LiteralPath $staging -File | Remove-Item -Force

        $files    += $png.Count
        $bytesIn  += $before
        $bytesOut += $after

        Write-Host ("  {0,-16} {1,5} png  {2,7:N1} -> {3,7:N1} MB" -f `
            $d.Name, $png.Count, ($before / 1MB), ($after / 1MB))
    }

    Write-Progress -Id 2 -Activity 'flatten + optimise + tar' -Completed

    # --- per-prefix summary ------------------------------------------------
    $tarSize = if (Test-Path -LiteralPath $tar) { (Get-Item -LiteralPath $tar).Length } else { 0 }
    ("  -- {0}: {1} folder(s), {2} file(s), {3:N2} -> {4:N2} GB, tar now {5:N2} GB" -f `
        (Split-Path $tar -Leaf), $all.Count, $files, ($bytesIn / 1GB), ($bytesOut / 1GB), ($tarSize / 1GB))

    if (-not $tarsTouched.Contains($tar)) { $tarsTouched.Add($tar) }
    $grandFolders += $all.Count
    $grandFiles   += $files
    $grandIn      += $bytesIn
    $grandOut     += $bytesOut
}

Write-Progress -Id 1 -Activity 'prefixes' -Completed

# --- summary ---------------------------------------------------------------
$saved = if ($grandIn) { (1 - $grandOut / $grandIn) * 100 } else { 0 }
""
"prefixes         : $($prefixes.Count)"
"folders this run : $grandFolders"
"files added      : $grandFiles"
("bytes in         : {0:N2} GB" -f ($grandIn / 1GB))
("bytes out        : {0:N2} GB" -f ($grandOut / 1GB))
("oxipng saving    : {0:N1} %" -f $saved)
""
"tars written:"
foreach ($t in $tarsTouched) {
    ("  {0,-28} {1,8:N2} GB" -f (Split-Path $t -Leaf), ((Get-Item -LiteralPath $t).Length / 1GB))
}
""
"processing log   : $csvLog"
"verify with:"
foreach ($t in $tarsTouched) {
    "  & `"$tarExe`" -tf `"$t`" | Measure-Object -Line"
}