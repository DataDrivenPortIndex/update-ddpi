## Overview

The `update-ddpi` application is designed for managing and updating port databases. It merges new (incremental) datasets with existing data, ensuring consistency by retaining existing port IDs. Additionally, the application integrates new polygons into existing ports and adds new ports if they are not already present in the database.

## Features

- **Preservation of Existing Port IDs:** Ensures that existing ports retain their unique IDs for consistency and traceability.
- **Addition of New Polygons:** Merges new polygon data with existing ports when matches are found in the database.
- **Integration of New Ports:** Seamlessly adds ports that are not present in the current database.

---

## Getting Started

### Prerequisites
Ensure that the necessary tools and dependencies are installed.

#### Install the Build System:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
#### Clone the Repository:
```bash
git clone https://github.com/DataDrivenPortIndex/update-ddpi.git
cd update-ddpi
```

## Usage

### Input Data
The application requires two main datasets:
1. **Existing Port Database:** Contains previously recorded ports with IDs, polygons, and metadata.
2. **New Port Data:** An incremental dataset with new/updated port information.


### Commands

#### 1. Running the Application
Execute the `main.py` script:

```bash
uv run  main.py --existing ddpi.geojson --new ddpi_new.geojson --output ddpi.geojson

```

---
