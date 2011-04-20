import itertools

def createTable(rows, table_classes=None):
    "create a table from this list it must be a balanced list within a list"
    if table_classes is not None:
        table_css = ' class="%s"' % ' '.join(table_classes)
    else:
        table_css = ''
    temp = ['<table%s>' % table_css]
    format = '<td>%s</td>'
    for row in rows:
        temp.append('<tr>')
        temp.extend([format % cell for cell in row])
        temp.append('</tr>')
    temp.append('</table>')
    return ''.join(temp)
    
def formatListForTable(seq, columns, filler=''):
    "return a list that is formated for this many columns and fill it with the value in filler for extra"
    return list(itertools.izip(*[itertools.chain(seq, itertools.repeat(filler, columns-1))]*columns))