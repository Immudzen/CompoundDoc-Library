import transaction

def subTrans(seq,  count):
    "do a subtransaction for every count"
    for idx,  item in enumerate(seq):
        if idx % count == 0:
            transaction.savepoint(optimistic=True)
        yield item
        
def subTransDeactivate(seq, count, persistent=None):
    "do a subtransaction for every count and also deactivate all objects"
    cacheGC = persistent._p_jar.cacheGC if persistent is not None else lambda :None
    for idx,  item in enumerate(seq):
        if idx % count == 0:
            cacheGC()
            transaction.savepoint(optimistic=True)
        yield item
        item._p_deactivate()

def subTransDeactivateKeyValue(seq, count, persistent=None):
    "do a subtransaction for every count and also deactivate all objects"
    cacheGC = persistent._p_jar.cacheGC if persistent is not None else lambda :None
    for idx,  item in enumerate(seq):
        if idx % count == 0:
            cacheGC()
            transaction.savepoint(optimistic=True)
        yield item
        item[1]._p_deactivate()