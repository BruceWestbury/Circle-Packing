#*****************************************************************************
#       Copyright (C) 2013 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from numbers import Real
from math import sqrt, pi, cos, sin, acos, cosh, sinh

class Triangle(object):
    """An abstract class for triangles."""

    def __init__(self, rrad, srad, trad):
        self.check(rrad)
        self.check(srad)
        self.check(trad)

        self.r = rrad
        self.s = srad
        self.t = trad

    def __repr__(self):
        return str( (self.r, self.s, self.t,) )

    def __eq__(self, other):
        return self.r == other.r  and self.s == other.s and self.t == other.t \
               and type(self) == type(other)

    def check(self, a):
        if not isinstance(a,Real):
            raise ValueError, "%s must be a real number" % a
        if a < 0:
            raise ValueError, "%s must be positive" % a

    def cosine_rule(self, u, v, w):
        raise RuntimeError, "Not yet implemented."

    def area(self):
        raise RuntimeError, "Not yet implemented."

    def angles(self):
        return \
              (self.cosine_rule(self.r, self.s, self.t), \
               self.cosine_rule(self.t, self.r, self.s), \
               self.cosine_rule(self.t, self.r, self.s),)

    def place(self, u, v):
        raise RuntimeError, "Not yet implemented."


class Hyperbolic(Triangle):
    """The class for hyperbolic triangles."""

    def __init__(self, rrad, srad, trad):
        if rrad != None:
            self.check(rrad)
        if srad != None:
            self.check(srad)
        if trad != None:
            self.check(trad)

        self.r = rrad
        self.s = srad
        self.t = trad

    def cosine_rule(self, u, v, w):
        """Implements the hyperbolic cosine rule.

        http://en.wikipedia.org/wiki/Hyperbolic_law_of_cosines
        """

        if u == None:
            return 0
        elif v == None and w == None:
            return acos( 1-2*exp(2*u) )
        elif v != None and w == None:
            num = cosh(u+v)-exp(v-u)
            den = sinh(u+v)
            return acos( num/den )
        elif v == None and w != None:
            num = cosh(u+w)-exp(w-u)
            den = sinh(u+w)
            return acos( num/den )
        elif v != None and w != None:
            a = v+w; b = u+v; c = u+w
            num = cosh(b)*cosh(c) - cos(a)
            den = sinh(b)*sinh(c)
            return acos( num/den )
        else
            raise RuntimeError, "This can't happen."

    def area(self):
        return pi - sum( self.angles() )

    def place(self, u, v):
        raise RuntimeError, "Not yet implemented."


class Parabolic(Triangle):
    """The class for Euclidean triangles."""

    def cosine_rule(self, u, v, w):
        """Implements the Euclidean cosine rule.

        http://en.wikipedia.org/wiki/Law_of_cosines
        """
        x = u*(u+v+w)
        y = v*w
        return acos( (x-y)/(x+y) )

    def area(self):
        """Calculates the area using Herron's formula.

        http://en.wikipedia.org/wiki/Triangle
        """
        s = ( self.r + self.s + self.t )/2
        return sqrt( s*(s-self.r)*(s-self.s)*(s-self.t)

    def place(self, u, v):
        raise RuntimeError, "Not yet implemented."


class Elliptic(Triangle):
    """The class for spherical triangles."""

    def __init__(self, rrad, srad, trad):
        self.check(rrad)
        self.check(srad)
        self.check(trad)
        if rrad + srad + trad > pi:
            raise ValueError, "Angle sum is too large"

        self.r = rrad
        self.s = srad
        self.t = trad

    def cosine_rule(self, u, v, w):
        """Implements the spherical cosine rule.

        http://en.wikipedia.org/wiki/Law_of_cosines

        Maybe this should use the haversine formula instead?
        
        http://en.wikipedia.org/wiki/Great-circle_distance
        """

        a = v+w; b = u+v; c = u+w
        num = cos(a) - cos(b)*cos(c)
        den = sin(b)*sin(c)
        return acos( num/den )

    def area(self):
        return sum( self.angles() ) - pi

    def place(self, u, v):
        raise RuntimeError, "Not yet implemented."



# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()
