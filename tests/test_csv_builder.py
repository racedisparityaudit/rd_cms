import pytest
import json
from flask import url_for

from application.cms.data_utils import TableObjectDataBuilder, TableObjectBuilder


def test_table_object_data_builder_does_return_object(stub_simple_table_object):
    builder = TableObjectDataBuilder()

    table = builder.process(stub_simple_table_object)

    assert table is not None


def test_table_object_data_builder_does_build_headers_from_simple_table(stub_simple_table_object):
    # given - a
    builder = TableObjectDataBuilder()
    table_object = stub_simple_table_object

    # when we process the object
    table = builder.process(table_object)

    # then the header for the returned table should match the ones from the simple table
    headers = table.pop(0)
    expected_headers = [table_object['category_caption']] + table_object['columns']
    assert headers == expected_headers


def test_table_object_data_builder_does_build_headers_from_legacy_simple_table(stub_simple_table_object):
    # given - a table without a category_caption value
    builder = TableObjectDataBuilder()
    table_object = stub_simple_table_object
    table_object.pop('category_caption', None)

    # when we process the object
    table = builder.process(table_object)

    # then the header for the returned table should match the ones from the simple table
    headers = table.pop(0)
    expected_headers = [''] + table_object['columns']
    assert headers == expected_headers


def test_table_object_data_builder_does_build_data_from_simple_table(stub_simple_table_object):
    # given - a table without a category_caption value
    builder = TableObjectDataBuilder()
    table_object = stub_simple_table_object

    # when we process the object
    data = builder.process(table_object)
    data.pop(0)

    # then the header for the returned table should match the ones from the simple table
    expected_data = [['White', '25.6', '0.256'], ['Other', '16.6', '0.166']]
    assert data == expected_data


def test_table_object_data_builder_does_build_headers_from_grouped_table(stub_grouped_table_object):
    # given - a
    builder = TableObjectDataBuilder()
    table_object = stub_grouped_table_object

    # when we process the object
    table = builder.process(table_object)

    # then the header for the returned table should match the ones from the simple table
    headers = table.pop(0)
    expected_headers = ['Sex', 'Custom category caption', 'Value', 'Rate']
    assert headers == expected_headers


def test_table_object_data_builder_does_build_headers_from_legacy_grouped_table(stub_grouped_table_object):
    # given - a
    builder = TableObjectDataBuilder()
    table_object = stub_grouped_table_object
    table_object.pop('category_caption', None)

    # when we process the object
    table = builder.process(table_object)

    # then the header for the returned table should match the ones from the simple table
    headers = table.pop(0)
    expected_headers = ['Sex', '', 'Value', 'Rate']
    assert headers == expected_headers


def test_table_object_data_builder_does_build_data_from_grouped_table(stub_grouped_table_object):
    # given - a table without a category_caption value
    builder = TableObjectDataBuilder()
    table_object = stub_grouped_table_object

    # when we process the object
    data = builder.process(table_object)
    data.pop(0)

    # then the header for the returned table should match the ones from the simple table
    expected_data = [['Men', 'White', '25.6', '0.256'], ['Men', 'Other', '16.6', '0.166'],
                     ['Women', 'White', '12.8', '0.128'], ['Women', 'Other', '10.0', '0.100']]


def test_table_object_builder_does_build_object_from_simple_table(stub_page_with_simple_table):
    # given - a table without a category_caption value
    builder = TableObjectBuilder()
    dimension = stub_page_with_simple_table.dimensions[0]

    # when we process the object
    table_object = builder.build(stub_page_with_simple_table, dimension)

    # then the header for the returned table should match the ones from the simple table
    assert table_object is not None


def test_table_object_builder_does_build_object_from_grouped_table(stub_page_with_grouped_table):
    # given - a table without a category_caption value
    builder = TableObjectBuilder()
    dimension = stub_page_with_grouped_table.dimensions[0]

    # when we process the object
    table_object = builder.build(stub_page_with_grouped_table, dimension)

    # then the header for the returned table should match the ones from the simple table
    assert table_object is not None
