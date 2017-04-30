# -*- encoding: utf-8 -*-

from __future__ import print_function

import sys

import click

from .pdf_table_extractor import extract_table_data


@click.command()
@click.option('--verbose', type=int, default=0)
@click.option('--format', type=str, default="csv")
@click.argument('input', type=click.File('rb'))
# @click.argument('output', type=click.File('wb'), default=sys.stdout)
def main(input, format, verbose):
    """This script tries to extract table data from file INPUT
    """
    tables = extract_table_data(input, verbose)

    if format == "csv":
        import csv
        o = csv.writer(sys.stdout)
        for table in tables:
            for row in table:
                o.writerow(row)

    elif format == "xls":
        import xlwt
        book = xlwt.Workbook(encoding="utf-8")

        for sheet_no, table in enumerate(tables):
            sheet = book.add_sheet("Table %s" % sheet_no)

            for row_no, row in enumerate(table):
                for col_no, col in enumerate(row):
                    sheet.write(row_no, col_no, col)

        book.save(sys.stdtou)

    else:
        raise click.BadOptionUsage("Unknown format %s" % format)


if __name__ == '__main__':
    main()
