from __future__ import print_function, unicode_literals

import sys

import unicodecsv

# We require three arguments, the TAST CSV file, the IntraAmerican CSV file,
# and an Output file.

if len(sys.argv) != 4:
    print("You must pass 3 args: TAST CSV, IAm CSV, Output CSV")
    sys.exit()

iam_column = u'IntraAmer'


def load_csv(file_name, iam_val):
    results = []
    cols = []
    ids = []
    with open(file_name, 'rU') as f:
        print("Loading " + file_name)
        reader = unicodecsv.DictReader(f, delimiter=',')
        cols = [x.lower() for x in reader.fieldnames if x != iam_column]
        for row in reader:
            ids.append(int(row[u'voyageid']))
            row[iam_column] = iam_val
            results.append(row)
    return results, cols, ids


tast_rows, tast_cols, tast_ids = load_csv(sys.argv[1], 0)
iam_rows, iam_cols, iam_ids = load_csv(sys.argv[2], 1)
bad_ids = set(tast_ids) & set(iam_ids)
if len(bad_ids) > 0:
    print("The voyage Ids are not unique")
    print(bad_ids)
    sys.exit()

all_cols = set(tast_cols + iam_cols + [iam_column])
all_rows = tast_rows + iam_rows

with open(sys.argv[3], 'w') as out_file:
    writer = unicodecsv.DictWriter(out_file, fieldnames=all_cols)
    writer.writeheader()
    for row in all_rows:
        writer.writerow(row)
