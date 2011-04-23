import zExceptions

def catalogIter(records):
    "iterate over a catalog safely"
    for record in records:
        try:
            item = record.getObject()
            if item is not None:
                yield item
        except (zExceptions.Unauthorized, zExceptions.NotFound, KeyError, AttributeError):
            pass

def catalogIterItems(records):
    "iterate over a catalog safely"
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
    "iterate over a catalog safely"
    for record in records:
        try:
            item = record.getObject()
            if item is not None:
                yield (record, item)
        except (zExceptions.Unauthorized, zExceptions.NotFound, KeyError, AttributeError):
            pass

def loadRecord(record):
    "load this single record"
    try:
        return record.getObject()
    except (zExceptions.Unauthorized, zExceptions.NotFound, KeyError, AttributeError):
        return None
