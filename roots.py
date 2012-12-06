#!/usr/bin/env python

# this just calculates the roots, it doesn't generate the heat map

# see https://thoughtstreams.io/jtauber/littlewood-fractals/

import itertools
import sys
import time

import numpy


DEGREE = 16
INNER_ONLY = False


print "generating roots for degree={}".format(DEGREE,)

start = time.time()

count = 0
click = 2 ** DEGREE / 10
next = click

if INNER_ONLY:
    filename = "roots_{}b.txt".format(DEGREE)
else:
    filename = "roots_{}.txt".format(DEGREE)

with open(filename, "wb") as f:
    for poly in itertools.product(*([[-1, 1]] * DEGREE)):
        count += 1
        if count == next:
            print >> sys.stderr, count
            next += click
        for root in numpy.roots((1,) + poly):
            if root.real >= 0 and root.imag >= 0:
                if not INNER_ONLY or abs(root) <= 1:
                    print >> f, root.real, root.imag

print >> sys.stderr, "wrote out {} in {} seconds".format(filename, time.time() - start)
