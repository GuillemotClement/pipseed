# pipseed

CLI tool for generating fake data to quickly populate test datasets.

## Features

- Generate various types of fake data (persons, addresses, companies, products, transactions, users)
- Multiple output formats: JSON, CSV, SQL INSERT statements
- Support for multiple locales (en_US, fr_FR, es_ES, etc.)
- Configurable number of records
- Pretty-print JSON output
- Save to file or output to stdout

## Installation

### From source

```bash
pip install -e .
```

### Using pip (once published)

```bash
pip install pipseed
```

## Usage

### Basic usage

Generate 10 persons in JSON format:
```bash
pipseed person
```

Generate 5 persons in CSV format:
```bash
pipseed person -n 5 -f csv
```

Generate 3 companies as SQL INSERT statements:
```bash
pipseed company -n 3 -f sql -t companies
```

Generate 20 products with French locale:
```bash
pipseed product -n 20 -l fr_FR
```

Pretty-print JSON output:
```bash
pipseed person -n 5 -p
```

Save output to a file:
```bash
pipseed person -n 100 -f csv -o data.csv
```

### Available data types

- **person**: Generate person data (name, email, phone, address)
- **address**: Generate address data (street, city, country, coordinates)
- **company**: Generate company data (name, email, website, industry)
- **product**: Generate product data (name, description, price, SKU)
- **transaction**: Generate transaction data (amount, currency, date, status)
- **user**: Generate user data (username, email, password hash)

### Command-line options

```
positional arguments:
  {person,address,company,product,transaction,user}
                        Type of data to generate

options:
  -h, --help            Show help message
  -n COUNT, --count COUNT
                        Number of records to generate (default: 10)
  -f {json,csv,sql}, --format {json,csv,sql}
                        Output format (default: json)
  -p, --pretty          Pretty print JSON output (only for JSON format)
  -t TABLE, --table TABLE
                        Table name for SQL output (default: data)
  -l LOCALE, --locale LOCALE
                        Locale for data generation (default: en_US)
  -o OUTPUT, --output OUTPUT
                        Output file path (default: stdout)
```

## Examples

### Generate test users for a database

```bash
pipseed user -n 50 -f sql -t users -o users.sql
```

### Generate CSV data for import

```bash
pipseed person -n 1000 -f csv -o persons.csv
```

### Generate French company data

```bash
pipseed company -n 10 -l fr_FR -p
```

## Requirements

- Python >= 3.8
- faker >= 20.0.0

## License

MIT
