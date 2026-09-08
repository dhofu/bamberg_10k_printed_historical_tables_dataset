# Datasheet for the Bamberg 10k Printed Historical Tables Dataset

## Description
The Bamberg 10k Printed Historical Tables Dataset is intended to advance work on table recognition, specifically for historical tables that are diverse, irregular and complex while forming one of the cornerstones of historical research per se.

In 2025 researchers from the University of Bamberg received a grant from the so-called so-called [Incubator Funds of the NFDI4memory consortium](https://4memory.de/aktivitaeten/incubator-funds/) to construct a 'benchmark dataset' of historical tables in the field of social and economic history. [Initial results of the project](https://doi.org/10.5281/zenodo.17249977) were presented during a poster session at the [NFDI Community Forum](https://4memory.de/aktivitaeten/community-forum/community-forum-2025/) during the Historikertag in Bonn in September 2025.

While the project is still very much 'under development', it is hoped that the dataset will make a significant contribution to the creation of a (large) ground truth dataset for table recognition. 

The current dataset contains 10,635 images of full-page tables derived from 234 books published between 1755 and 1899 and part of the [digital collections of the Bavarian State Libary](https://www.digitale-sammlungen.de). A ML-classification tool was developed to locate these images. Some misclassifications are unavoidable. The tables are provided in PNG format.

The dataset consists of a single tar.gz-file, metadata files, and processing documentation.

### Publisher

**Digital History at the Otto-Friedrich Universität Bamberg** See: [website](https://www.uni-bamberg.de/digihist/)

### Dataset curators

- **[Werner Scheltjens](https://github.com/dhofu)** (Person)
  - **Affiliation:**: Otto-Friedrich-Universität Bamberg
  - **Identifiers:**: [0000-0002-5209-9052](https://orcid.org/0000-0002-5209-9052) (ORCID)
  - **Contact:** [digihist@uni-bamberg.de](mailto:digihist@uni-bamberg.de)
  - Werner Scheltjens is professor of digital history at the University of Bamberg. He was responsible for source retrieval, metadata data harvesting, image harvesting, ML-model training, publication of the data and drafting of the datasheet. 

- **[Sebastian Geschonke](https://github.com/Sebaristoteles)** (Person)
  - **Affiliation:**: Humboldt Universität zu Berlin
  - **Identifiers:**: [0009-0009-5264-7600](https://orcid.org/0009-0009-5264-7600) (ORCID)
  - **Contact:** [sebastian.geschonke@gmail.com](mailto:sebastian.geschonke@gmail.com)
  - [Sebastian Geschonke](https://sebastiangeschonke.com/) is Doctoral Candidate at Berlin School of Economics. He was responsible for reviewing the scripts and data and drafting of the datasheet. 

### Point of contact

- **Werner Scheltjens** (Person)
  - **Affiliation:**: Otto-Friedrich-Universität Bamberg
  - **Identifiers:**: [0000-0002-5209-9052](https://orcid.org/0000-0002-5209-9052) (ORCID)
  - **Contact:** [digihist@uni-bamberg.de](mailto:digihist@uni-bamberg.de)

### Paper or other reference
Scheltjens, W. (2025). Aufbau und Bereitstellung eines Benchmark Datensatzes für Historische Tabellen, 1750-1990 [Graphic]. Zenodo. NFDI4Memory Community Forum, Bonn. URL: https://doi.org/10.5281/zenodo.17249977

### Supported tasks or shared tasks

This dataset was not part of a shared task.

#### AI categories

- [image segmentation](https://huggingface.co/tasks/image-segmentation)
- [image feature extraction](https://ai4culture.eu/resources?page=0&aiCategories=IMAGE_FEATURE_EXTRACTION)

#### Types of cultural heritage applications

- [digitisation](https://sidedoc.app/vocabs/ai4culture-application-type/digitisation)
- [computer vision](https://ai4culture.eu/resources?page=0&aiCategories=COMPUTER_VISION)

#### Cultural heritage application example

- table recognition

## Distribution

This dataset is distributed by the named dataset curators. 

### Data access URL

[https://doi.org/10.5281/zenodo.22251282](https://doi.org/10.5281/zenodo.22251282)

### License

[Creative Commons Attribution 4.0 International CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

### File format

[image/png](https://www.iana.org/assignments/media-types/image/png)

### Citation information

```
@dataset{scheltjens_2026_22251282,
  author       = {Scheltjens, Werner and
                  Geschonke, Sebastian},
  title        = {Bamberg 10k Printed Historical Tables Dataset},
  month        = sep,
  year         = 2026,
  publisher    = {Digital History at the Otto-Friedrich Universität Bamberg},
  version      = 1,
  doi          = {10.5281/zenodo.22251282},
  url          = {https://doi.org/10.5281/zenodo.22251282},
}
```

## Composition

### Dataset category

- [content](https://sidedoc.app/vocabs/dataset-category/content)

### Media category

- [image](https://sidedoc.app/vocabs/edm-media-type/image)

### Object types

- [computer dataset](http://rdaregistry.info/termList/RDAContentType/1007)
- [monographs](http://vocab.getty.edu/page/aat/300060417)
- [periodicals](http://vocab.getty.edu/page/aat/300026657)

### Dataset structure

During the image harvesting process, each book was stored as a separate folder named after the book's bsb-identifier. The dataset published on Zenodo contains all 10,635 PNG images from these 234 folders in a lossless and format preserving compression, merged into three flattened TAR-files: `images_part1.tar`, `images_part2.tar` and `images_part3.tar`. The accompanying harvesting manifest and classification log files per book are stored in 2 additional TAR-files, `manifest.tar`and `classification_log.tar`. The harvesting `*_manifest.json` contains details about the source of each image and its license. The `*_classification_log.jsonl` contains page-wise information about its classification by the ML-classification algorithm. 
Image filenames have the following structure: [bsb-identifier]\_[page-number]\_conf\_[confidence-rate].png

#### Languages

| language | # of works |
|----------|------------|
| [Bulgarian](http://id.loc.gov/vocabulary/iso639-2/bul) | 1 |
| [English](http://id.loc.gov/vocabulary/iso639-2/eng) | 5 |
| [French](http://id.loc.gov/vocabulary/iso639-2/fra) | 27 |
| [German](http://id.loc.gov/vocabulary/iso639-2/deu) | 124 |
| [German](http://id.loc.gov/vocabulary/iso639-2/deu) & [French](http://id.loc.gov/vocabulary/iso639-2/fra) | 2 |
| [German](http://id.loc.gov/vocabulary/iso639-2/deu) & [Latin](http://id.loc.gov/vocabulary/iso639-2/lat) | 1 |
| [Greek](http://id.loc.gov/vocabulary/iso639-2/gre) | 1 |
| [Italian](http://id.loc.gov/vocabulary/iso639-2/ita) | 35 |
| [Latin](http://id.loc.gov/vocabulary/iso639-2/lat) | 3 |
| [Russian](http://id.loc.gov/vocabulary/iso639-2/rus) | 1 |
| [Undetermined](http://id.loc.gov/vocabulary/iso639-2/und) | 34 |

#### Descriptive statistics

The dataset amounts to ca 50 GB in compressed form (tar.gz-file). The number of images amounts up to 10,635. 

## Data collection process

### Curation rationale

See [README.md](README.md)

### Source data

#### Initial data collection

See [README.md](README.md)

#### Digitisation pipeline

See [README.md](README.md)

#### Source data producer

Source data were produced by the Bavarian State Library. All scans in the dataset are part of their digital collections. 

### Preprocessing and cleaning

See [README.md](README.md)

### Version information

This is the first version of the dataset.

#### Release date

#### Date

2026-09-09

#### Checksums

- [MD5:](https://www.iana.org/assignments/hash-alg-registry/md5) d62f993850f50fd316e7a6823f32dc89
- [SHA256:](https://www.iana.org/assignments/hash-alg-registry/sha256) 1b547c9d8afc99485f090b97b323ea38d95e3b1b0460f0e42840308a818a7d2c

### Maintenance plan

#### Maintenance level

[Limited Maintenance](https://sidedoc.app/vocabs/maintenance-level/limited-maintenance)

#### Update periodicity

[Unknown](http://publications.europa.eu/resource/authority/frequency/UNKNOWN)

## Examples and considerations for using the data

The dataset is suitable to serve as a foundation for historical table recognition.

### Ethical considerations

#### Personal or other sensitive information

The dataset does not contain personal or sensitive information.

#### Potential societal impact of using the dataset

This dataset uses historical printed titles that have been published before the 20th century. 
The societal impact of the dataset is therefore negligible.

### Example of dataset reuse

So far, this dataset has not yet been reused.

### Unanticipated uses

There are no known unanticipated uses made of this dataset. Users are invited to report the uses they made of this dataset back to the curators, which would enable an update of this datasheet.

This datasheet was created following the example set by the 'sister' [Historical Tables Dataset](https://github.com/StabiBerlin/TabellarischeQuellen) from the Berlin State Library. 
