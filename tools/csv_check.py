from __future__ import print_function, unicode_literals

# This tool can be used to verify that CSV data was imported without any loss.
# After running the importcsv command, head to the Contribute section and
# export CSV files for the datasets (separately for TAST and I-Am). Then the
# functions below (check_intra, check_tast) can be used to detect any
# inconsistency or data loss.


default_ignore_keys = set(["status", "comments", "infant7"])
bool_values = ["true", "false"]
integral_fields = [
    "tonnage", "boy3", "girl3", "infant3", "feml3imp", "boy7", "girl7",
    "infant7", "adult7", "child7", "male7", "female7", "women7"
]


# Usage sample.
# 1. Import CSV files using the manage.py importcsv command
# 2. Run export CSV from Editorial Platform. Make sure to export
#    only published voyages and select a single DataSet (TAST/I-Am)
#    for each file download.
# 3. With both imported/exported CSV file pairings at hand, run
#    a Django Shell session: $ manage.py shell
# 4. Copy & paste code above into the shell.
# 5. Run the check_intra, check_tast functions as foolows:
#    delta = check_intra("path/to/imported.csv", "path/to/exported.csv")
#    get_fields_affected(delta)
#    ...
#    print_delta(delta)
