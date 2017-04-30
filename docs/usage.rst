=====
Usage
=====

To use PDF Table Extractor in a project::

    import pdf_table_extractor
    from drunken_child_in_the_fog import DrunkenChildInTheFog

    tables = extract_table_data(
    	   DrunkenChildInTheFog(open("test.pdf", "rb")).get_document())

Or, use CLI command:

.. code-block:: console

    $ pdf_extract_tables input.pdf output.xls --format=xls --verbose=3
