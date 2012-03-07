import sys
import couchdb
import config

URL = config.URL
USER = config.USER
PASS = config.PASS
DBNAME = config.DBNAME
VIEW = config.VIEW

orca_template = \
'''function main() {

rc = find(ORRunModel);
xl3 = find(ORXL3Model, %(crate)i, 0);

if (!rc || !xl3) {
  print("error finding run or xl3");
  return 1;
}

// vthr for crate %(crate)i
%(script)s

return 0;
}
'''

orca_line = '[xl3 setVthrDACsForSlot:%(slot)i withChannelMask:%(mask)s dac:%(dac)i];'

channel_masks = [hex(1 << channel) for channel in range(32)]

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

def print_vthr_orcascript(crate, vthrs):
    lines = []
    for slot in vthrs:
        if vthrs[slot] is not None:
            for i in range(len(vthrs[slot])):
                s = {
                    'slot': slot,
                    'mask': channel_masks[i],
                    'dac': vthrs[slot][i]
                }
                lines.append(orca_line % s)

    print orca_template % {'crate': crate, 'script': '\n'.join(lines)}

if __name__ == '__main__':
    crate = int(sys.argv[1])
    vthrs = get_vthrs(crate)
    print_vthr_orcascript(crate, vthrs)

