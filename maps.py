
#*****************************************************************************
#       Copyright (C) 2013 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

# This code was built and tested with Windows 7 and Python 2.7

"""
Implementation of a variation of ribbon graphs.

AUTHOR:
Bruce Westbury (2013): initial version

"""

__all__ = [ 'dart', 'justgraph', 'join', 'Embedding', 'search' ]

#from collections import deque
from collections import namedtuple
from operator import countOf


Features = namedtuple('Features',['directed','colour','over'])

vanilla = Features('neither','red',True)

# class dart(SageObject):
class dart(object):
    """
    The class whose instances are half edges in a ribbon graph.
    """
    __slots__ = ('v', 'f', 'decorations')
    def __init__(self,decorations=vanilla):
        self.v = None
        self.f = None
        self.decorations = decorations

    def _repr_(self):
        return str(id(self))

class justmap():
    """A class for a set of darts. Implemented following a talk in
    Paris by Georges Gonthier in June 2013
    """

    def __init__(self,he):
        he = set(he)
        if any( not isinstance(a,dart) for a in he ):
            raise ValueError, "Must be a set of darts."
        boundary = { a for a in he if a.v == None }
        interior = { a for a in he if a.v != None }

        if { a.v for a in interior } != interior:
            raise ValueError, "Vertex map is not a bijection."

        if any( a.f not in he and a.f != None for a in he ):
            raise ValueError, "Face map is not consistent."

        for a in interior:
            try:
                b = a.v.f.v.f
                if b != a: raise ValueError, "v.f is not an involution."
                if len({a, a.v, a.v.f, a.v.f.v}) != 4:
                    raise ValueError, "Mappings are inconsistent."
            except AttributeError: pass

        self.he = he

    def _repr_(self):
        s = len(self)
        return 'A justgraph with %d edges.' % s
        
    @staticmethod
    def vertex(n):
        """
        Constructs a single vertex of valency n.

        INPUT:
        A positive integer n, at least 1.

        OUTPUT:
        A set of half edges.

        This is the basic construction.

        EXAMPLE:

        >>> #[ isinstance(a,halfedge) for a in justgraph.vertex(3).he ]
        [True, True, True]

        """

        if not n > 1:
            raise ValueError, "%n must be greater then one." % n
        inn = [ dart() for i in xrange(n) ]
        bdi = [ dart() for i in xrange(n) ]
        bdo = [ dart() for i in xrange(n) ]
        for i in xrange(n):
            inn[i-1].v = inn[i]
            inn[i].f = bdo[i]
            bdi[i].f = inn[i]

        he = inn + bdi + bdo
        return justmap(he)

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

        if not n > 1:
            raise ValueError, "%n must be greater then one." % n
        in1 = [ dart() for i in xrange(n) ]
        in2 = [ dart() for i in xrange(n) ]
        in3 = [ dart() for i in xrange(n) ]
        bdi = [ dart() for i in xrange(n) ]
        bdo = [ dart() for i in xrange(n) ]
        for i in xrange(n):
            in1[i].v = in2[i]
            in2[i].v = in3[i]
            in3[i].v = in1[i]
            in3[i-1].f = in3[i]
            bdi[i].f = in1[i]
            in1[i].f = in2[i-1]
            in2[i].f = bdo[i]

        he = inn1 + inn2 + inn3 + bdi + bdo
        return justmap(he)

    def copy(self):
        """Makes a deepcopy with the identification.

        INPUT: A justgraph

        OUTPUT: An embedding.

        Without the identification this could probably be replaced
        by copy.deepcopy(self)


        EXAMPLE:

        >>> f = justgraph.vertex(5).copy()
        >>>

        >>> justgraph.polygon(5).copy() #doctest: +ELLIPSIS
        <__main__.Embedding instance at 0x...>

        """
        he = self.he
        D = dict()
        for a in he:
            D[a] = dart()
        for a in he:
            if a.v != None:
                D[a].v = D[a.v]
            if a.f != None:
                D[a].f = D[a.f]
            D[a].decorations = a.decorations
        h = justmap(D.values())
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
        component = { he.pop() }
        flag = True
        while flag:
            flag = False
            nev = { a.v for a in component if a.v not in component and a.v != None }
            if len(nev) > 0:
                flag = True
                component.update(nev)
            nef = { a.f for a in component if a.f not in component and a.f != None }
            if len(nef) > 0:
                flag = True
                component.update(nef)

        return component == h

    def dual(self):
        D = dict()
        for a in self.he:
            D[a] = dart()
        for a in self.he:
            if a.f != None:
                D[a].v = D[a.f]
            if a.v != None:
                D[a].f = D[a.v]
            D[a].decorations = a.decorations

        return justmap(D.values())

    def reverse(self):
        D = dict()
        for a in self.he:
            D[a] = dart()
            D[a].decorations = a.decorations
        for a in self.he:
            if a.f != None:
                D[a.f].f = D[a]
            if a.v != None:
                D[a.v].v = D[a]

        return justmap(D.values())

    # This is in the wrong file.
    def to_justmap(self):
        """Convert a justgraph to a justmap."""
        D = dict()
        for a in self.he:
            D[a] = dart()
            D[a].decorations = a.decorations
        for a in self.he:
            if a.e == None:
                D[(a.left)] = dart()
                D[(a.left)].decorations = a.decorations
                D[(a.right)] = dart()
                D[(a.right)].decorations = a.decorations
        for a in self.he:
            D[a].v = D[a.c]
            if a.c.e != None:
                D[a.c.e].f = D[a]
        for a in self.he:
            if a.e == None:
                D[(a,left)].f = D[a]
                D[a].f = D[(a,right)]

        return justmap(D.values())

    def to_justgraph(self):
        """Convert a justmap to a justgraph."""
        D = dict()
        for a in self.he:
            if a.v != None:
                D[a] = halfedge()
                D[a].decorations = a.decorations
        for a in self.he:
            if a.v != None:
                D[a].c = D[a.v]
            if a.f != None:
                if a.f.v != None:
                    D[a].e = D[a.f.v]

        return justgraph(D.values())

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
        if any( x.e == None for x in self.he ):
            raise ValueError, 'Only implemented for closed graphs.'

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
        if x.v != None:
            raise ValueError('Not a boundary halfedge')
        if y.v != None:
            raise ValueError('Not a boundary halfedge')
        if x.decorations.colour != y.decorations.colour:
            raise ValueError('Colours do not match.')
        dx = x.decorations.directed
        dy = y.decorations.directed
        allowed = [ ('neither','neither'), ('head','tail'), ('tail','head') ]
        if not (dx,dy) in allowed:
            raise ValueError('Directions do not match.')
        
        u = x.f.v
        u.f = y.f
        u = y.f.v
        u.f = x.f

        self.he.remove(x)
        self.he.remove(x.f.v.f)
        self.he.remove(y)
        self.he.remove(y.f.v.f)

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
            raise ValueError, "Map is inconsistent."
        if len(set(D.values())) != len(D):
            raise ValueError, "Map is not injective."
        for a in he:
            if a.decorations != D[a].decorations:
                raise ValueError, "%s is not compatible with decorations." %D
        for a in he:
            if a.v != None:
                if D[a.v] != D[a].v:
                     raise ValueError, "%s is not compatible with vertex maps." %D
            if a.f != None:
                if D[a.f] != D[a].f:
                     raise ValueError, "%s is not compatible with face maps." %D

        self.domain = f
        self.codomain = g
        self.map = D

    def show(self):
        print "Not yet implemented."

    def compose(self, other):
        print "Not yet implemented."



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
    if u != None and not u in h.he:
        raise ValueError, "Must given an element of domain."
    if not h.is_connected():
        raise ValueError, "Domain must be connected."
    if len(h.he) == 1:
        raise ValueError, "Domain must be non-empty." 

    if u == None: u = h.he.pop()

    def test(x):
        D = dict()
        D[u] = x
        flag = True
        while flag:
            flag = False
            newD = dict()
            for a in D:
                if a.v != None and not a.v in D:
                    newD[a.v] = D[a].v
                if a.f != None and not a.f in D:
                    newD[a.f] = D[a].f
            if len(newD) != 0:
                if any( a.decorations != newD[a].decorations for a in newD ):
                    return False, D
                D.update(newD)
                flag = True
            for a in D:
                if a.v in D:
                    if D[a.v] != D[a].v:
                        return False, D
                if a.f in D:
                    if D[a.f] != D[a].f:
                        return False, D
        return len(D.values()) == len(h.he), D

    output = []
    for x in g.he:
        t, D = test(x)
        if t:
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


