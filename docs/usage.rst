=====
Usage
=====

To use PDF Table Extractor in a project::

    from pdf_table_extractor.pdf_table_extractor import extract_table_data

    tables = extract_table_data(open("test.pdf", "rb")).get_document()

Or, use CLI command:

.. code-block:: console

    $ pdf_extract_tables input.pdf output.xls --format=xls --verbose=3
