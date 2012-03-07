import sys
import couchdb

import config
import rw

URL = config.URL
USER = config.USER
PASS = config.PASS
DBNAME = config.DBNAME
VIEW = config.VIEW

def get_vthrs(crate):
    '''get a dict (by slot) of lists (by channel) of thresholds'''
    couch = couchdb.Server(URL)

    try:
        couch.resource.credentials = (USER, PASS)
    except NameError:
        pass

    db = couch[DBNAME]

    vthrs = {}
    for row in db.view(VIEW, startkey=[crate], endkey=[crate,{}], reversed=True):
        doc = row.value
        slot = doc['card']
        try:
            v = []
            for i in range(len(doc['hw']['vthr'])):
                v.append(doc['hw']['vthr'][i])
            vthrs[slot] = v
        except KeyError:
            vthrs[slot] = None

    return vthrs

if __name__ == '__main__':
    crate = int(sys.argv[1])
    vthrs = get_vthrs(crate)
    rw.print_vthr_orcascript(crate, vthrs)

