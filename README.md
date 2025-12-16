# Zotero Tag Exporter

Exports annotations in the format `<text> (<authors>, <date>, <page>) <tags>)`.

## Geting started

Install:

- git
- python

Clone the repository:

```bash
git clone https://github.com/this-oliver/zotero-tag-exporter.git
cd zotero-tag-exporter
```

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Create a .env file with your API Key and User ID. See the [.env.example](.env.example) for a reference.

## Usage

To fetch annotations based on a tag, you will need to run:

```bash
python main.py "<tag>"

# For example, to get all annotations tagged with "rooney", run:
python main.py "rooney"

# For annotations with the tag "rooney is the best"
python main.py "rooney is the best"
```
