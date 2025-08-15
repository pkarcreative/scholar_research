# Semantic Scholar Research

This repository contains tools and data for researching academic papers using the Semantic Scholar API.

## Contents

- **`data_access.py`** - Python script to retrieve papers from Semantic Scholar API
- **`papers.json`** - Dataset of papers retrieved using the search query "generative ai"

## Features

- Bulk paper retrieval from Semantic Scholar
- Configurable search parameters (query, year range, fields)
- Automatic pagination handling for large result sets
- JSON output format for easy data processing

## Usage

The `data_access.py` script is configured to search for papers containing "generative ai" published from 2023 onwards. It retrieves the following fields for each paper:

- Title
- URL
- Publication types
- Publication date
- Open access PDF availability
- Year
- Fields of study

## Requirements

- Python 3.x
- `requests` library

## Installation

```bash
pip install requests
```

## Running the Script

```bash
python data_access.py
```

The script will automatically retrieve all available papers matching the search criteria and save them to `papers.json`.

## Data Format

Each paper in the JSON file contains structured data from the Semantic Scholar API, making it easy to analyze trends in generative AI research.
