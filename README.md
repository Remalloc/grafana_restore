# Grafana Restore Tool Documentation

[中文文档](README_ZH-cn.md) | [English Doc](README.md)

## Overview

The Grafana Restore Tool is a utility designed to restore Grafana data. This tool uses the built-in Grafana data table `dashboard_version` to restore deleted dashboards. Note: This program can only restore dashboards, and corresponding organizational relationships and other data will still be lost.

## Getting Started

### Prerequisites

Before you begin, ensure that you have the following:

- Python 3.7+ installed on your system.

## Installation

Clone the repository containing the Grafana Restore Tool:
```shell
git clone https://github.com/Remalloc/grafana_restore.git
```

Change to the project directory:
```shell
cd grafana_restore
```

Install the required Python packages:
```shell
pip install -r requirements.txt
```

## Usage

Fill in the Grafana database link in the `main` function. If you are using the default Grafana database (sqlite), you will need to copy the database file to the project directory. The default location of the file is `/var/lib/grafana/grafana.db`.

Create an organization on the Grafana page and fill in the organization ID.

```python
def main():
    restore = Restore(db_url="sqlite:///grafana.db", org_id=8)
    restore.run()
```

Call the `run` method to execute the program:
```python
restore.run()
```

If you are using an sqlite database, after the restoration is complete, you will also need to copy the file back to its original location.

Please note that this is a basic translation and may require adjustments based on actual usage conditions.
