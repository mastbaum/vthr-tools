import sys
import db
import rw

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
        crate, rates = rw.parse_rate_file(f)

    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            crate, vthrs = rw.parse_vthr_file(f)
    else:
        vthrs = db.get_vthrs(crate)

    vthrs = improve(vthrs, rates)
    rw.print_vthr_orcascript(crate, vthrs)

