#!/bin/bash
# Put the output of the synclegacydb script to a file, and give the filename as the argument of this function
echo -n "Number of problem text_refs: "
cat "${1}" | grep "WARNING: Could not find source for " | wc -l
echo
cat "${1}" | grep "WARNING: Could not find source for " | sed -e 's/WARNING: Could not find source for /"/' -e 's/ on order.* for voyage .*$/"/' | sort | uniq -c
