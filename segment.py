#!/usr/bin/env python

class segment(object):
    """A class for segments of lines in the complex plane.

    EXAMPLES:

    >>> segment(complex(0,0),complex(0,1))
    0j ---> 1j

    """

    def __init__(self,u,v):
        t = type(complex(0,0))
        if type(u) != t or type(v) != t:
            raise ValueError, "Arguments must be complex numbers."
        self.u = u
        self.v = v

    def __repr__(self):
        return '%s ---> %s' %(self.u, self.v)

    def __eq__(self, other):
        return self.u == other.u and self.v == other.v

    def length(self):
        """Returns the length of the segment.

        EXAMPLES:

        >>> segment(complex(0,0),complex(0,1)).length()
        1.0

        """
        return abs(self.u - self.v)

    def reverse(self):
        """Reverses the direction of a segment.

        EXAMPLES:

        >>> segment(complex(0,0),complex(0,1)).reverse()

        """
        return segment(self.v, self.u)

    def intersects(self, other):
        """Returns True if two segments intersect internally.

        EXAMPLES:
        >>> a = segment(complex(0,-1),complex(0,1))
        >>> b = segment(complex(-1,0),complex(1,0))
        >>> a.intersects(b)
        True

        """
        ao = triangle( self.v, other.u, other.v ).clockwise() != \
             triangle( self.u, other.u, other.v ).clockwise()
        ac = triangle( self.u,  self.v, other.v ).clockwise() != \
             triangle( self.u,  self.v, other.u ).clockwise()
        return ao and ac

    def intersection(self, other):
        """Returns the intersection of the lines defined by the two segments.

        EXAMPLES:
        >>> a = segment(complex(0,-1),complex(0,1))
        >>> b = segment(complex(-1,0),complex(1,0))
        >>> a.intersection(b)
        (-0-0j)


        """
        den = (self.u.real-self.v.real)*(other.u.imag-other.v.imag)-\
              (self.u.imag-self.v.imag)*(other.u.real-other.v.real)
        if abs(den) < 0.001:
            return ValueError, "Lines are too close to parallel."
        x = self.u.real*self.v.imag-self.u.imag*self.v.real
        y = other.u.real*other.v.imag-other.u.imag*other.v.real
        nx = x*(other.u.real-other.v.real)-y*(self.u.real-self.v.real)
        ny = x*(other.u.imag-other.v.imag)-y*(self.u.imag-self.v.imag)
        return complex(nx/den, ny/den)

class triangle(object):
    """A class for triangles in the complex plane.

    EXAMPLES:

    >>> triangle(complex(0,0),complex(0,1), complex(1,0) )
    [0j, 1j, (1+0j)]

    """

    def __init__(self,u,v,w):
        t = type(complex(0,0))
        if type(u) != t or type(v) != t or type(w) != t:
            raise ValueError, "Arguments must be complex numbers."
        self.u = u
        self.v = v
        self.w = w

    def __repr__(self):
        return str([self.u, self.v, self.w])

    def __eq__(self, other):
        return self.u == other.u and self.v == other.v and self.w == other.w

    def area(self):
        """Twice the signed area of a triangle in the complex plane.
        EXAMPLES:

        >>> triangle(complex(0,0),complex(0,1), complex(1,0) ).area()
        -1.0

        """
        return (self.w.imag-self.u.imag)*(self.v.real-self.u.real)-\
                 (self.w.real-self.u.real)*(self.v.imag-self.u.imag)

    def clockwise(self):
        """Returns True if oriented clockwise
        and False if oriented anticlockwise.

        EXAMPLES:

        >>> triangle(complex(0,0),complex(0,1), complex(1,0) ).clockwise()
        False

        """
        return self.area < 0

    def inside(self,z):
        """Returns True if the point z is inside the triangle self.

        EXAMPLES:

        >>> triangle(complex(0,0),complex(0,1), complex(1,0) ).inside(complex(2,0))
        False

        """
        return triangle(self.u, self.v, z).clockwise() \
               and triangle(self.v, self.w, z).clockwise() \
               and triangle(self.w, self.u, z).clockwise()


# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()

