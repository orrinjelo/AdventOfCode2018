#!/usr/bin/env python3

import re
import sys

pattern = re.compile('Step (.) must be finished before step (.) can begin')

print('digraph graphname {')
for line in open(sys.argv[1]):
    a, b = (pattern.match(line).groups())
    print('{} -> {};'.format(a, b)) 
print('}')

# Save output to file and `dot -Tpng resultfile`