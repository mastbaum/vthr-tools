import sys
import couchdb
import config

URL = config.URL
USER = config.USER
PASS = config.PASS
DBNAME = config.DBNAME
VIEW = config.VIEW

orca_template = '[xl3 setVthrDACsForSlot:%(slot)i withChannelMask:%(mask)s dac:%(dac)i];'

channel_masks = [
    '0x1',
    '0x2',
    '0x4',
    '0x8',
    '0x10',
    '0x20',
    '0x40',
    '0x80',
    '0x100',
    '0x200',
    '0x400',
    '0x800',
    '0x1000',
    '0x2000',
    '0x4000',
    '0x8000',
    '0x10000',
    '0x20000',
    '0x40000',
    '0x80000',
    '0x100000',
    '0x200000',
    '0x400000',
    '0x800000',
    '0x1000000',
    '0x2000000',
    '0x4000000',
    '0x8000000',
    '0x10000000',
    '0x20000000',
    '0x40000000',
    '0x80000000'
]

def get_vthrs(crate):
    '''get a dict (by slot) of lists (by channel) of thresholds'''
    couch = couchdb.Server(URL)

    try:
        couch.resource.credentials = (USER, PASS)
    except NameError:
        pass

    db = couch[DBNAME]

    vthrs = {}
    for row in db.view(VIEW, startkey=[crate], endkey=[crate,{}]):
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

def print_vthr_orcascript(vthrs):
    for slot in range(len(vthrs)):
        if slot in vthrs and vthrs[slot] is not None:
            for i in range(len(vthrs[slot])):
                s = {
                    'slot': slot,
                    'mask': channel_masks[i],
                    'dac': vthrs[slot][i]
                }

                print orca_template % s
        else:
            print 'Sorry, no vthrs for slot', slot

if __name__ == '__main__':
    crate = int(sys.argv[1])
    vthrs = get_vthrs(crate)
    print_vthr_orcascript(vthrs)

