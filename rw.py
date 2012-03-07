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

def print_vthr_orcascript(crate, vthrs):
    lines = []
    for slot in vthrs:
        if vthrs[slot] is not None:
            for i in range(len(vthrs[slot])):
                s = {
                    'slot': slot,
                    'mask': hex(1 << i),
                    'dac': vthrs[slot][i]
                }
                lines.append(orca_line % s)

    print orca_template % {'crate': crate, 'script': '\n'.join(lines)}

def parse_rate_file(f):
    rates = {}
    for l in f.readlines():
        if 'XL3 crate' in l:
            crate = int(l.split()[2])
        if 'slot' in l:
            slot = int(l.split()[1].rstrip(','))
            try:
                rates[slot].extend(map(float, l.split(':')[1].split()))
            except KeyError:
                rates[slot] = map(float, l.split(':')[1].split())

    return crate, rates

def parse_vthr_file(f):
    v = {}
    for l in f.readlines():
        if 'ORXL3Model' in l:
            crate = int(l.split()[2].split(',')[1])
        if 'xl3 setVthrDACsForSlot' in l:
            slot = int(l.split()[1].split(':')[1])
            dac = int(l.split()[3].split(':')[1].rstrip('];'))
            try:
                v[slot].append(dac)
            except KeyError:
                v[slot] = [dac]

    return crate, v

def parse_vthr_array(crate, slot, s):
    s = s.strip('[]')
    v = {slot: map(float, s.split(','))}
    return crate, v

