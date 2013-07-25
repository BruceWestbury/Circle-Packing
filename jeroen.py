
#*****************************************************************************
#       Copyright (C) 2013 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

"""These are examples of genus zero constellations."""

import constellation

"""These permutations generate the Mathieu group M23."""
s = [ 11, 7, 19, 12, 4, 14, 10, 1, 3, 2, 0, 6, 13, 8, 22, 21, 16, 17, 9, 18, 5, 15,
20 ]
a = [ 22, 15, 9, 12, 6, 4, 16, 19, 13, 0, 10, 14, 3, 11, 8, 1, 5, 18, 7, 17, 20, 21,
2 ]
p = [ 18, 21, 14, 3, 20, 16, 4, 19, 5, 9, 6, 12, 8, 13, 0, 7, 11, 2, 17, 1, 22, 15,
10 ]
m23 = constellation.HyperMap(s,a,p)
#print "Trying Mathieu"
#m23.show('SVG',name='Mathieu 23')

"""These permutations generate the Mathieu group PSU3(5)."""
s = [ 15, 49, 9, 8, 18, 35, 29, 7, 3, 2, 32, 13, 21, 11, 47, 0, 16, 22, 4, 36, 34,
12, 17, 42, 30, 40, 26, 39, 28, 6, 24, 38, 10, 41, 20, 5, 19, 44, 31, 27, 25,
33, 23, 43, 37, 45, 48, 14, 46, 1 ]

a = [ 4, 49, 10, 14, 27, 32, 44, 29, 8, 9, 26, 16, 41, 25, 43, 1, 12, 23, 15, 39,
45, 6, 34, 31, 48, 22, 36, 35, 33, 5, 3, 37, 7, 28, 13, 0, 2, 17, 42, 20, 47,
11, 38, 30, 46, 19, 21, 40, 24, 18 ]

p = [ 5, 0, 19, 24, 15, 6, 12, 10, 3, 2, 9, 33, 16, 20, 8, 4, 13, 44, 1, 45, 27, 48,
40, 22, 46, 11, 32, 18, 41, 7, 43, 42, 35, 28, 17, 39, 26, 38, 23, 36, 14, 21,
31, 47, 29, 34, 37, 25, 30, 49 ]

inv = [ 4, 49, 2, 3, 0, 39, 34, 45, 8, 9, 36, 12, 11, 21, 30, 18, 16, 37, 15, 32, 29,
13, 44, 31, 47, 46, 26, 35, 28, 20, 14, 23, 19, 33, 6, 27, 10, 17, 42, 5, 48,
41, 38, 43, 22, 7, 25, 24, 40, 1 ]

mPSU3F5 = constellation.HyperMap(s,a,p,inv)

"""This degree seven permutation representation is a test case."""
s = [1,2,3,4,0,5,6]
a = [5,1,2,3,4,6,0]
p = [6,0,1,2,3,4,5]

test7 = constellation.HyperMap(s,a,p)


s = [ 5, 1, 0, 7, 3, 2, 6, 4, 9, 10, 8, 11 ]
a = [ 0, 7, 2, 1, 5, 6, 10, 11, 8, 9, 4, 3 ]
p = [ 2, 4, 5, 11, 9, 7, 0, 1, 10, 8, 6, 3 ]

inv = [ 8, 1, 9, 7, 4, 10, 6, 3, 0, 2, 5, 11 ]

m12 = constellation.HyperMap(s,a,p,inv)

s = [ 3, 1, 7, 0, 8, 5, 6, 2, 4, 10, 9 ]
a = [ 0, 4, 1, 10, 6, 8, 2, 7, 3, 9, 5 ]
p = [ 3, 7, 6, 4, 1, 9, 8, 2, 5, 10, 0 ]

inv = [ 3, 1, 9, 0, 10, 11, 6, 7, 8, 2, 4 ]

m11 = constellation.HyperMap(s,a,p,inv)

s = [ 0, 1, 20, 8, 16, 5, 7, 6, 3, 11, 17, 9, 12, 13, 14, 15, 4, 10, 19, 18, 2 ]
a = [ 14, 17, 12, 9, 7, 3, 2, 13, 8, 19, 4, 11, 18, 10, 1, 20, 16, 0, 6, 5, 15 ]
p = [ 10, 14, 7, 5, 17, 18, 19, 16, 3, 8, 13, 9, 20, 6, 0, 2, 4, 1, 12, 11, 15 ]

mystery = constellation.HyperMap(s,a,p)
