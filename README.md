# Bamberg 10k Printed Historical Tables Dataset

This repository contains the scripts that were used for creating a dataset of ca. 10,000 full-page printed tables in the field of social and economic history, published between 1755 and 1899. The scripts were created in dialogue with Claude Sonnet, Claude Opus 4.7 and 4.8, and Claude Opus 5.
The Bamberg 10k Printed Historical Tables Dataset is accessible on [Zenodo](10.5281/zenodo.22251282). 

## Description of the Dataset
We publish a dataset containing 10,635 full-page printed tables published between 1755 and 1899. The historical tables were collected from 234 scanned books in the realm of social and economic history, which are part of the [digital collections of the Bavarian State Library](https://www.digitale-sammlungen.de). Full bibliographic references for all books in the dataset can be found in [NFDI_234_metadata.json](historical_tables_dataset/NFDI_234_metadata.json). The file is also available as `.csv`-file. 200 out of 234 works (84 %) are from the period 1835-1899; 34 works (16 %) are from the period 1755-1834. 

The uneven distribution of the works in our dataset is in line with our expectations about the period, which is marked by a revolution in printing and drastic increases in the availability and distribution of printed works during the nineteenth century. This increase went hand in hand with a booming interest in capturing data on all aspects of human life. Tabular formats were often the preferred way of publishing these data. 

The dataset contains 8,140 scans that are classified as full-page tables with a 1.0 confidence score. Details about the classification results can be found in NFDI_234_folder_statistics.csv. The classification model is described in the section Processing Documentation.

| total_pngs | conf < 0.80 | conf >= 0.80 | conf >= 0.90 | conf >= 0.95 | conf = 1.00 |
|------------|-------------|--------------|--------------|--------------|-------------|
| 10635 | 785 | 365 | 306 | 1039 | 8140 |

The topics of the tables in the dataset are perhaps best described based on the signatures of their former library shelves. Three topics in the realm of social and economic history are central in the dataset: `cam.`; `merc.` and `num.[ant.|rec.]`. These library signatures (Ger. _Signaturfächer_) are described by [Haller (2011)](www.digitale-sammlungen.de/de/view/bsb00067806) as follows:

- _cam._: Disciplina cameralis (Cameralia); Nationalökonomie, Finanz- und Versicherungswesen, Arbeiterfrage, Geld und Währung, Sozialismus unter wirtschaftlichem Aspekt
- _merc._: Mercatura; Handel, Handels- und Wechselrecht
- _num.ant._: Numismatica antiqua; Alte Münzkunde bis zu Karl dem Großen, Münzgeschichte insgesamt. Münzkataloge
- _num.rec._: Numismatica recens; Neuere Münzkunde, Münzkataloge

These shelves and their topics are represented as follows in the dataset:

    cam.: 61 works
    merc.: 159 works
    num.ant.: 7 works
    num.rec.: 7 works

The dataset contains works in the following languages:

| language | # of works |
|----------|------------|
| bul | 1 |
| eng | 5 |
| fre | 27 |
| ger | 124 |
| ger & fre | 2 |
| ger & lat | 1 |
| gre | 1 |
| ita | 35 |
| lat | 3 |
| rus | 1 |
| und | 34 |

The dataset is the result of a longer process comprising (1) Metadata harvesting of digital collections in the realm of social and economic history between 1750 and 1900, (2) ML-based classification of page-scans for the purpose of identifying full-page historical printed tables; (3) page classification and download of ca. 100,000 page-scans from 1,043 titles; and (4) Criteria-based selection of a subset of ca. 10,000 printed tables. 

Because of its size (54.4 GB), we publish the historical tables dataset on Zenodo. The accompanying materials for understanding and using the dataset, such as background information, scripts and statistics, are published on GitHub. For the sake of clarity, some of the accompanying materials (the readme.md file and the datasheet) are published on both platforms.

Our dataset has the following file structure::

```txt
historical_tables_dataset/
├── NFDI_234_metadata.json
├── NFDI_234_metadata.csv
├── NFDI_234_book_statistics.csv
├── images/ (on Zenodo)
    |   └── images_part1.tar (21.3 GB, 3952 images)
    |   └── images_part2.tar (18.0 GB, 3131 images)
    |   └── images_part3.tar (15.1 GB, 3552 images)
├── manifests/ (64.6 MB, on Zenodo)
    |   └── [bsb-identifier_1]_manifest.json
    |   └── [bsb-identifier_2]_manifest.json
    |   └── [bsb-identifier_n]_manifest.json
├── classification_logs/ (7.20 MB, on Zenodo)
    |   └── [bsb-identifier_1]_classification_log.jsonl
    |   └── [bsb-identifier_1]_classification_log.jsonl
    |...
    ├── └── [bsb-identifier_n]_classification_log.jsonl
├── README.md
├── Datasheet_for_Bamberg_10k_Printed_Historical_Tables_Dataset.md
```

During the image harvesting process, each book was stored as a separate folder named after the book's bsb-identifier. The dataset published on Zenodo contains all 10,635 PNG images from these 234 folders in a lossless and format preserving compression, merged into three flattened TAR-files. The accompanying harvesting manifest and classification log files per book are stored in 2 additional TAR-files. The harvesting `*_manifest.json` contains details about the source of each image and its license. The `*_classification_log.jsonl` contains page-wise information about its classification by the ML-classification algorithm. 

## Processing Documentation

```txt
processing_documentation/
├── legacy_harvesting_script.py
├── oai_harvesting_results.json
├── training_script.py
├── image_harvesting_script.py
├── NFDI_234_bsb_identifiers.txt
├── flatten_optimize_tar.ps1
training_data/
    ├── Table/
    ├── Text/
    ├── Text_and_Table/
    ├── Title/
```

### Metadata harvesting
Metadata harvesting was done for the purpose of obtaining a large pool of potential resources that were likely to contain full-page tables. We used the OAI-PMH endpoint of the BSB Lab in combination with a local instance of MongoDB (Community Edition) for storing the harvesting results. The OAI-PMH endpoint has changed since the data were harvested between 2025.02.23 and 2025.03.15. Therefore, we limit ourselves to documenting the main patterns that were traced in the book titles and book metadata using regexes: `tafeln?`, `tabelle[n|s]??`, `tables?`, `statisti` and `tab[e|u]l{1,2}a` for book title patterns and `Merc\.|Cam\.|Num\.rec\.|Num\.ant\.` for book metadata patterns. Both were searched as one set of patterns, resulting in a broad capturing of book titles that have either 'table' (or a variant) in the raw data of the record or are part of the selected library shelves, or both. 

Harvesting was conducted on the set 'all' (now no longer available) of the BSB digital collections. The process was divided into several steps. One book metadata pattern was selected per run; the year of the last update of the record was used to further divide the process into manageable steps. In the meantime, this OAI-PMH is no longer in use. It has been replaced with a new OAI endpoint and a different configuration of the sets in the digital collections. A [legacy script](processing_documentation/legacy_harvesting_script.py) is published as documentation of the process described here. The results of our metadata harvesting effort are published in [a JSON file](processing_documentation/oai_harvesting_results.json) on Github. 

### Page Classifier for Finding Tables
We trained an ML-algorithm to find tables in large amounts of page-scans of free-of-copyright printed works from the eighteenth and nineteenth centuries. The [training script](processing_documentation/training_script.py) is stored in the folder [processing_documentation](processing_documentation). The [training data](training_data) are stored in a separate folder. The training data consists of 1,384 page-scans belonging to 4 classes ([Title](training_data/Title), [Text](training_data/Text), [Table](training_data/Table), [Text_and_Table](training_data/Text_and_Table)). The classification was done manually. 1,108 files were used for training; 276 for validation during model training. The resulting Keras classification model (> 131 MB) is published on Zenodo. 

### Image Classification and Download
We implemented an [image classification and download script](processing_documentation/image_harvesting_script.py) for processing the records for which metadata were harvested in the previous step. The script examines and classifies each page using the page classifier and downloads only pages that were classified as `Table` or as `Text_and_Table`. The process was carried out until a margin of 100,000 downloaded page scans was reached. This happened after only 1,043 out of 8,985 harvested books were processed, indicating that there are many more tables to be found in the digital collections. For the current stage of this project, the size of 100,000 was deemed sufficient. 

### Selection of a 10k Subset
In the final step, a subset of ca. 10,000 printed tables was created from the 100k collection of harvested images. We selected all 234 works containing 3 to 100 full-page table scans with a 1.0 confidence score. This limit was set to increase the diversity of the dataset. A [list of BSB identifiers](processing_documentation/NFDI_234_bsb_identifiers.txt) for all 234 books in the dataset is provided. It can be used to reproduce the dataset with the [image harvesting script](processing_documentation/image_harvesting_script.py).

### Preparation of Zenodo upload
Images were originally stored in one folder per harvested book during the harvesting process. To facilitate upload to Zenodo, the images were stored in large, flattened TAR-files using a Powershell script that flattens the folders, optimizes file size of the PNGs with `oxipng` and stores the images in a TAR file. The [Powershell script](processing_documentation/flatten_optimize_tar.ps1) is available on GitHub.

## Future Work
Work on the Bamberg 10k Printed Historical Tables Dataset is part of a large initiative that aims to improve historical table recognition. Despite impressive recent advances, stimulated not at the least by rapid increases in the capabilities of LLMs and VLMs, obtaining high quality machine-readable transcriptions of historical tables is still an issue. This is especially true for handwritten tables, but printed historical tables as well continue to present issues due to complex and irregular table structures, bad scan quality, typographical issues etc. 

Since March 2025 we have started building a tool for ground truth production for historical table recognition, which will be released in its pilot version in the coming months. This tool will be indispensible for much-needed ground truth production, which continues to be a precondition of vital importance for structural advances in historical table recognition. 

Alongside tool development, our efforts to expand the Bamberg 10k Printed Historical Tables Dataset are ongoing. The preliminary scripts developed during the 'Incubator' grant period is elaborated further. A general approach to harvesting that goes well beyond the realm of social and economic history is adopted, improving the quality of the page classifier along the way. Our novel general approach and is likely to reveal the existence of many more varieties of printed historical tables and new challenges for historical table recognition. For now, our focus on the digital collections of the Bavarian State Library is maintained. In the longer term, however, possibilities to harvest other significant digital collections should be explored.
