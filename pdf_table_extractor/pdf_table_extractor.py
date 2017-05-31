# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from drunken_child_in_the_fog.core import DrunkenChildInTheFog, \
    NoSuchElement, BoxQuery


def print_debug(*args, **kw):
    """Output debug information"""
    print(*args, **kw)


def dont_debug(*args, **kw):
    pass


def extract_table_data(input, verbose=0, fuzzy_border=0.5,
                       horizontal_fuzziness=1.0,
                       cell_text_query="starts_inside"):
    """
    :param input: input document
    :type input: :class:`drunken_child_in_the_fog.core.DrunkenChildInTheFog`
    :param verbose: will spew out a lot of debugging information if 1
    :param fuzzy_border: borders usuallly aren't ideal; this parameter
        describes a range which will be used when looking for horizontal and
        vertical lines, and text.
    :param horizontal_fuzziness: for even more less-than-ideal borders,
        this is a margin to which horizontal coordinates of a line will be
        expanded when looking for table borders. See code.
    :type fuzzy_border: float
    :param cell_text_query: :class:`drunken_child_in_the_fog.core.BoxQuery`
        parameter, used when looking for text inside cell table. See
        :class:`drunken_child_in_the_fog.core.BoxQuery` docs for details
    :return: a list containing tables. Each table is a list of rows. Each
        row is a list of strings.
    """
    global debug, print_debug, dont_debug

    debug = print_debug
    if verbose == 0:
        debug = dont_debug

    doc = DrunkenChildInTheFog(input).get_document()
    for elem in doc.everything():
        debug(
            "%f, %f, %f, %f, %09.2f, %s" % (elem.x1, elem.y1,
                                            elem.x2,
                                            elem.y2,
                                            elem.position_in_document(),
                                            elem.text))

    tables = []

    for page in doc.get_pages():
        assert page.sorted
        top = left = 0

        while True:
            ret = []
            if verbose > 0:
                debug("~" * 40)
                debug("TOP, LEFT, WIDTH, HEIGHT: ", top, left, page.width,
                      page.height)

            try:
                first_vertical_line = page.starting_from(
                    top=top, left=left).lines().vertical().first()
            except NoSuchElement:
                break

            try:
                first_horizontal_line = page.starting_from(
                    top=top, left=left).lines().horizontal().first()
            except NoSuchElement:
                break

            debug("X" * 90)
            debug(first_horizontal_line)
            debug(first_vertical_line)
            debug("X" * 90)

            top = first_vertical_line.y2

            table = dict(x1=first_horizontal_line.x1 - horizontal_fuzziness,
                         y1=first_horizontal_line.y2,
                         x2=first_horizontal_line.x2 + horizontal_fuzziness,
                         y2=first_vertical_line.y2,
                         fuzzy_border=fuzzy_border)

            debug("=" * 78, "\n", "TABLE", table, "\n", "=" * 78)
            horizontal_lines = page.inside(
                BoxQuery(**table)).lines().horizontal()
            vertical_lines = page.inside(
                BoxQuery(**table)).lines().vertical().all()
            vertical_lines.sort(key=lambda elem: elem.x1)

            debug("VERTICAL LINES", "\n", "-" * 78)
            for elem in vertical_lines:
                debug(elem)
            debug("HORIZONTAL LINES", "\n", "-" * 78)
            for elem in horizontal_lines:
                debug(elem)

            previous_horizontal_line = horizontal_lines.first()
            for current_horizontal_line in horizontal_lines.all()[1:]:
                debug("CURRENT HORIZONTAL LINE", current_horizontal_line)
                row = []

                this_row = dict(
                    x1=previous_horizontal_line.x1,
                    y1=previous_horizontal_line.y2,
                    x2=current_horizontal_line.x2,
                    y2=current_horizontal_line.y2
                )
                debug("THIS ROW", this_row)

                previous_vertical_line = first_vertical_line
                for current_vertical_line in vertical_lines:
                    this_cell = dict(
                        x1=previous_vertical_line.x1,
                        y1=previous_horizontal_line.y1,
                        x2=current_vertical_line.x1,
                        y2=current_horizontal_line.y1,
                        fuzzy_border=fuzzy_border
                    )

                    debug("THIS CELL", this_cell)

                    value = " ".join([x.text for x in page.inside(
                        BoxQuery(**this_cell), cell_text_query).text()])
                    debug("THIS CELL TEXT [%s]" % value)
                    previous_vertical_line = current_vertical_line
                    row.append(value)

                previous_horizontal_line = current_horizontal_line
                ret.append(row)

            tables.append(ret)

    return tables
