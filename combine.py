#!/usr/bin/python

import itertools
from math import floor
import numpy
import os
import png

def print1d(data, cols, rows, index, pad=4):
	data = list(data)
	for row in range(rows):
		s = str(row).rjust(3) + ':'
		for col in range(cols):
			s += str(data[row][col * 4 + index]).rjust(pad)
		print s

def print2d(data, cols, rows, index, pad=4):
	for row in range(rows):
		s = str(row).rjust(3) + ':'
		for col in range(cols):
			s += str(data[row][col * 4 + index]).rjust(pad)
		print s

def print3d(image3d, cols, rows, index, pad=4):
	for row in range(rows):
		s = str(row).rjust(3) + ':'
		for col in range(cols):
			s += str(image3d[row][col][index]).rjust(pad)
		print s


r = png.Reader(open('texture.png', 'rb'))
texcols, texrows, texdata, texmeta = r.read()

print 'texrows: ' + str(texrows)
print 'texcols: ' + str(texcols)
print 'texplanes: ' + str(texmeta['planes'])

tex2d = numpy.vstack(itertools.imap(numpy.uint16, texdata))
tex3d = numpy.reshape(tex2d, (texrows, texcols, texmeta['planes']))

r = png.Reader(open('uvpass.png', 'rb'))
cols, rows, uvdata, uvmeta = r.read()
uv2d = numpy.vstack(itertools.imap(numpy.uint16, uvdata))
uv3d = numpy.reshape(uv2d, (rows, cols, uvmeta['planes']))

print 'cols: ' + str(cols)
print 'rows: ' + str(rows)
print 'uvplanes: ' + str(uvmeta['planes'])

out3d = numpy.empty((rows, cols, 4), numpy.uint8)
for row in range(rows):
	for col in range(cols):
		#out3d[row][col] = [float(row) * 255 / rows, float(col) * 255 / cols, 255, 255]
		if uv3d[row][col][2] == 0:
			out3d[row][col] = [0, 0, 0, 255]
		else:
			texrow = int(texrows - uv3d[row][col][1] / 65536.0 * texrows - 1)
			texcol = int(uv3d[row][col][0] / 65536.0 * texcols)
			out3d[row][col] = tex3d[texrow][texcol][0:4]
			out3d[row][col][3] = uv3d[row][col][3]

print 'outcols: ' + str(cols)
print 'outrows: ' + str(rows)
print 'outplanes: ' + str(4)


"""
		if uv3d[x][y][2] < 65535:
			out[x][y] = [0, 0, 0]
		else:
			texx = int(uv3d[x][y][0] / 65536.0 * texwidth)
			texy = int(uv3d[x][y][1] / 65536.0 * texheight)
			#print str(x) + "," + str(y) + ": " + str(uv3d[x][y]) + " " + str(texx) + "," + str(texy) + ": " + str(tex3d[texx][texy])
			out[x][y] = tex3d[texx][texy][0:3]
			#out[x][y] = [float(x) * 255 / uvwidth, float(y) * 255 / uvheight, 255]
"""

# FIXME: Use numpy.reshape to do this.
outdata = []
for row in range(rows):
	rowdata = []
	for col in range(cols):
		rowdata.append(out3d[row][col][0])
		rowdata.append(out3d[row][col][1])
		rowdata.append(out3d[row][col][2])
		rowdata.append(out3d[row][col][3])
	outdata.append(rowdata)


f = open('output.png', 'wb')
w = png.Writer(cols, rows, bitdepth=8, alpha=True)
w.write(f, outdata)
f.close()

os.system('open output.png')

