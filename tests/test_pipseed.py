"""
Tests for pipseed CLI tool
"""

import json
import pytest
from pipseed.__main__ import generate_fake_data, format_as_json, format_as_csv, format_as_sql


def test_generate_person_data():
    """Test generating person data"""
    data = generate_fake_data('person', 5)
    assert len(data) == 5
    assert all('first_name' in record for record in data)
    assert all('last_name' in record for record in data)
    assert all('email' in record for record in data)
    assert all('phone' in record for record in data)
    assert all('date_of_birth' in record for record in data)
    assert all('address' in record for record in data)


def test_generate_address_data():
    """Test generating address data"""
    data = generate_fake_data('address', 3)
    assert len(data) == 3
    assert all('street' in record for record in data)
    assert all('city' in record for record in data)
    assert all('country' in record for record in data)


def test_generate_company_data():
    """Test generating company data"""
    data = generate_fake_data('company', 2)
    assert len(data) == 2
    assert all('name' in record for record in data)
    assert all('email' in record for record in data)
    assert all('website' in record for record in data)


def test_generate_product_data():
    """Test generating product data"""
    data = generate_fake_data('product', 3)
    assert len(data) == 3
    assert all('name' in record for record in data)
    assert all('price' in record for record in data)
    assert all('sku' in record for record in data)


def test_generate_transaction_data():
    """Test generating transaction data"""
    data = generate_fake_data('transaction', 2)
    assert len(data) == 2
    assert all('amount' in record for record in data)
    assert all('currency' in record for record in data)
    assert all('status' in record for record in data)


def test_generate_user_data():
    """Test generating user data"""
    data = generate_fake_data('user', 3)
    assert len(data) == 3
    assert all('username' in record for record in data)
    assert all('email' in record for record in data)
    assert all('password_hash' in record for record in data)


def test_format_as_json():
    """Test JSON formatting"""
    data = [{'name': 'Test', 'value': 123}]
    result = format_as_json(data)
    assert json.loads(result) == data
    
    # Test pretty printing
    result_pretty = format_as_json(data, pretty=True)
    assert json.loads(result_pretty) == data
    assert '\n' in result_pretty


def test_format_as_csv():
    """Test CSV formatting"""
    data = [
        {'name': 'Test1', 'value': 123},
        {'name': 'Test2', 'value': 456}
    ]
    result = format_as_csv(data)
    lines = result.strip().split('\n')
    assert len(lines) == 3  # header + 2 records
    assert 'name,value' in lines[0]


def test_format_as_sql():
    """Test SQL formatting"""
    data = [{'name': 'Test', 'value': 123}]
    result = format_as_sql(data, 'test_table')
    assert 'INSERT INTO test_table' in result
    assert 'name' in result
    assert 'value' in result


def test_invalid_data_type():
    """Test error handling for invalid data type"""
    with pytest.raises(ValueError):
        generate_fake_data('invalid_type', 1)


def test_locale_support():
    """Test locale support"""
    data_us = generate_fake_data('person', 1, locale='en_US')
    data_fr = generate_fake_data('person', 1, locale='fr_FR')
    
    assert len(data_us) == 1
    assert len(data_fr) == 1
    # Both should have the same structure
    assert set(data_us[0].keys()) == set(data_fr[0].keys())


def test_empty_data_csv():
    """Test CSV formatting with empty data"""
    result = format_as_csv([])
    assert result == ""


def test_empty_data_sql():
    """Test SQL formatting with empty data"""
    result = format_as_sql([], 'test_table')
    assert result == ""


def test_sql_escaping():
    """Test SQL string escaping"""
    data = [{'name': "O'Brien", 'value': 123}]
    result = format_as_sql(data, 'test_table')
    assert "O''Brien" in result  # Single quotes should be escaped
