
#*****************************************************************************
#       Copyright (C) 2010 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

# This code was built and tested with Windows 7 and Python 2.7

"""
Implementation of ribbon graphs. A closed ribbon graph is a finite set with a
fixed point free involution and a bijection. A graph embedded in an oriented
surface gives a ribbon graph by taking the set of pairs consisting of a vertex
in an edge. More intuitively put a bead on one end of an edge. Then there are
two operations that move the bead: one is to move the bead to the other end of
the edge; the other is to move the bead around the vertex in a clockwise sense.

Conversely a closed ribbon graph has a geometric realisation as a graph embedded
in an oriented surface. This embedding has the property that every connected
component of the complement of the graph is an open disk. If we also draw the
dual graph then we have a tiling of the surface by quadrilaterals.

This is implemented as a pair consisting of a set of half edges with a subset
consisting of the half edges in the boundary. The complement of the boundary
is the set of internal half edges. The function c is a bijection on the set
of half edges and the function e is an involution on the set of internal half
edges.

AUTHOR:
Bruce Westbury (2010-09-01): initial version

"""

#from collections import deque
from collections import namedtuple
from operator import countOf


Features = namedtuple('Features',['directed','colour','over'])

vanilla = Features('neither','red',True)

# class halfedge(SageObject):
class halfedge(object):
    """
    The class whose instances are half edges in a ribbon graph.
    """
    __slots__ = ('c', 'e', 'IsI', 'decorations')
    def __init__(self,decorations=vanilla):
        self.c = None
        self.e = None
        self.IsI = False
        self.decorations = decorations

    def _repr_(self):
        return str(id(self))

    @property
    def anti(self):
        s, t = self, self.c
        while t != self:
            s, t = t, t.c
        return s

class justgraph():
    """A class for a set of half edges."""

    def __init__(self,he):
        if { a.c for a in he } != set(he):
            raise ValueError("c is not a bijection.")
        if any( a.e not in he for a in he if a.e != None ):
            raise ValueError("e is inconsistent.")
        if any( a.e.e != a for a in he if a.e != None ):
            raise ValueError("e is not an involution.")
        if any( a.e == a for a in he if a.e != None ):
            raise ValueError("e has a fixed point.")

        self.he = set(he)

    def _repr_(self):
        s = len(self)
        t = len( a for a in self.he if a.e == None )
        return 'A justgraph with %d boundary half edges and\
                    %d internal half edges.' % (t,s-t)

    def is_closed(self):
        """Determines if the graph is closed.

        INPUT: None

        OUTPUT: A boolean

        TESTS:

        >>> f = justgraph.vertex(3)
        >>> f.is_closed()
        False
        >>> join(f,f,f,he,f.he).is_closed()
        True
        """

        return all( a.e != None for a in self.he)

    def dual(self):
        """Finds the dual of a closed graph.

        INPUT: None

        OUTPUT: A justgraph

        TESTS:

        >>> justgraph.vertex(3).dual()
        (<type 'exceptions.ValueError'>, 'The graph must be closed.')

        >>> f = vertex(4)
        >>> g = polygon(4)
        >>> join(f,g,f.he,g.he).dual() #doctest: +ELLIPSIS
        <__main__.justgraph instance at 0x...>

        >>> f = vertex(3)
        >>> g = polygon(3)
        >>> tetrahedron = join(f,g,f.he,g.he)
        >>> tetrahedron.dual() == tetrahedron
        True             
        """
        if not self.is_closed():
            return ValueError, 'The graph must be closed.'
        flags = dict([])
        for a in self.he:
            flags[a] = halfedge()
        for a in self.he:
            flags[a].e = flags[a.e]
            flags[a.e].c = flags[a.c]
        g = justgraph(flags.values())
        return g, flags
        
    @staticmethod
    def vertex(n):
        """
        Constructs a single vertex of valency n.

        INPUT:
        A positive integer n, at least 1.

        OUTPUT:
        A set of half edges.

        This is the basic construction.

        TESTS:

        >>> [ isinstance(a,halfedge) for a in justgraph.vertex(3).he ]
        [True, True, True]

        """

        if not n > 0:
            raise ValueError, "%n must be a positive integer." % n
        a = [ halfedge() for i in xrange(n) ]
        for i in xrange(n):
            a[i-1].c = a[i]

        return justgraph(a)

    @staticmethod
    def line():
        """Constructs a superfluous vertex of valency two.

        INPUT:
        None.

        OUTPUT:
        A justgraph with two half edges.

        This is not intended for use by the user.

        TESTS:

        >>> justgraph.line() #doctest: +ELLIPSIS
        <__main__.justgraph instance at 0x...>

        >>> [ isinstance(a,halfedge) for a in justgraph.line().he ]
        [True, True]

        """

        he = justgraph.vertex(2).he
        for a in he:
            a.IsI = True
        return justgraph(he)

    @staticmethod
    def polygon(n):
        """
        This constructs a polygon with n sides.

        INPUT:
        A positive integer n, at least 1.

        OUTPUT:
        A justgraph with 3n half edges.

        This function has been provided for convenience and for
        use in the documentation testing.


        EXAMPLE:

        >>> justgraph.polygon(4) #doctest: +ELLIPSIS
        <__main__.justgraph instance at 0x...>

        """

        if not n > 0:
            raise ValueError, "%n must be a positive integer." % n
        a =  [ halfedge() for i in xrange(n) ]
        b1 = [ halfedge() for i in xrange(n) ]
        b2 = [ halfedge() for i in xrange(n) ]
        for i in xrange(n):
            b1[i-1].e = b2[i]
            b2[i].e = b1[i-1]
            a[i].c = b1[i]
            b1[i].c = b2[i]
            b2[i].c = a[i]
        return justgraph(a+b1+b2)

    def normal(self):
        """A normalisation. Removes superfluous vertices.

        Note that the set of half edges is modified in place.

        INPUT: A set of half edges.

        OUTPUT: A set of half edges.

        EXAMPLE:

        >>> justgraph.polygon(4).normal()
        >>>

        """

        he = self.he
        flag = True
        while flag:
            flag = False
            r = [ a for a in he if a.IsI and a.e != None ]
            if r != []:
                x = r[0]; y = x.c
                if y.e != None  and x.e != y:
                    flag = True
                    x.e.e = y.e
                    y.e.e = x.e
                    he.discard(x)
                    he.discard(y)
                elif y.e == None:
                    flag = True
                    z = x.e
                    y.c = z.c
                    z.anti.c = y
                    y.IsI = z.IsI
                    he.discard(x)
                    he.discard(z)

    def copy(self):
        """Makes a deepcopy with the identification.

        INPUT: A justgraph

        OUTPUT: An embedding.

        Without the identification this could probably be replaced
        by copy.deepcopy(self)


        EXAMPLE:

        >>> justgraph.polygon(5).copy() #doctest: +ELLIPSIS
        <__main__.Embedding instance at 0x...>

        """
        he = self.he
        D = dict()
        for a in he:
            D[a] = halfedge()
        for a in he:
            D[a].c = D[a.c]
            if a.e != None:
                D[a].e = D[a.e]
            D[a].IsI = a.IsI
            D[a].decorations = a.decorations
        h = justgraph(D.values())
        return Embedding(D,self,h)


    def is_connected(self):
        """Tests if graph is connected.

        INPUT: None

        OUTPUT: A Boolean

        EXAMPLE:

        >>> justgraph.polygon(4).is_connected()
        True

        """
        he = self.he
        if he == {}:
            return True
        r = [ a for a in he if a.e == None ]
        if r == []:
            return False
        return set( self.get_bd(r[0]) ) == set(r)

    # This gives a method for extracting the components.
    def get_bd(self,x=None):
        """
        Gets the list of boundary points in the component of x.

        INPUT: A justgraph and an element.

        OUTPUT: A list of halfedges.

        EXAMPLE:

        >>> f=justgraph.polygon(5)
        >>> len(f.get_bd())
        5

        """

        if x != None and not x in self.he:
            raise ValueError, "%s must be an element of %s", %(x,self)
        if x != None and x.e != None:
            raise ValueError, "%s must be in the boundary of %s", %(x,self)
        if x == None:
            r = [ a for a in self.he if a.e == None ]
            if r == []:
                return []
            else:
                x = r[0]

        def adjacent(x):
            if not x in self.he:
                raise ValueError
            if x.e != None:
                raise ValueError
            s = x.c
            while True:
                if s.e == None:
                    return s
                else:
                    s = s.e.c

        b = [x]
        s, t = x, adjacent(x)
        while t != x:
            b.append(t)
            s, t = t, adjacent(t)
        return b

    def subdivision(self):
        """Medial subdivision."""
        labels = ('O','E','A','B',)
        flags = dict([])
        for l in labels:
            for x in self.he:
                flags[(x,l,)] = halfedge()

        for x in self.he:
            flags[(x,'O',)].e = flags[(x,'E',)]
            flags[(x,'E',)].e = flags[(x,'O',)]
            flags[(x,'A',)].e = flags[(x.c,'B',)]
            flags[(x.c,'B',)].e = flags[(x,'A',)]

            flags[(x,'O',)].c = flags[(x.c,'O',)]
            flags[(x,'E',)].c = flags[(x,'B',)]
            flags[(x,'A',)].c = flags[(x,'E',)]
            flags[(x,'B',)].c = flags[(x.e,'A',)]

        for x in self.he:
            flags[(x,'O',)].decorations = x.decorations
            flags[(x,'E',)].decorations = x.decorations
            flags[(x,'A',)].decorations = Features('neither','None',True)
            flags[(x,'B',)].decorations = Features('neither','None',True)

        g = justgraph(set(flags.values()))
        inc = {x: flags[(x,'O',)] for x in self.he}
            
        return g, inc

    def inspect(self):
        """Gives basic information on a closed graph.
        """
        if not self.is_closed():
            return ValueError, 'The graph must be closed.'

        vs = [ len(a) for a in self.get_orbits(lambda a: a.c) ]
        es = [ len(a) for a in self.get_orbits(lambda a: a.e) ]
        fs = [ len(a) for a in self.get_orbits(lambda a: a.e.c) ] 
        print 'Vertices', vs
        print 'Edges',    es
        print 'Faces',    fs
        print 'Euler characteristic', len(vs)-len(es)+len(fs)

        
    @property
    def vertices(self):
        """Get the vertices of a justgraph.

        INPUT: A justgraph

        OUTPUT: A list of lists of halfedges

        EXAMPLE:

        >>> len(justgraph.polygon(5).vertices)
        5

        >>> [ len(a) for a in justgraph.polygon(4).vertices ]
        [3, 3, 3, 3]

        """
        return self.get_orbits(lambda a: a.c)

    def count_vertices(self):
        """Counts the numbers of vertices of each valency in a justgraph.

        INPUT: A justgraph

        OUTPUT: A list of non-negative integers

        Note that the first entry in the list is the number of vertices of
        valency zero and so will always be zero. The second entry is the
        number of vertices of valency one and so will almost always be zero.
        The last entry is the number of vertices of maximum valency.

        EXAMPLES:

        >>> justgraph.polygon(4).count_vertices()
        [0, 0, 0, 4]

        >>> f=justgraph.vertex(4)
        >>> g=justgraph.vertex(3)
        >>> r=f.get_bd()[:2]
        >>> s=g.get_bd()[:2]
        >>> h=join(f,g,r,s)
        >>> h.count_vertices()
        [0, 0, 0, 1, 1]

        """
        v = [ len(a) for a in self.vertices ]
        #return [ len([ 0 for a in v if a == i ]) for i in range(max(v)+1) ]
        return [ countOf(v,i) for i in range(max(v)+1) ]


    def get_orbits(self,m):
        """Get the orbits of a bijection on the halfedges of a justgraph.

        INPUT: A justgraph and a bijection

        OUTPUT: A list of lists of halfedges

        EXAMPLE:

        >>> g=justgraph.polygon(4)
        >>> go = g.get_orbits(lambda a: a.c)
        >>> gv = g.vertices
        >>> ao = [ frozenset(a) for a in go]
        >>> av = [ frozenset(a) for a in gv]
        >>> set(ao) == set(av)
        True

        """
        phi = self.copy()
        h = phi.codomain.he
        inv = dict([ [phi.map[a], a] for a in phi.map ])
        orbits = []
        while h != set():
            s = h.pop()
            v = [inv[s]]
            while m(s) in h:
                t = m(s)
                v.append(inv[t])
                h.remove(t)
                s = t
            orbits.append(tuple(v))

        return orbits

        #D = dict()
        #for x in orbits:
            #for a in x:
                #D[a] = frozenset(x)
        #return D


    def stitch(self,x,y):
        if x.e != None:
            raise ValueError('Not a boundary halfedge')
        if y.e != None:
            raise ValueError('Not a boundary halfedge')
        if x.decorations.colour != y.decorations.colour:
            raise ValueError('Colours do not match.')
        dx = x.decorations.directed
        dy = y.decorations.directed
        allowed = [ ('neither','neither'), ('head','tail'), ('tail','head') ]
        if not (dx,dy) in allowed:
            raise ValueError('Directions do not match.')
        ln = list(justgraph.line().he)
        he = self.he.union(set(ln))
        u = ln[0]
        v = ln[1]
        x.e, u.e = u, x
        y.e, v.e = v, y
        a = Features(y.decorations.directed, x.decorations.colour, True)
        u.decorations = a
        a = Features(x.decorations.directed, y.decorations.colour, True)
        v.decorations = a
        self.he = he

# End of class definition

def join(f, g, r, s):
    """The join operation.

    INPUT:

    - r is a subset of the boundary of f
    - s is a subset of the boundary of g

    r, s are lists of the same length

    OUTPUT: A just graph

    EXAMPLE:

    >>> f=justgraph.vertex(4)
    >>> g=justgraph.vertex(3)
    >>> r=f.get_bd()[:2]
    >>> s=g.get_bd()[:2]
    >>> join(f,g,r,s) #doctest: +ELLIPSIS
    <__main__.justgraph instance at 0...>

    """
    if not set(r).issubset(f.he):
        raise ValueError
    if not set(s).issubset(g.he):
        raise ValueError
    if not len(r) == len(s):
        raise ValueError

    ps = f.copy()
    po = g.copy()
    hs = ps.codomain.he
    ho = po.codomain.he
    jg = justgraph(hs.union(ho))

    for x, y in zip(r,s):
        jg.stitch(ps.map[x], po.map[y])
    jg.normal()
    return jg



# This looks better but I need to figure out how to check
# the data passes the tests in OldEmbedding
#Embedding = namedtuple('Embedding',['map','domain','codomain'])

# In fact the domain is redundant as we have
# map.keys() = domain.he. Also map.items() is a subset of codomain.he
# but may be a proper subset.
class Embedding():
    """ A class for embeddings of ribbon graphs."""

    def __init__(self,D,f,g):
        he = f.he
        if set(D.keys()) != he:
            raise ValueError
        if len(set(D.values())) != len(D):
            raise ValueError
        for a in he:
            if D[a.c] != D[a].c:
                raise ValueError
        for a in he:
            if a.e != None:
                if D[a].e != None and D[a.e] != None:
                    if D[a.e] != D[a].e:
                        raise ValueError
        for a in he:
            if D[a].IsI != a.IsI:
                raise ValueError

        self.domain = f
        self.codomain = g
        self.map = D

    def show(self):
        pass


# This could be speeded up by only checking new entries at each pass.
# Use search(g,g) to construct the set of automorphisms of g
def search(h,g,u=None):
    """
    Searches for embeddings of h in g. This requires h is connected.

    INPUT: A pair of ribbon graphs.

    OUTPUT: A list of embeddings.

    EXAMPLE:

    >>> h=justgraph.vertex(3)
    >>> g=justgraph.polygon(4)
    >>> len(search(h,g))
    12

    """
    if u != None and not u in h.fe:
        raise ValueError
    if not h.is_connected():
        raise ValueError

    # If we did not require a boundary point we could use
    # u = h.fe.pop(), he.fe.add(u)
    if u == None:
        r = [ a for a in h.he if a.e == None ]
        if r == []: # Is this necessary?
            raise ValueError
        else:
            u = r[0]

    def test(x):
        D[u] = x
        flag = True
        while flag:
            flag = False
            newD = dict()
            for a in D:
                while not a.c in D:
                    if a in D:
                        newD[a.c] = D[a].c
                    elif a in newD:
                        newD[a.c] = newD[a].c
                    a = a.c
            for a in D:
                if a.e != None and not a.e in D:
                    newD[a.e] = D[a].e
            if len(newD) != 0:
                if any( a.decorations != newD[a].decorations for a in newD ):
                    return False
                D.update(newD)
                flag = True
            for a in D:
                if D[a].IsI != a.IsI:
                    return False
                if a.c in D:
                    if D[a.c] != D[a].c:
                        return False
                if a.e in D:
                    if D[a.e] != D[a].e:
                        return False
        if len(set(D.values())) != len(D):
            return False
        return True
    output = []
    for x in g.he:
        D = dict()
        if test(x):
            output.append(Embedding(D, h, g))
    return output


def overlaps(f,g):
    """Finds overlaps between two justgraphs.

    INPUT: Two justgraphs

    OUTPUT: A list of dictionaries

    """

    if not f.is_connected():
        raise ValueError
    if not g.is_connected():
        raise ValueError

    def test():
        for a in D:
            if a.decorations != D[a].decorations:
                return False
            if a.IsI != D[a].IsI:
                return False

        flag = True
        while flag:
            flag = False
            newD = dict()
            for a in D:
                while not a.c in D:
                    if a in D:
                        newD[a.c] = D[a].c
                    elif a in newD:
                        newD[a.c] = newD[a].c
                    a = a.c
            for a in D:
                if a.e != None and not a.e in D:
                    if D[a].e != None:
                        newD[a.e] = D[a].e
            if len(newD) != 0:
                if any( a.decorations != newD[a].decorations for a in newD ):
                    return False
                D.update(newD)
                flag = True
            for a in D:
                if D[a].IsI != a.IsI:
                    return False
                if a.c in D:
                    if D[a.c] != D[a].c:
                        return False
                if a.e in D:
                    if D[a.e] != D[a].e:
                        return False
        if len(set(D.values())) != len(D):
            return False
        return True


    output = []
    vf = f.get_orbits(lambda a: a.c)
    vg = g.get_orbits(lambda a: a.c)
    for uf in vf:
        n = len(v)
        for ug in [ u for u in vg if len(u) == n ]:
            D = dict()
            for i in xrange(n):
                D[uf[i]] = ug[i]
            if test():
                output.append(D)
    return D



# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()


