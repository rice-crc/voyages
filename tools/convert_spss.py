import re
import sys

subst = [
    ('\s*\.$', ''), # remove trailing dot
	('missing\(([^\)]+)\)', '\\1 is None'), # use is None test for missing values
	('\s+&\s+', ' and '), # logic and
	('\s+\|\s+', ' or '), # logic or
	('if\s+\(([^\(]*(?:\([^\)]+\)[^\(]*)*)\)\s+(.*)$', 'if \\1: \\2'), # parse SPSS if with at most two levels of parentheses
	('~=', '!='), # not equal comparisson
	('\s*(?<![<>=!~])=(?!=)\s*(?=.*:)', ' == '), # equal comparisson
	('\s+:\s+', ': '), # remove redundant spaces
	('\s*([><=+\-!\*/]+)\s*', ' \\1 '), # space between operators
	('\s+lt\s+', ' < '), # less than
	('\s+gt\s+', ' > '), # greater than
]

def replace_many(original):
	result = original
	for (k, v) in subst:
		result = re.sub(k, v, result, flags=re.IGNORECASE)
	return result

lines = [replace_many(line.rstrip('\n')) + '\n' for line in open(sys.argv[1])]
with open(sys.argv[2], 'w') as f:
	f.writelines(lines)
