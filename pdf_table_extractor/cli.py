# -*- encoding: utf-8 -*-

from __future__ import print_function

import click

from .pdf_table_extractor import extract_table_data


@click.command()
@click.option('--verbose', type=int, default=0)
@click.option('--format', type=str, default="csv")
@click.option('--fuzzy-border', type=float, default="0.5")
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=str)
def main(input, output, format, verbose, fuzzy_border):
    """This script tries to extract table data from file INPUT
    """
    tables = extract_table_data(input, verbose, fuzzy_border=fuzzy_border)

    if format == "csv":
        import csv
        output = open(output, "w")
        o = csv.writer(output)
        for table in tables:
            for row in table:
                o.writerow(row)
        output.close()

    elif format == "xls":
        import xlwt
        book = xlwt.Workbook(encoding="utf-8")

        for sheet_no, table in enumerate(tables):
            sheet = book.add_sheet("Table %s" % sheet_no)

            for row_no, row in enumerate(table):
                for col_no, col in enumerate(row):
                    sheet.write(row_no, col_no, col)

        output = open(output, "wb")
        book.save(output)
        output.close()

    else:
        raise click.BadOptionUsage("Unknown format %s" % format)


if __name__ == '__main__':
    main()
