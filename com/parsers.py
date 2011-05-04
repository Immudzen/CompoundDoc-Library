import csv
import StringIO

def makeCSV(seq, eol='\n', sep=','):
    """return a string that is a csv file with the eol and seperator handed in
    sequence is a sequence of sequences (tuple of tuples for instance) that can be
    turned into a csv file"""
    temp = StringIO.StringIO()
    writer = csv.writer(temp, lineterminator=eol, delimiter=sep)
    writer.writerows(seq)
    output = temp.getvalue()
    temp.close()
    return output
    
def makeCSVStream(seq, REQUEST, eol='\n', sep=',', filename='file.csv'):
    """stream a CSV file to the viewer over the REQUEST object,
    this allows a file to be lazy sent so the viewer will start
    downloading immediately, sequence should be a generator of
    tuples so that entries can be written line by line as they come in,
    REQUEST is required and all other fields are optional"""
    REQUEST.RESPONSE.setHeader('Content-Disposition' , 'attachment; filename="%s"' % filename)
    REQUEST.RESPONSE.setHeader('Content-Type',"text/x-csv")
    writer = csv.writer(REQUEST.RESPONSE, lineterminator=eol, delimiter=sep)
    writer.writerows(seq)