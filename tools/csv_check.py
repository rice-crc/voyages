# This tool can be used to verify that CSV data was imported without any loss.
# After running the importcsv command, head to the Contribute section and export
# CSV files for the datasets (separately for TAST and I-Am). Then the functions
# below (check_intra, check_tast) can be used to detect any inconsistency or
# data loss.

import itertools
import re
import unicodecsv

def get_csv_data(fpath):
    f = list(open(fpath, "rb"))
    f[0] = f[0].decode("utf-8").lower().replace("_", "").encode("utf-8")
    reader = unicodecsv.DictReader(f, encoding="utf-8", delimiter=",")
    rows = []
    for row in reader:
        rows.append(row)
    rows.sort(key=lambda r: r["voyageid"])
    return rows

default_ignore_keys = set(["status", "comments", "infant7"])
bool_values = ["true", "false"]
integral_fields = ["tonnage", "boy3", "girl3", "infant3", "feml3imp", "boy7", "girl7", "infant7", "adult7", "child7", "male7", "female7", "women7"]

def get_set_from_prefix(row, prefix):
    row_set = [row.get(prefix + c) for c in "abcdefghijklmnop"]
    return set([o for o in row_set if o is not None and o.strip() != '' and o.strip() != "."])

def compare_csv(r1, r2, default_values={}, ignore_keys=default_ignore_keys, key_map=None):
    pairs = itertools.zip_longest(r1, r2)
    bad = []
    for (a, b) in pairs:
        if a is None or b is None: 
            bad.append((a, b, { "__row__": "Missing" }))
        else:
            keys = set(a.keys()).union(b.keys())
            diffs = {}
            for k in keys:
                if key_map: k = key_map.get(k, k)
                if k in ignore_keys: continue
                x = a.get(k, default_values.get(k, "")).strip()
                y = b.get(k, default_values.get(k, "")).strip()
                if x == y: continue
                if (x == ",," and y == "") or (x == "" and y == ",,"): continue
                # Same date?
                dx = re.search(r"^(\d+)[,/-](\d+)[,/-](\d+)$", x)
                dy = re.search(r"^(\d+)[,/-](\d+)[,/-](\d+)$", y)
                if dx and dy and int(dx[1]) == int(dy[1]) and int(dx[2]) == int(dy[2]) and int(dx[3]) == int(dy[3]): continue
                try:
                    # If the field is numeric, we compare with some tolerance
                    fx = float(x if x != "" else "0")
                    fy = float(y if y != "" else "0")
                    delta = abs(fx - fy)
                    if (delta < 0.001): continue
                    if k in integral_fields and delta < 0.51: continue
                except: pass
                try:
                    # Boolean comparisson
                    bx = x.lower()
                    by = y.lower()
                    if bx in bool_values and by in bool_values and bx == by: continue
                except: pass
                diffs[k] = "Fields differ: \"" + str(a.get(k)) + "\" != \"" + str(b.get(k)) + "\""
            if len(diffs) > 0:
                # See if it the errors are due to the ordering in a multi-value field (e.g. owner)
                for prefix in ["owner", "captain"]:
                    prefix_diffs = [key for key in diffs.keys() if key.startswith(prefix)]
                    for k in prefix_diffs:
                        diffs.pop(k)
                    prefix_set_a = get_set_from_prefix(a, prefix)
                    prefix_set_b = get_set_from_prefix(b, prefix)
                    if prefix_set_a != prefix_set_b:
                        diffs[prefix + "_set"] = "Set of " + prefix + " is different: " + str(prefix_set_a) + " vs. " + str(prefix_set_b)
            if len(diffs) > 0: bad.append((a, b, diffs))
    return bad

def check_files(name, imported_csv_file, exported_csv_file, default_values, ignore_keys, key_map=None):
    imported_csv_data = get_csv_data(imported_csv_file)
    exported_csv_data = get_csv_data(exported_csv_file)
    return compare_csv(imported_csv_data, exported_csv_data, default_values, ignore_keys, key_map)

def check_intra(imported_csv_file, exported_csv_file):
    return check_files(
        "intra",
        imported_csv_file,
        exported_csv_file,
        { "evgreen": "false" },
        default_ignore_keys | 
            set(["afrinfo", 
                "othercargo",
                "dateland1",
                "dateland2",
                "datedep",
                "datebuy",
                "dateleftafr",
                "voyageid2"]),
        { "datebuy1": "datebuy" })

def check_tast(imported_csv_file, exported_csv_file):
    return check_files(
        "intra",
        imported_csv_file,
        exported_csv_file,
        {},
        default_ignore_keys | set(["datebuy",
            "datedep",
            "datedepam",
            "dateland1",
            "dateland2",
            "dateland3",
            "dateend",
            "dateleftafr"]))

def get_fields_affected(delta):
    all = set()
    for x in delta:
        all = all | set(x[2].keys())
    return all

def print_delta(delta):
    if len(delta) > 0:
        print("Check failed!")
        for item in delta:
            voyage_id = item[0]["voyageid"]
            if item[1]["voyageid"] != voyage_id:
                print("- Voyage id mismatch " + voyage_id + "/" + item[0]["voyageid"])
            else:
                print("- Voyage id: " + voyage_id)
            print(str(item[2]))

# Example test
# delta = check_intra("path/to/imported.csv", "path/to/exported.csv")
# get_fields_affected(delta)
# ...
# print_delta(delta)
