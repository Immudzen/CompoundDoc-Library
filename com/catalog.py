import zExceptions

def catalogIter(records):
    "iterate over a catalog safely and return the object for a record"
    for record in records:
        try:
            item = record.getObject()
            if item is not None:
                yield item
        except (zExceptions.Unauthorized, zExceptions.NotFound, KeyError, AttributeError):
            pass

def catalogIterItems(records):
    "iterate over a catalog safely and return a list of (record, object) pairs"
    temp = []
    for record in records:
        try:
            item = record.getObject()
            if item is not None:
                temp.append((record, item))
        except (zExceptions.Unauthorized, zExceptions.NotFound, KeyError, AttributeError):
            pass
    return temp

def catalogIterItems2(records):
    "iterate over a catalog safely and return a generator of (record, object) pairs (does not work inside zope)"
    for record in records:
        try:
            item = record.getObject()
            if item is not None:
                yield (record, item)
        except (zExceptions.Unauthorized, zExceptions.NotFound, KeyError, AttributeError):
            pass

def loadRecord(record):
    "load this single record safely"
    try:
        return record.getObject()
    except (zExceptions.Unauthorized, zExceptions.NotFound, KeyError, AttributeError):
        return None
