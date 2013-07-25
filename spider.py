#!/usr/bin/env python

#*****************************************************************************
#       Copyright (C) 2010 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

# This code was built and tested with Windows 7 and Python 2.7

"""
The set of boundary points is cyclically ordered and has a base point.
Equivalently this is a list. This is implemented as an instance of the
type deque.

The function vertex() is the basic construction and the polygon() function
is included for convenience. The functions rotate() and glue() are the basic
operations of a spider. The definition of a spider comes from


`Spiders for rank 2 Lie algebras <http://arxiv.org/abs/q-alg/9712003>`_

The motivation for the definition of a spider was to give a reformulation
of pivotal or spherical categories. There is also a simple modification
which gives a reformulation of planar algberas.

My papers on this subject are:

- `Enumeration of non-positive planar trivalent graphs <http://arxiv.org/abs/math/0507112>`_

- `Invariant tensors for the spin representation of so(7) <http://arxiv.org/abs/math/0601209>`_

- `Confluence Theory for Graphs <http://arxiv.org/abs/math/0609832>`_

- `Recoupling theory for quantum spinors <http://arxiv.org/abs/1007.2579>`_

- `Hurwitz' theorem on composition algebras <http://arxiv.org/abs/1011.6197>`_

- `Web bases for the general linear groups <http://arxiv.org/abs/1011.6542>`_

AUTHOR:
Bruce Westbury (2010-09-01): initial version

"""

__all__ = [ 'RibbonGraph', 'glue' ]

import ribbon
import closedgraph
import spider
import pivotal

from collections import deque
from collections import Iterable


class RibbonGraph(object):
    """The class of mutable ribbon graphs."""

    def __init__(self,h,b):
        """Constructor for ribbon graph.

        INPUT: h a justgraph, b a deque

        OUTPUT: A ribbon graph
        """
        if { a for a in h.he if a.e == None } != set(b):
            raise ValueError
        self.jg = h
        self.bd = deque(b)

    @staticmethod
    def vertex(x):
        """
        Constructs a single vertex of valency n.
        INPUT:
        A positive integer n, at least 1 or a list of features.

        OUTPUT:
        A closed ribbon graph.

        EXAMPLES:

        >>> RibbonGraph.vertex(3) # doctest:+ELLIPSIS
        <__main__.RibbonGraph object at 0x...>

        """

        if isinstance(x, Iterable):
            n = len(x)
        else:
            n = x
        if n<1: raise ValueError("Not enough points.")

        a = [ ribbon.halfedge() for i in xrange(n) ]
        for i in xrange(n-1):
            a[i].c = a[i+1]
        a[n-1].c = a[0]
        if isinstance(x, Iterable):
            for i, r in zip(xrange(n),x):
                if not isinstance(r, ribbon.features):
                    raise ValueError
                a[i].decorations = r

        h = ribbon.justgraph(a)
        return RibbonGraph(h,a)

    @staticmethod
    def line():
        """Constructs a superfluous vertex of valency two."""

        g = RibbonGraph.vertex(2)
        for a in g.jg.he:
            a.IsI = True
        return g

    @staticmethod
    def polygon(n):
        """
        This constructs a polygon with n sides.

        INPUT:
        A positive integer n, at least 1.

        OUTPUT:
        A closed ribbon graph.

        EXAMPLE:

        >>> RibbonGraph.polygon(4) # doctest:+ELLIPSIS
        <__main__.RibbonGraph object at 0x...>
        """

        if n<1: raise ValueError
        a =  [ ribbon.halfedge() for i in xrange(n) ]
        b1 = [ ribbon.halfedge() for i in xrange(n) ]
        b2 = [ ribbon.halfedge() for i in xrange(n) ]
        for i in xrange(n-1):
            b1[i].e = b2[i+1]
            b2[i+1].e = b1[i]
        b1[n-1].e = b2[0]
        b2[0].e = b1[n-1]
        for i in xrange(n):
            a[i].c = b1[i]
            b1[i].c = b2[i]
            b2[i].c = a[i]
        h = ribbon.justgraph(a+b1+b2)
        return RibbonGraph(h,a)

    def rotate(self,n):
        """
        Rotate anticlockwise by n steps.

        INPUT: an integer

        OUTPUT: a ribbon graph

        EXAMPLES:

        >>> RibbonGraph.vertex(4).rotate(3) # doctest:+ELLIPSIS
        <__main__.RibbonGraph object at 0x...>

        """

        g = self.copy()
        g.bd.rotate(n)
        return RibbonGraph(g.jg, g.bd)

    def normal(self):
        """A normalisation. Removes superfluous vertices.
        Modifies the ribbon graph in place.

        INPUT: A ribbon graph

        OUTPUT: None

        Note this modifies the ribbon graph in place.

        EXAMPLE:

        >>> RibbonGraph.vertex(4).normal()


        """

        self.jg.normal()

    def copy(self):
        """Copies a ribbon graph.

        EXAMPLE:

        >>> RibbonGraph.vertex(4).copy() # doctest:+ELLIPSIS
        <__main__.RibbonGraph object at 0x...>

        """
        phi = self.jg.copy()
        h = phi.codomain
        b = [ phi.map[a] for a in self.bd ]
        return RibbonGraph(h,b)

    def show(self,
             geometry = 'Euclidean',
             boundary = 'Neumann',
             bv = None,
             style = 'SVG',
             name = None):
        """Shows the ribbon graph.

        EXAMPLES:

        >>> g = RibbonGraph.vertex(4)


        >>> g = RibbonGraph.polygon(5)

        
        >>> f = RibbonGraph.vertex(4)
        >>> g = RibbonGraph.vertex(3)


        """
        if bv == None:
            bv = [ 1 for a in self.bd ]

        self.closure(bv).show(style, name )

    def morphism(self,n,m):
        """Construct a morphism from a ribbon graph.

        EXAMPLE:

        >>> g=spider.RibbonGraph.polygon(5)
        >>> g.morphism(2,3) # doctest:+ELLIPSIS
        <pivotal.Morphism instance at 0x...>

        """
        if n+m != len(self.bd):
            raise ValueError
        all = list(self.bd)
        do = all[:n]
        co = all[(m-1):]
        co.reverse()
        return pivotal.Morphism(self.jg, do, co)

    def is_connected(self):
        """Tests if a ribbon graph is connected.

        INPUT: None

        OUTPUT: A Boolean

        EXAMPLE:

        >>> RibbonGraph.vertex(4).is_connected()
        True

        """
        return self.jg.get_bd(self.bd[0]) == list(self.bd)

    def closure(self, bv=None):
        """Construct the closure of a web.

        INPUT: A web and a boundary vector.

        OUTPUT: A closed web.

        EXAMPLES:

        >>> RibbonGraph.polygon(5).closure() #doctest: +ELLIPSIS
        <closedgraph.ClosedGraph object at 0x...>

        >>> RibbonGraph.polygon(5).closure().graph.count_vertices()
        [0, 0, 5, 10]

        """
        if bv == None:
            bv = [1] * len(self.bd)
        if sum(bv) != len(self.bd):
            raise ValueError("Boundary vector is not consistent with web.")
        if len(bv) < 3:
            raise ValueError("Not enough corners.")

        C = len(bv)
        B = len(self.bd)

        phi = self.jg.copy()
        he = phi.codomain.he

        rim = ribbon.Features('neither','black',True)
        switch = {'head':'tail','neither':'neither','tail':'head'}
        
        ci = [ ribbon.halfedge() for i in xrange(C) ]
        for a in ci:
            a.decorations = rim
        co = [ ribbon.halfedge() for i in xrange(C) ]
        for a in co:
            a.decorations = rim
        he = he.union(ci+co)
        bi = [ ribbon.halfedge() for i in xrange(B) ]
        for a in bi:
            a.decorations = rim
        bo = [ ribbon.halfedge() for i in xrange(B) ]
        for a in bo:
            a.decorations = rim
        bc = [ ribbon.halfedge() for i in xrange(B) ]
        he = he.union(bi+bo+bc)

        for i in xrange(C):
            ci[i].c = co[i]
            co[i].c = ci[i]

        nb = [ phi.map[a] for a in self.bd ]
        for i in xrange(B):
            bi[i].c = bo[i]
            bo[i].c = bc[i]
            bc[i].c = bi[i]
            bc[i].e = nb[i]
            nb[i].e = bc[i]

        for a in bc:
            f = a.e.decorations
            a.decorations = ribbon.Features(switch[f.directed],f.colour,True)

        p = 0
        for i, a in enumerate(bv):
            r = co[i-1]
            for j in xrange(a):
                bi[p].e = r
                r.e = bi[p]
                r = bo[p]
                p += 1
            r.e = ci[i]
            ci[i].e = r

        ng = ribbon.justgraph(he)

        u = co[0]
        outside = [u]
        s = u.e.c
        while s != u:
            outside.append(s)
            s = s.e.c

        return closedgraph.ClosedGraph(ng, outside)

# End of class definition

def glue(g,h,n):
    """
    Glues two ribbon graphs together.

    INPUT:

    - A ribbon graph
    - A ribbon graph
    - A non-negative integer.

    OUTPUT: A ribbon graph

    >>> f = RibbonGraph.vertex(4)
    >>> g = RibbonGraph.vertex(3)
    >>> glue(f,g,0) #doctest: +ELLIPSIS
    <__main__.RibbonGraph object at 0...>

    """
    if n < 0:
        raise ValueError("Need a non-negative integer.")
    if n > len(g.bd) or n > len(h.bd):
        raise ValueError("Cannot glue this many points.")

    a = g.copy()
    b = h.copy()
    he = a.jg.he.union(b.jg.he)
    jg = ribbon.justgraph(he)

    for i in xrange(n):
        x = a.bd.pop()
        y = b.bd.popleft()
        jg.stitch(x,y)

    return RibbonGraph(jg,list(a.bd)+list(b.bd))

def replace(k,phi):
    """Replace image of map D:h -> g by k

    INPUT: k a ribbon graph, phi an Embedding

    OUTPUT: A ribbon graph.
    """
    h = phi.domain
    g = phi.codomain
    D = phi.map
    mg = copy(g)
    Dg = mg.map
    ng = mg.codomain
    mk = copy(k)
    Dk = mk.map
    nk = mk.codomain

    he = set(union(ng.he,nk.he))

    # This should be stitch
    def join(a,b):
        ln = line()
        he = h.union(ln)
        u, v = ln[0], ln[1]
        a.e, u.e = u, a
        b.e, v.e = v, b
    for s, t in zip(h.bd,k.bd):
        join(Dg[D[s]],Dk[t])
    for u in [ Dg[D[a]] for a in h.he if a.e != None ]:
        he.remove(u)

    if { a.c for a in he } != he:
        raise RuntimeError
    return he

def trees(n):
    """ Constructs a list of planar rooted binary trees with n+2 leaves and
    n trivalent vertices.

    EXAMPLES:

    >>> trees(5)
    
    """
    if not n >= 0:
        raise ValueError

    if n == 0:
        return [ RibbonGraph.line() ]
    if n == 1:
        return [ RibbonGraph.vertex(3) ]

    result = [None] * (n+1)
    result[0] = [ RibbonGraph.line() ]
    result[1] = [ RibbonGraph.vertex(3) ]

    for k in range(2,n+1):
        output = []
        for r in range(k):
            for gf in result[r]:
                for gs in result[k-r-1]:
                    g = glue( gs, RibbonGraph.line(), 0 ).rotate(1)
                    h = glue( gf, g, 1 )
                    output.append( glue( h, RibbonGraph.vertex(3), 2 ) )
        result[k] = output
    return result[n]

# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()


