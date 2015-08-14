sed -e 's/\"/\\\"/g' $1 | sed -e 's/.*trans::\(.*\)$/gettext("\1");/' | sort -u > /tmp/trans_log.c
xgettext --from-code=UTF-8 /tmp/trans_log.c -d $2
# rm -f /tmp/trans_log.c
sed -i.bak $2.po -e 's/CHARSET/UTF-8/'
echo "Use msgcat voyages/locale/xx/LC_MESSAGES/django.po $2.po -o output.po to merge the PO files while keeping existing translations"
echo "Replace xx above by the locale, e.g. pt, de"


