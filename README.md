Voltage Threshold Tools
=======================
For setting up channel thresholds with ORCA scripts

CLI
---
Make vthr-loading script for a crate from database values:

    $ python db.py <crate_num>


Make a new vthr-loading file with improved thresholds given measured CMOS rates (copied from the ORCA log):

    $ python improve.py <cmos_rates.txt> [vthr_script]

If `vthr_script` is given, use it as the starting point. Otherwise, use the database.

Module
------
### `db` ###
* `db.get_vthrs(crate)` takes a crate number and returns a dict where keys are slot number and values are lists of the 32 channel CMOS rates

### `improve` ###
* `improve.improve(vthrs, rates, verbose=False)` takes a vthr dict and a cmos dict (see `rw`)

### `rw` ###
* `rw.print_vthr_orcascript(crate, vthrs)` prints the script to set thresholds given in vthrs dict on given crate
* `rw.parse_rate_file(f)` reads a file containing ORCA log cmos rates and returns (crate num, dict with slot numbers as keys and list of rates per channel as values)
* `rw.parse_vthr_file(f)` reads an ORCA script and returns (crate num, dict with slot numbers as keys and list of thresholds per channel as values)
* `rw.parse_vthr_array(crate, slot, s)` turns an single-slot threshold array into a vthr dictionary

