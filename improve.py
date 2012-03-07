import sys
import db

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

def improve(vthrs, rates, verbose=False):
    bumped_up = 0
    bumped_down = 0
    for slot in rates:
        for i in range(len(rates[slot])):
            for v in range(7):
                if rates[slot][i] > 4.0 * 10**v:
                    if vthrs[slot][i] + 1 > 255:
                        continue
                    bumped_up += 1
                    vthrs[slot][i] += 1
            if rates[slot][i] <= 0:
                if vthrs[slot][i] - 1 < 0:
                    continue
                bumped_down += 1
                vthrs[slot][i] -= 1
    if verbose:
        print 'bumped up', bumped_up, 'thresholds'
        print 'bumped down', bumped_down, 'thresholds'

    return vthrs

if __name__ == '__main__':
    rate_file = sys.argv[1]

    with open(rate_file) as f:
        crate, rates = parse_rate_file(f)

    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            crate, vthrs = parse_vthr_file(f)
    else:
        vthrs = db.get_vthrs(crate)

    vthrs = improve(vthrs, rates)

    db.print_vthr_orcascript(crate, vthrs)

