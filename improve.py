import sys
import db

def parse_rates(f):
    rates = {}
    channel = 0
    for l in f.readlines():
        try:
            slot = int(l.split()[1].rstrip(','))
            try:            
                rates[slot].extend(map(float, l.split(':')[1].split()))
            except KeyError:
                rates[slot] = map(float, l.split(':')[1].split())
        except IndexError:
            continue

    return rates

def parse_vthrs(f):
    v = {}
    channel = 0
    for l in f.readlines():
        slot = int(l.split()[1].split(':')[1])
        dac = int(l.split()[3].split(':')[1].rstrip('];'))
        print slot, dac
        try:
            v[slot].append(dac)
        except KeyError:
            v[slot] = [dac]

    return v

if __name__ == '__main__':
    rate_file = sys.argv[1]

    thresh_file = None
    if len(sys.argv) > 2:
        thresh_file = sys.argv[2]

    with open(rate_file) as f:
        crate = int(f.readline().split()[2])
        rates = parse_rates(f)

    vthrs = None
    if thresh_file is not None:
        with open(thresh_file) as f:
            print f
            vthrs = parse_vthrs(f)
    else:
        vthrs = db.get_vthrs(crate)

    for slot in rates:
        for i in range(len(rates[slot])):
            for v in range(7):
                if rates[slot][i] > 2.0 * 10**v:
                    if vthrs[slot][i] + 1 > 255:
                        continue
                    vthrs[slot][i] += 1

    db.print_vthr_orcascript(vthrs)

