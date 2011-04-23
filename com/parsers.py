import csv
import StringIO

def makeCSV(seq, eol='\n', sep=','):
    temp = StringIO.StringIO()
    writer = csv.writer(temp, lineterminator=eol, delimiter=sep)
    writer.writerows(seq)
    output = temp.getvalue()
    temp.close()
    return output
    
def makeCSVStream(seq, REQUEST, eol='\n', sep=',', filename='file.csv'):
    REQUEST.RESPONSE.setHeader('Content-Disposition' , 'attachment; filename="%s"' % filename)
    REQUEST.RESPONSE.setHeader('Content-Type',"text/x-csv")
    writer = csv.writer(REQUEST.RESPONSE, lineterminator=eol, delimiter=sep)
    writer.writerows(seq)