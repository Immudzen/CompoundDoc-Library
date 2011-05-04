import itertools

def createTable(rows, table_classes=None):
    """create a table from this list it must be a balanced list within a list, table_classes is an
    optional arguement and it allows you to set a list of classes on the <table> element
    tables_classes is a sequence of strings"""
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
    "return a list that is formated for [columns numbers] and fill it with the value in filler for extra"
    return list(itertools.izip(*[itertools.chain(seq, itertools.repeat(filler, columns-1))]*columns))
    
def docType(REQUEST, encoding='iso-8859-15', language_code='en', frames=0, html5=0):
    """create a doctype for a page, REQUEST is required and the other fields are optional 
    if you hand in frames it will use a frame doctype for html4, if you hand in a non-false html5
    value it will generate an html5 doctype"""
    REQUEST.RESPONSE.setHeader('content-type', 'text/html; charset=%s' % encoding)
    if html5:
        return '<!DOCTYPE HTML><html lang="%s">' % language_code
    elif frames:
        return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<html lang="%s">''' % language_code
    else:
        return '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="%s">''' % language_code

def link_css(css, CacheVersionURL=None, media=None):
    "create a css link tag and version it if possible"
    if CacheVersionURL is not None:
        url = CacheVersionURL.version_absolute_url_path(css)
    else:
        url = css.absolute_url_path()
    media = 'media="%s"' % media if media is not None else ''
    return '<link rel="stylesheet" type="text/css" href="%s" %s>' % (url, media)
    
def link_js(js, CacheVersionURL=None):
    "create a js script tag and version it if possible"
    if CacheVersionURL is not None:
        url = CacheVersionURL.version_absolute_url_path(js)
    else:
        url = js.absolute_url_path()
    return '<script type="text/javascript" src="%s"></script>' % url