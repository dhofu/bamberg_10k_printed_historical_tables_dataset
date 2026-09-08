# ---------------------------------------------------------------------------
# flatten_optimize_tar.ps1

# Script written with Claude Opus 5
# Per source folder: 
# copy PNGs -> staging, optimise with oxipng,
# append to a growing .tar, clear staging, log as done.
#
# Disk use stays at roughly one volume's worth, and the run is resumable:
# folders listed in $doneLog are skipped, so just re-run after an interrupt.

# --- settings --------------------------------------------------------------
$src      = '\\uni-bamberg\team\table-recognition-2.digihist'
$prefix   = 'bsb115*'                            # use prefix to restrict number of folders to process, '*' for all
$staging  = 'C:\10k\_staging'                     # scratch, emptied as we go
$tar      = 'C:\10k\images_part3.tar'                   # grows across runs
$doneLog  = 'C:\10k\_done.txt'                    # resume record
$csvLog   = 'C:\10k\flattening_compression_log.csv'    # per-folder processing record
$csvDelim = ';'

$oxipng   = 'oxipng'                       # or full path to oxipng.exe
$oxiArgs  = @('-r', '-o', '4', '--strip', 'safe', '-q')
$optimise = $true                          # $false to skip oxipng
# ---------------------------------------------------------------------------

$ErrorActionPreference = 'Stop'

# --- preflight -------------------------------------------------------------
foreach ($t in @($tar, $doneLog, $csvLog)) {
    New-Item -ItemType Directory (Split-Path $t) -Force | Out-Null
}
New-Item -ItemType Directory $staging -Force | Out-Null

$tarExe = "$env:SystemRoot\System32\tar.exe"
if (-not (Test-Path $tarExe)) { throw "tar.exe not found at $tarExe" }

if ($optimise -and -not (Get-Command $oxipng -ErrorAction SilentlyContinue)) {
    throw "oxipng not found. Install it, reopen PowerShell, or set `$oxipng to the full path."
}

if (-not (Test-Path -LiteralPath $src)) { throw "Source not reachable: $src" }

$done = if (Test-Path $doneLog) { @(Get-Content $doneLog) } else { @() }

$all = @(Get-ChildItem -LiteralPath $src -Directory -Filter $prefix |
         Where-Object { $_.Name -notin $done })

if ($all.Count -eq 0) {
    Write-Warning "Nothing to do: no folders match '$prefix' in $src, or all are already done."
    return
}
Write-Host "$($all.Count) folder(s) to process. $($done.Count) already done."

# --- csv logging -----------------------------------------------------------
# Numbers are written with an invariant decimal point so the file parses the
# same everywhere, regardless of the machine's locale.
function Add-LogRow {
    param([string]$Folder, [int]$Count, [long]$Before, [long]$After)

    $inv = [cultureinfo]::InvariantCulture
    $pct = if ($Before -gt 0) { (1 - $After / $Before) * 100 } else { 0 }

    [pscustomobject][ordered]@{
        timestamp    = (Get-Date).ToString('s')
        folder       = $Folder
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
$i = 0; $files = 0; $bytesIn = 0L; $bytesOut = 0L

foreach ($d in $all) {
    $i++
    Write-Progress -Activity 'flatten + optimise + tar' `
                   -Status "$i/$($all.Count)  $($d.Name)" `
                   -PercentComplete ($i / $all.Count * 100)

    # empty staging (leftovers from an interrupted run are re-made below)
    Get-ChildItem -LiteralPath $staging -File | Remove-Item -Force

    # 1. copy this volume's PNGs in flat
    $png = @(Get-ChildItem -File -LiteralPath $d.FullName -Recurse -Filter *.png)
    if ($png.Count -eq 0) {
        Write-Warning "$($d.Name): no PNGs, skipping."
        Add-LogRow -Folder $d.Name -Count 0 -Before 0 -After 0
        Add-Content $doneLog $d.Name
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

    # 3. append to the tar via a file list (keeps names bare, no cmdline limit)
    $list = Join-Path $env:TEMP 'tar_list.txt'
    (Get-ChildItem -LiteralPath $staging -File).Name | Set-Content $list -Encoding ascii
    & $tarExe -rf $tar -C $staging -T $list
    if ($LASTEXITCODE -ne 0) { throw "$($d.Name): tar exited $LASTEXITCODE" }
    Remove-Item $list -Force

    # 4. record success, free the space
    Add-LogRow -Folder $d.Name -Count $png.Count -Before $before -After $after
    Add-Content $doneLog $d.Name
    Get-ChildItem -LiteralPath $staging -File | Remove-Item -Force

    $files    += $png.Count
    $bytesIn  += $before
    $bytesOut += $after

    Write-Host ("  {0,-16} {1,5} png  {2,7:N1} -> {3,7:N1} MB" -f `
        $d.Name, $png.Count, ($before / 1MB), ($after / 1MB))
}

Write-Progress -Activity 'flatten + optimise + tar' -Completed

# --- summary ---------------------------------------------------------------
$saved = if ($bytesIn) { (1 - $bytesOut / $bytesIn) * 100 } else { 0 }
""
"folders this run : $($all.Count)"
"files added      : $files"
("bytes in         : {0:N2} GB" -f ($bytesIn / 1GB))
("bytes out        : {0:N2} GB" -f ($bytesOut / 1GB))
("oxipng saving    : {0:N1} %" -f $saved)
("tar size         : {0:N2} GB" -f ((Get-Item $tar).Length / 1GB))
""
"processing log   : $csvLog"
"verify with:  & `"$tarExe`" -tf `"$tar`" | Measure-Object -Line"
