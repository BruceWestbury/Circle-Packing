#!/usr/bin/env python

#   Copyright (C) 2011 Bruce Westbury

#   This is based on:

#   Copyright (C) 2007-2009 Marc Culler, Nathan Dunfield and others.
#
#   This program is distributed under the terms of the
#   GNU General Public License, version 2 or later, as published by
#   the Free Software Foundation.  See the file gpl-2.0.txt for details.
#   The URL for this program is
#     http://www.math.uic.edu/~t3m/plink
#   A copy of the license file may be found at:
#     http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#
#   The development of this program was partially supported by
#   the National Science Foundation under grants DMS0608567,
#   DMS0504975 and DMS0204142.


from math import sqrt

class StickDiagram(object):

    def __init__(self, Vertices, Arrows, Crossings):
        self.Vertices = Vertices
        self.Arrows = Arrows
        self.Crossings = Crossings

    def draw(self, canvas):
        pass

    def from_Graph(self):
        pass

    def edit(self):
        pass
    
#######################################################################

class Vertex:
    """
    A vertex in a PL link diagram.
    """
    epsilon = 6

    def __init__(self, x, y):
        self.x, self.y = int(x), int(y)
        self.in_arrow = None
        self.out_arrow = None
        
    def __repr__(self):
        return '(%d,%d)'%(self.x, self.y)

    def __eq__(self, other):
        """
        Vertices are equivalent if they are sufficiently close.
        Use the "is" operator to test if they are identical.
        """
        return abs(self.x - other.x) + abs(self.y - other.y) < Vertex.epsilon

    def point(self):
        return self.x, self.y

    def is_endpoint(self):
        return self.in_arrow == None or self.out_arrow == None

    def is_isolated(self):
        return self.in_arrow == None and self.out_arrow == None

    def reverse(self):
        self.in_arrow, self.out_arrow = self.out_arrow, self.in_arrow

    def swallow(self, other, palette):
        """
        Join two paths.  Self and other must be endpoints. Other is erased.
        """
        if not self.is_endpoint() or not other.is_endpoint():
            raise ValueError
        if self.in_arrow is not None:
            if other.in_arrow is not None:
                other.reverse_path()
            self.out_arrow = other.out_arrow
            self.out_arrow.set_start(self)
        elif self.out_arrow is not None:
            if other.out_arrow is not None:
                other.reverse_path()
            self.in_arrow = other.in_arrow
            self.in_arrow.set_end(self)
        other.erase()

    def reverse_path(self, crossings=[]):
        """
        Reverse all vertices and arrows of this vertex's component.
        """
        v = self
        while True:
            e = v.in_arrow
            v.reverse()
            if not e:
                break
            e.reverse(crossings)
            v = e.end
            if v == self:
                return
        self.reverse()
        v = self
        while True:
            e = v.out_arrow
            v.reverse()
            if not e:
                break
            e.reverse(crossings)
            v = e.start
            if v == self:
                return

    def update_arrows(self):
        if self.in_arrow:
            self.in_arrow.vectorize()
        if self.out_arrow:
            self.out_arrow.vectorize()

    def erase(self):
        """
        Prepare the vertex for the garbage collector.
        """
        self.in_arrow = None
        self.out_arrow = None
        
################################################################################

class Arrow:
    """
    An arrow in a PL link diagram.
    """
    epsilon = 12

    def __init__(self, start, end):
        self.start, self.end = start, end
        self.lines = []
        self.cross_params = []
        if self.start != self.end:
            self.start.out_arrow = self
            self.end.in_arrow = self
            self.vectorize()

    def __repr__(self):
        return '%s-->%s'%(self.start, self.end)

    def __xor__(self, other):
        """
        Returns the barycentric coordinate at which self crosses other.

        This is called as self ^ other 
        """
        D = float(other.dx*self.dy - self.dx*other.dy)
        if D == 0:
            return None
        xx = other.start.x - self.start.x
        yy = other.start.y - self.start.y
        s = (yy*self.dx - xx*self.dy)/D
        t = (yy*other.dx - xx*other.dy)/D
        if 0 < s < 1 and 0 < t < 1:
            return t
        else:
            return None

    def vectorize(self):
        self.dx = float(self.end.x - self.start.x)
        self.dy = float(self.end.y - self.start.y)
        self.length = sqrt(self.dx*self.dx + self.dy*self.dy)

    def reverse(self, crossings=[]):
        self.end, self.start = self.start, self.end
        self.vectorize()

    def draw(self, crossings=[], recurse=True):
        if self.hidden or self.frozen:
            return
        self.vectorize()
        gap = 9.0/self.length
        for line in self.lines:
            self.canvas.delete(line)
        self.lines = []
        cross_params = []
        over_arrows = [c.over for c in crossings if c.under == self]
        for arrow in over_arrows:
            t = self ^ arrow
            if t:
                cross_params.append(t)
        cross_params.sort()
        x0, y0 = x00, y00 = self.start.point()
        for s in cross_params:
            x1 = x00 + (s-gap)*self.dx
            y1 = y00 + (s-gap)*self.dy
            self.lines.append(self.canvas.create_line(
                    x0, y0, x1, y1,
                    width=3, fill=self.color))
            x0, y0 = x1 + 2*gap*self.dx, y1 + 2*gap*self.dy
        x1, y1 = self.end.point()
        self.lines.append(self.canvas.create_line(
                x0, y0, x1, y1,
                arrow=Tk_.LAST,
                width=3, fill=self.color))
        if recurse:
            under_arrows = [c.under for c in crossings if c.over == self]
            for arrow in under_arrows:
                arrow.draw(crossings, recurse=False)

    def set_start(self, vertex, crossings=[]):
        self.start = vertex
        if self.end:
            self.vectorize()
            self.draw(crossings)

    def set_end(self, vertex, crossings=[]):
        self.end = vertex
        if self.start:
            self.vectorize()
            self.draw(crossings)

    def erase(self):
        """
        Prepare the arrow for the garbage collector.
        """
        self.start = None
        self.end = None

    def too_close(self, vertex):
        if vertex == self.start or vertex == self.end:
            return False
        try:
            e = Arrow.epsilon
            Dx = vertex.x - self.start.x
            Dy = vertex.y - self.start.y
            comp1 = (Dx*self.dx + Dy*self.dy)/self.length
            comp2 = (Dy*self.dx - Dx*self.dy)/self.length
            return -e < comp1 < self.length + e and -e < comp2 < e
        except:
            #print vertex
            return False

###############################################################################

class Crossing:
    """
    A pair of crossing arrows in a PL link diagram.
    """
    def __init__(self, over, under):
        self.over = over
        self.under = under
        self.locked = False
        self.KLP = {}    # See the SnapPea file link_projection.h
        self.hit1 = None # For computing DT codes
        self.hit2 = None

    def __repr__(self):
        return '%s over %s at (%d,%d)'%(self.over, self.under, self.x, self.y)

    def __eq__(self, other):
        """
        Crossings are equivalent if they involve the same arrows.
        """
        if self.over in other and self.under in other:
            return True
        else:
            return False

    def __contains__(self, arrow):
        if arrow == None or arrow == self.over or arrow == self.under:
            return True
        else:
            return False

    def locate(self):
        t = self.over ^ self.under
        if t:
            self.x = int(self.over.start.x + t*self.over.dx)
            self.y = int(self.over.start.y + t*self.over.dy)
        else:
            self.x, self.y = None, None

    def sign(self):
        try:
            D = self.under.dx*self.over.dy - self.under.dy*self.over.dx
            if D > 0: return 'RH'
            if D < 0: return 'LH'
        except:
            return 0

    def strand(self, arrow):
        sign = self.sign()
        if arrow not in self:
            return None
        elif ( (arrow == self.over and sign == 'RH') or
               (arrow == self.under and sign =='LH') ):
            return 'X'
        else:
            return 'Y'

    def reverse(self):
        self.over, self.under = self.under, self.over

    def height(self, arrow):
        if arrow == self.under:
            return self.under ^ self.over
        elif arrow == self.over:
            return self.over ^ self.under
        else:
            return None

    def hit(self, count):
        if self.hit1 is None:
            self.hit1 = count
        elif self.hit2 is None:
            self.hit2 = count
        else:
            raise ValueError, 'Too many hits!'

    def clear_hits(self):
        self.hit1, self.hit2 = None, None

###############################################################################

class ECrossing:
    """
    A pair: (Crossing, Arrow), where the Arrow is involved in the Crossing.
    The ECrossings correspond 1-1 with edges of the link diagram.
    """
    def __init__(self, crossing, arrow):
        if arrow not in crossing:
            raise ValueError
        self.crossing = crossing
        self.arrow = arrow
        self.strand = self.crossing.strand(self.arrow)

    def pair(self):
        return (self.crossing, self.arrow)

    def goes_over(self):
        if self.arrow == self.crossing.over:
            return True
        return False
