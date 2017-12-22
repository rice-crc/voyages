SCRIPT_PATH=$(dirname "$(realpath -s "$0")")
DATA_PATH=$SCRIPT_PATH/../initialdata/
# For all fixture files that are not test*.json (test only fixtures) or users.json we
# list all the model types that appear in the fixture file and generate a single
# dumpdata command will all the models in the file. The order in which the models
# appear is crucial to ensure that dependent models appear after in the file, otherwise
# the loaddata commands for the fixtures will fail.
CURRENT_PATH=$(pwd)
cd $DATA_PATH
for f in `(ls | grep -v '^test' | grep -v '^users')`; do echo -n './manage.py dumpdata --all '; grep -oP '"model": "\K.*(?=")' $f | awk '!x[$0]++' | tr '\n' ' '; echo "--indent 4 > /tmp/dumps/$(basename $f)"; done
cd $CURRENT_PATH
