#!/usr/bin/env python

# see https://thoughtstreams.io/jtauber/littlewood-fractals/

import array
import colorsys
import itertools
import struct
import time
import zlib

import numpy


DEGREE = 16
SIZE = 200


print "generating roots for degree={}, size={}".format(DEGREE, SIZE)

hits = numpy.zeros((int(SIZE * 2.1), int(SIZE * 1.5)), dtype=numpy.int)
start = time.time()
max_hits = 0

count = 0
click = 2 ** DEGREE / 10
next = click
for poly in itertools.product(*([[-1, 1]] * DEGREE)):
    count += 1
    if count == next:
        print count
        next += click
    for root in numpy.roots((1,) + poly):
        x, y = round(root.real * SIZE), round(root.imag * SIZE)
        if x >= 0 and y >= 0:
            hits[x, y] += 1


filename = "littlewood_{}_{}.png".format(DEGREE, SIZE)
width = int(SIZE * 4)
height = int(SIZE * 2 * numpy.sqrt(2))
log_max = numpy.log(numpy.amax(hits))


def output_chunk(f, chunk_type, data):
    f.write(struct.pack("!I", len(data)))
    f.write(chunk_type)
    f.write(data)
    checksum = zlib.crc32(data, zlib.crc32(chunk_type))
    f.write(struct.pack("!i", checksum))


print "writing out PNG..."

hit_to_rgb = {}

with open(filename, "wb") as f:
    f.write(struct.pack("8B", 137, 80, 78, 71, 13, 10, 26, 10))
    output_chunk(f, "IHDR", struct.pack("!2I5B", width, height, 8, 2, 0, 0, 0))
    compressor = zlib.compressobj()
    data = array.array("B")
    for py in range(height):
        if py % 100 == 0:
            print py
        hy = abs(py - height / 2)
        data.append(0)
        for px in range(width):
            hx = abs(px - width / 2)
            h = hits[hx, hy]
            if h > 0:
                r, g, b = hit_to_rgb.get(h, (None, None, None))
                if r is None:
                    value = numpy.log(h) / log_max
                    r, g, b = (int(255 * x) for x in colorsys.hsv_to_rgb(value / 4, 1 - value, 0.5 + value / 2))
                    hit_to_rgb[h] = (r, g, b)
            else:
                r, g, b = 0, 0, 0
            data.extend([r, g, b])
    compressed = compressor.compress(data.tostring())
    flushed = compressor.flush()
    output_chunk(f, "IDAT", compressed + flushed)
    output_chunk(f, "IEND", "")

print "wrote out {} in {} seconds".format(filename, round(time.time() - start))
