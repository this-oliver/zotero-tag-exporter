# Zotero Tag Exporter

> [![CI](https://github.com/this-oliver/zotero-tag-exporter/actions/workflows/ci.yaml/badge.svg)](https://github.com/this-oliver/zotero-tag-exporter/actions/workflows/ci.yaml) [![CD](https://github.com/this-oliver/zotero-tag-exporter/actions/workflows/cd.yaml/badge.svg)](https://github.com/this-oliver/zotero-tag-exporter/actions/workflows/cd.yaml)

Exports annotations from Zotero based on your tags.

## Geting started

pre-requisites:

- git
- python

Clone the repository:

```bash
git clone https://github.com/this-oliver/zotero-tag-exporter.git
cd zotero-tag-exporter
```

Setup virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Create a .env file with your API Key and User ID. See the [.env.example](.env.example) for a reference.

## Usage

To fetch annotations based on a tag, you will need to run:

```bash
python main.py -t "<tag>"

# example: get all annotations tagged with "abc"
python main.py -t "abc"

# example: get all annotations tagged with "abc" and "zyx"
python main.py -t "abc" -t "zyx"
```
