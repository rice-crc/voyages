from __future__ import unicode_literals

import re
import sys

subst = [
    (r'slaximp\s\-\s\(slaximp\*([.0-9]+)\)', 'slaximp * (1 - \\1)'),
    # remove trailing dot
    (r'\s*\.$', ''),
    # use is None test for missing values
    (r'missing\(([^\)]+)\)', '\\1 is None'),
    (r'\s+&\s+', ' and '),  # logic and
    (r'\s+\|\s+', ' or '),  # logic or
    (r'\s+\)', ')'),  # remove space before ')'
    # parse SPSS if with at most two levels of parentheses
    (r'if\s+\(([^\(]*(?:\([^\)]+\)[^\(]*)*)\)\s+(.*)$', 'if \\1:\n    \\2'),
    (r'~=', '!='),  # not equal comparisson
    (r'\s*(?<![<>=!~])=(?!=)\s*(?=.*:)', ' == '),  # equal comparisson
    (r'\s+:\s+', ': '),  # remove redundant spaces
    (r'\s*([><=+\-!\*/]+)\s*', ' \\1 '),  # space between operators
    (r'\s+lt\s+', ' < '),  # less than
    (r'\s+gt\s+', ' > '),  # greater than
]


def replace_many(original):
    result = original
    for (k, v) in subst:
        result = re.sub(k, v, result, flags=re.IGNORECASE)
    return result


lines = [replace_many(line.rstrip('\n')) + '\n' for line in open(sys.argv[1])]
with open(sys.argv[2], 'w') as f:
    f.writelines(lines)
