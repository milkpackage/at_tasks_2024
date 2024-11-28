# Framework Setup and Testing Guide

## Installation

To install the framework packages navigate to the framework folder and run:
```bash
pip install -e .
```

## Browser Selection

You can choose which browser to use for testing by adding parameters:

For Firefox:
```bash
--browser firefox
```

For Chrome:
```bash
--browser chrome
```

## Running Tests

To launch tests, use pytest in your terminal in root folder:
```bash
pytest
```

To specifically run tests in Firefox:
```bash
pytest --browser firefox
```