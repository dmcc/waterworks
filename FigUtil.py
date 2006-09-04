from sets import Set
import sys

def dict_to_table(d, headers=True, x_header='', reverse=False):
    """Convert dict with (x, y) as keys to a 2D table."""
    all_x = Set()
    all_y = Set()
    for x, y in d.keys():
        all_x.add(x)
        all_y.add(y)
    all_x = list(all_x)
    all_y = list(all_y)
    all_x.sort()
    all_y.sort()
    if reverse:
        if 'x' in reverse:
            all_x.reverse()
        if 'y' in reverse:
            all_y.reverse()

    if headers:
        table = [[x_header] + all_y]
    else:
        table = []
    for i, x in enumerate(all_x):
        row = [None] * len(all_y)
        for j, y in enumerate(all_y):
            row[j] = d.get((x, y))
        if headers:
            row.insert(0, x)
        table.append(row)
    return table

def format_table(table, format='csv', outputstream=sys.stdout):
    if format in ('csv', 'tsv'):
        import csv
        dialect = {'csv' : csv.excel, 'tsv' : csv.excel_tab}[format]
        writer = csv.writer(outputstream, dialect=dialect)
        for row in table:
            writer.writerow(row)
    elif format == 'tex':
        import TeXTable
        print >>outputstream, TeXTable.texify(table, has_header=True)
    else:
        raise ValueError("Sorry, only 'csv', 'tsv', and 'tex' formats are supported now.")

if __name__ == "__main__":
    print dict_to_table({('add-0', '01') : 7,
                         ('add-0', '22') : 8,
                         ('add-0', '24') : 9,
                         ('add-1', '01') : 10,
                         ('add-1', '22') : 11,
                         ('add-1', '24') : 12,})
    format_table(dict_to_table({('add-0', '01') : 7,
                         ('add-0', '22') : 8,
                         ('add-0', '24') : 9,
                         ('add-1', '01') : 10,
                         ('add-1', '22') : 11,
                         ('add-1', '24') : 12,}), format='tex')
