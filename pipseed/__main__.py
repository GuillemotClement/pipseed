"""
Main CLI module for pipseed
"""

import argparse
import sys
import json
import csv
from io import StringIO
from faker import Faker


def generate_fake_data(data_type, count, locale='en_US'):
    """
    Generate fake data based on the specified type
    
    Args:
        data_type: Type of data to generate (person, address, company, etc.)
        count: Number of records to generate
        locale: Locale for fake data generation
    
    Returns:
        List of dictionaries containing generated data
    """
    fake = Faker(locale)
    data = []
    
    if data_type == 'person':
        for _ in range(count):
            data.append({
                'id': fake.uuid4(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'date_of_birth': fake.date_of_birth().isoformat(),
                'address': fake.address().replace('\n', ', ')
            })
    
    elif data_type == 'address':
        for _ in range(count):
            data.append({
                'id': fake.uuid4(),
                'street': fake.street_address(),
                'city': fake.city(),
                'state': fake.state(),
                'country': fake.country(),
                'postal_code': fake.postcode(),
                'latitude': str(fake.latitude()),
                'longitude': str(fake.longitude())
            })
    
    elif data_type == 'company':
        for _ in range(count):
            data.append({
                'id': fake.uuid4(),
                'name': fake.company(),
                'email': fake.company_email(),
                'phone': fake.phone_number(),
                'website': fake.url(),
                'industry': fake.bs(),
                'address': fake.address().replace('\n', ', ')
            })
    
    elif data_type == 'product':
        for _ in range(count):
            data.append({
                'id': fake.uuid4(),
                'name': fake.catch_phrase(),
                'description': fake.text(max_nb_chars=200),
                'price': round(fake.random.uniform(1.0, 1000.0), 2),
                'sku': fake.bothify(text='???-########'),
                'barcode': fake.ean13(),
                'category': fake.word()
            })
    
    elif data_type == 'transaction':
        for _ in range(count):
            data.append({
                'id': fake.uuid4(),
                'transaction_id': fake.uuid4(),
                'amount': round(fake.random.uniform(1.0, 10000.0), 2),
                'currency': fake.currency_code(),
                'date': fake.date_time_this_year().isoformat(),
                'status': fake.random.choice(['pending', 'completed', 'failed', 'refunded']),
                'description': fake.sentence()
            })
    
    elif data_type == 'user':
        for _ in range(count):
            data.append({
                'id': fake.uuid4(),
                'username': fake.user_name(),
                'email': fake.email(),
                'password_hash': fake.sha256(),
                'created_at': fake.date_time_this_decade().isoformat(),
                'last_login': fake.date_time_this_year().isoformat(),
                'is_active': fake.boolean()
            })
    
    else:
        raise ValueError(f"Unknown data type: {data_type}. Available types: person, address, company, product, transaction, user")
    
    return data


def format_as_json(data, pretty=False):
    """Format data as JSON"""
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def format_as_csv(data):
    """Format data as CSV"""
    if not data:
        return ""
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def format_as_sql(data, table_name):
    """Format data as SQL INSERT statements"""
    if not data:
        return ""
    
    statements = []
    fields = list(data[0].keys())
    
    for row in data:
        values = []
        for field in fields:
            value = row[field]
            if isinstance(value, str):
                # Escape single quotes in strings
                value = value.replace("'", "''")
                values.append(f"'{value}'")
            elif isinstance(value, bool):
                values.append('TRUE' if value else 'FALSE')
            elif value is None:
                values.append('NULL')
            else:
                values.append(str(value))
        
        statement = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(values)});"
        statements.append(statement)
    
    return '\n'.join(statements)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='pipseed',
        description='Generate fake data for testing purposes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pipseed person -n 10                    # Generate 10 persons in JSON format
  pipseed person -n 5 -f csv              # Generate 5 persons in CSV format
  pipseed company -n 3 -f sql -t companies # Generate 3 companies as SQL inserts
  pipseed product -n 20 -l fr_FR          # Generate 20 products with French locale
  
Available data types:
  person      - Generate person data (name, email, phone, address)
  address     - Generate address data (street, city, country, coordinates)
  company     - Generate company data (name, email, website, industry)
  product     - Generate product data (name, description, price, SKU)
  transaction - Generate transaction data (amount, currency, date, status)
  user        - Generate user data (username, email, password hash)
        """
    )
    
    parser.add_argument(
        'data_type',
        choices=['person', 'address', 'company', 'product', 'transaction', 'user'],
        help='Type of data to generate'
    )
    
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=10,
        help='Number of records to generate (default: 10)'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'csv', 'sql'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '-p', '--pretty',
        action='store_true',
        help='Pretty print JSON output (only for JSON format)'
    )
    
    parser.add_argument(
        '-t', '--table',
        type=str,
        default='data',
        help='Table name for SQL output (default: data)'
    )
    
    parser.add_argument(
        '-l', '--locale',
        type=str,
        default='en_US',
        help='Locale for data generation (default: en_US, e.g., fr_FR, es_ES)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default: stdout)'
    )
    
    args = parser.parse_args()
    
    try:
        # Generate data
        data = generate_fake_data(args.data_type, args.count, args.locale)
        
        # Format data
        if args.format == 'json':
            output = format_as_json(data, args.pretty)
        elif args.format == 'csv':
            output = format_as_csv(data)
        elif args.format == 'sql':
            output = format_as_sql(data, args.table)
        
        # Output data
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Data written to {args.output}", file=sys.stderr)
        else:
            print(output)
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
