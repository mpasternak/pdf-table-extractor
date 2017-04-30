#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pdf_table_extractor
----------------------------------

Tests for `pdf_table_extractor` module.
"""

import os

import pytest
from click.testing import CliRunner
from drunken_child_in_the_fog.core import DrunkenChildInTheFog

from pdf_table_extractor import cli
from pdf_table_extractor import pdf_table_extractor


@pytest.fixture
def test_path():
    return os.path.dirname(__file__)


@pytest.fixture
def test_pdf(test_path):
    return open(os.path.join(test_path, "test.pdf"), "rb")


@pytest.fixture
def test_pdf_doc(test_pdf):
    return DrunkenChildInTheFog(test_pdf).get_document()


def test_pdf_table_extractor(test_pdf):
    tables = pdf_table_extractor.extract_table_data(test_pdf)  # , verbose=3)
    assert len(tables) == 3
    assert tables[1][2][3] == "every row counts yea"


def test_command_line_interface(test_path):
    runner = CliRunner()
    input_path = os.path.join(test_path, "test.pdf")
    with runner.isolated_filesystem():
        result = runner.invoke(cli.main, [input_path, "output.csv"])
        assert result.exit_code == 0
        assert 'multiple rows in table' in open("output.csv", "r").read()

    with runner.isolated_filesystem():
        result = runner.invoke(cli.main, [input_path, "output.xls",
                                          "--format=xls"])
        assert result.exit_code == 0

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
