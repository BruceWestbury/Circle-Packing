
#*****************************************************************************
#       Copyright (C) 2011 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

"""
This is the start of implementing some knot theory.

The precedents for this are Knotscape, Knotilus, SnapPy, KnotAtlas, Knotplot

Andrew Bartholomew's Mathematics Page
http://www.layer8.co.uk/maths/index.htm

The CompuTop.org Software Archive
http://www.math.uiuc.edu/~nmd/computop/

SeifertView
http://www.win.tue.nl/~vanwijk/seifertview/

Seifert Matrix Computation (Julia Collins)
http://www.maths.ed.ac.uk/~s0681349/SeifertMatrix

AUTHOR:

- Bruce Westbury (2011-08-03): initial version

"""

__all__ = [ 'LinkDiagram' ]

import ribbon
import pivotal
import closedgraph

from itertools import product

in_over = ribbon.Features('head','blue',True)
in_under = ribbon.Features('head','blue',False)
out_over = ribbon.Features('tail','blue',True)
out_under = ribbon.Features('tail','blue',False)

class LinkDiagram(closedgraph.ClosedGraph):

    def __init__(self,g,outside):
        if set([a.e for a in g.he]) != set(g.he):
            raise ValueError("e is not a bijection.")

        fc = g.get_orbits( lambda a: a.e.c )
        ot = set(outside)
        if not any( set(x) == ot for x in fc ):
            raise ValueError("Second argument is not a face.")

        self.graph = g
        self.outside = outside
        self.bc = 'Dirichlet'

    @staticmethod
    def from_DT(DT):
        """Construct a knot diagram from the Dowker-Thistlewaite code.

        The theory is given in the original paper:

        Classification of knot projections
        C. H. Dowker & Morwen B. Thistlewaite
        Topology and its Applications 16 (1983), 19--31

        INPUT:
            A list of positive even integers

        OUTPUT:
            A closed justgraph

        EXAMPLES:
            >>> LinkDiagram.from_DT(DT([4,6,2])) #doctest: +ELLIPSIS
            <__main__.LinkDiagram object at 0x...>
            >>> LinkDiagram.from_DT(DT([4,6,8,2])) #doctest: +ELLIPSIS
            <__main__.LinkDiagram object at 0x...>
            >>> LinkDiagram.from_DT(DT([4,8,10,2,6])) #doctest: +ELLIPSIS
            <__main__.LinkDiagram object at 0x...>
            >>> LinkDiagram.from_DT(DT([6,8,10,2,4])) #doctest: +ELLIPSIS
            <__main__.LinkDiagram object at 0x...>

            >>> g = LinkDiagram.from_DT(DT([4,6,2]))
            >>> [ len(v) for v in g.vertices ]
            [4, 4, 4]
            >>> [ len(v) for v in g.edges ]
            [2, 2, 2, 2, 2, 2]
            >>> x = [ len(v) for v in g.faces ]
            >>> x.sort()
            >>> x
            [2, 2, 2, 3, 3]

            >>> g = LinkDiagram.from_DT(DT([4,6,8,2]))
            >>> [ len(v) for v in g.vertices ]
            [4, 4, 4, 4]
            >>> [ len(v) for v in g.edges ]
            [2, 2, 2, 2, 2, 2, 2, 2]
            >>> x = [ len(v) for v in g.faces ]
            >>> x.sort()
            >>> x
            [2, 2, 3, 3, 3, 3]
            >>> x = [ len(v) for v in g.graph.get_orbits( lambda a: a.c.e ) ]
            >>> x.sort()
            >>> x
            [2, 2, 3, 3, 3, 3]

            >>> g = LinkDiagram.from_DT(DT([4,8,10,2,6]))
            >>> [ len(v) for v in g.vertices ]
            [4, 4, 4, 4, 4]
            >>> [ len(v) for v in g.edges ]
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            >>> x = [ len(v) for v in g.faces ]
            >>> x.sort()
            >>> x
            [2, 2, 2, 3, 3, 4, 4]
            >>> x = [ len(v) for v in g.graph.get_orbits( lambda a: a.c.e ) ]
            >>> x.sort()
            >>> x
            [2, 2, 2, 3, 3, 4, 4]

            >>> g = LinkDiagram.from_DT(DT([8,10,2,12,4,6]))
            >>> x = [ len(v) for v in g.vertices ]
            >>> x.sort()
            >>> x
            [4, 4, 4, 4, 4, 4]
            >>> [ len(v) for v in g.edges ]
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
            >>> x = [ len(v) for v in g.faces ]
            >>> x.sort()
            >>> x
            [2, 2, 2, 3, 3, 3, 4, 5]
            >>> x = [ len(v) for v in g.graph.get_orbits( lambda a: a.c.e ) ]
            >>> x.sort()
            >>> x
            [2, 2, 2, 3, 3, 3, 4, 5]

        REFS:
            http://katlas.org/wiki/DT_%28Dowker-Thistlethwaite%29_Codes
        """

        emb = DT.orientation

        m = 2 * len(emb)

        left =  [ ribbon.halfedge() for i in range(m) ]
        right = [ ribbon.halfedge() for i in range(m) ]
        for i in range(m):
            left[i].e = right[i-1]
            right[i-1].e = left[i]
        for i, k in enumerate(DT.code):
            a = abs(k)-1
            x = [ left[2*i], left[a], right[2*i], right[a] ]
            if k > 0:
                x[0].decorations = in_over
                x[1].decorations = in_under
                x[2].decorations = out_over
                x[3].decorations = out_under
            elif k < 0:
                x[0].decorations = in_under
                x[1].decorations = in_over
                x[2].decorations = out_under
                x[3].decorations = out_over
            else:
                raise ValueError("Not a valid Dowker-Thistlewaite code")
            if emb[i] == -1:
                x.reverse()
            elif emb[i] != 1:
                raise RuntimeError
            for i in xrange(4):
                x[i-1].c = x[i]

        g = ribbon.justgraph( set(left).union(set(right)) )
        outside = g.get_orbits( lambda a: a.e.c )[0]
        return LinkDiagram(g,outside)

    @staticmethod
    def from_braid(word):
        """Constructs a link diagram from a braid word.

        INPUT: A list of non-zero integers

        OUTPUT: A LinkDiagram

        EXAMPLES:

        >>> LinkDiagram.from_braid([1]) #doctest: +ELLIPSIS
        <__main__.LinkDiagram object at 0x...>

        """

        b = pivotal.braid(word)

        g = b.graph
        for u, v in zip( b.domain, b.codomain ):
            g.stitch(u,v)
        g.normal()

        u = b.domain[0]
        outside = [u]
        s = u.e.c
        while s != u:
            outside.append(s)
            s = s.e.c

        return LinkDiagram( g, outside )

    @staticmethod
    def from_PlanarDiagram(PD):
        """Produces a LinkDiagram from the planar diagram notation.

        INPUT: A list or set of 4-tuples

        OUTPUT: A closed justgraph

        EXAMPLES:

        >>> LinkDiagram.from_PlanarDiagram([[1,2,3,4],[4,3,6,5],[2,1,5,6]]) #doctest: +ELLIPSIS
        <__main__.LinkDiagram object at 0x...>

        >>> g = LinkDiagram.from_PlanarDiagram([[1,2,3,4],[4,3,6,5],[2,1,5,6]])
        >>> [ len(v) for v in g.vertices ]
        [4, 4, 4]
        >>> [ len(v) for v in g.edges ]
        [2, 2, 2, 2, 2, 2]
        >>> x = [ len(v) for v in g.faces ]
        >>> x.sort()
        >>> x
        [2, 2, 2, 3, 3]
        >>> x = [ len(v) for v in g.graph.get_orbits( lambda a: a.e.c ) ]
        >>> x.sort()
        >>> x
        [2, 2, 2, 3, 3]


        """
        if not all([ len(x) == 4 for x in PD ]):
            raise ValueError("Not a valid planar diagram code")
        for i in range(2*len(PD)):
            p = [ x for x in PD if i+1 in x ]
            if len(p) != 2:
                raise ValueError("Not a valid planar diagram code")

        D = dict()
        he = set()
        for x in PD:
            a = [ ribbon.halfedge() for i in range(4) ]
            for i in range(4):
                a[i-1].c = a[i]
            D[tuple(x)] = a
            he = he.union(set(a))

        for i in range(2*len(PD)):
            p = [ x for x in PD if i+1 in x ]
            a0 = D[tuple(p[0])][p[0].index(i+1)]
            a1 = D[tuple(p[1])][p[1].index(i+1)]
            a0.e = a1
            a1.e = a0

        g = ribbon.justgraph(he)
        outside = g.get_orbits( lambda a: a.e.c )[0]
        return LinkDiagram(g,outside)

    @property
    def _components(self):
        m = lambda a: a.e.c.c
        return self.graph.get_orbits(m)

    # Could draw components in different colours.
    @property
    def no_components(self):
        """Computes the number of components of a link diagram.

        EXAMPLE:

        >>> c = DT([4,6,8,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.no_components
        1

        """

        return len(self._components)/2

    @property
    def DowkerThistlewaite(self):
        """Computes a Dowker-Thistlewaite code of a knot diagram.

        EXAMPLE:

        >>> c = DT([4,6,8,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> a = g.DowkerThistlewaite
        >>> a in [[1, 2, 3, 1, 4, 3, 2, 4],[1, 2, 3, 4, 2, 1, 4, 3]]
        True

        """
        cp = self._components
        if len(cp) > 2:
            raise ValueError("This has only been implemented for knots.")

        c = cp[0]
        vt = self.vertices
        DV = dict()
        for x in vt:
            for a in x:
                DV[a] = x
        count = 0
        D = dict([ (x,None) for x in vt ])

        for a in c:
            if D[DV[a]] == None:
                count += 1
                D[DV[a]] = count

        return [ D[DV[a]] for a in c ]


    @property
    def meander_word(self):
        pass

    @property
    def planar_diagram(self):
        pass

    def reverse_orientation(self):
        """Reverses the crossings of a LinkDiagram.

        EXAMPLE:

        >>> c = DT([4,6,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.reverse_orientation() #doctest: +ELLIPSIS
        <__main__.LinkDiagram object at 0x...>
        >>> g.reverse_orientation().genus
        2


        """

        switch = {'head':'tail','neither':'neither','tail':'head'}
        phi = self.graph.copy()
        g = phi.codomain

        for a in g.he:
            a.decorations._replace(directed=switch[a.decorations.directed])

        outside = [ phi.map[a] for a in self.outside ]
        return LinkDiagram(g,outside)

    def reverse_crossings(self):
        """Reverses the crossings of a LinkDiagram.

        EXAMPLE:

        >>> c = DT([4,6,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.reverse_crossings() #doctest: +ELLIPSIS
        <__main__.LinkDiagram object at 0x...>
        >>> g.reverse_crossings().genus
        2

        """
        phi = self.graph.copy()
        g = phi.codomain

        for a in g.he:
            a.decorations._replace(over = not a.decorations.over)

        outside = [ phi.map[a] for a in self.outside ]
        return LinkDiagram(g,outside)

    def connected_sum(self,other):
        """Constructs the connected sum of two link diagrams.

        EXAMPLE:

        >>> c = DT([4,6,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.connected_sum(g) #doctest: +ELLIPSIS
        <__main__.LinkDiagram object at 0x...>
        >>> g.connected_sum(g).genus
        2

        """
        phi = self.graph.copy()
        psi = other.graph.copy()

        he = phi.codomain.he.union(psi.codomain.he)

        u = phi.map[self.outside[0]]
        v = psi.map[other.outside[0]]
        x = u.e; y = v.e

        if u.decorations.over == v.decorations.over:
            u.e = y; y.e = u
            v.e = x; x.e = v
        else:
            u.e = x; x.e = u
            v.e = y; y.e = v


        outside = [u]
        s = u.e.c
        while s != u:
            outside.append(s)
            s = s.e.c

        return LinkDiagram( ribbon.justgraph(he), outside )

    def cable(self,n):
        r = range(n)
        p = product(self.graph.he,range(n),range(n))
        D = dict()

        for x in p:
            D[x] = halfedge()

        for x in p:
            D[x].decorations = x[0].decorations
            D[x].c = D[(x[0].c,x[1],x[2])]


    def colourings(self,n):
        pass

    @property
    def seifert(self):
        """Finds the Seifert circles of a LinkDiagram.

        EXAMPLE:

        >>> g = LinkDiagram.from_DT(DT([4,6,8,2]))
        >>> x = [ len(x) for x in g.seifert ]
        >>> x.sort(); x
        [2, 2, 2, 2, 4, 4]

        """
        def _next(a):
            if a.e.c.decorations.directed == a.decorations.directed:
                return a.e.c
            else:
                return a.e.c.c.c

        return self.graph.get_orbits( _next )

    def withseifert(self):
        """Draws a link diagram with coloured Seifert circles.

        EXAMPLES: See demo.py

        """
        colours = ['red','blue','green','purple','orange','brown']
        phi = self.graph.copy()
        g = phi.codomain
        ot = [ phi.map[a] for a in self.outside ]
        ld = LinkDiagram(g, ot)
        st = set([ frozenset(x + tuple([ a.e for a in x ])) for x in ld.seifert ])
        col = colours
        while len(col) < len(st):
            col = col + colours

        for x, c in zip(st, col):
            for a in x:
                dec = a.decorations
                a.decorations = ribbon.Features(dec.directed, c, dec.over)

        return ld

    def witharcs(self):
        """Draws a link diagram with coloured arcs.

        EXAMPLES: See demo.py

        """
        colours = ['red','blue','green','purple','orange','brown']
        phi = self.graph.copy()
        g = phi.codomain
        ot = [ phi.map[a] for a in self.outside ]
        ld = LinkDiagram(g, ot)
        st = ld.arcs
        col = colours
        while len(col) < len(st):
            col = col + colours

        for x, c in zip(st, col):
            for a in x:
                dec = a.decorations
                a.decorations = ribbon.Features(dec.directed, c, dec.over)

        return ld

    @property
    def arcs(self):
        """Finds the arcs of a LinkDiagram.

        EXAMPLES:

        >>> g = LinkDiagram.from_DT(DT([4,6,2]))
        >>> x = [ len(x) for x in g.arcs ]
        >>> x.sort(); x
        [4, 4, 4]


        >>> g = LinkDiagram.from_DT(DT([4,6,8,2]))
        >>> x = [ len(x) for x in g.arcs ]
        >>> x.sort(); x
        [4, 4, 4, 4]

        """
        initial = [ a for a in self.graph.he if\
          a.decorations.directed == 'tail' and\
          a.decorations.over == False ]

        output = []
        for a in initial:
            arc = [a,a.e]
            s = a
            while s.e.decorations.over:
                s = s.e.c.c
                arc = arc + [s,s.e]
            output.append(arc)
        return output

    @property
    def three_colourings(self):
        """Calculates the number of three colourings of the LinkDiagram.

        A colouring is a labelling of the arcs by one of three colours.
        A colouring is allowed if either one or three colours appear at
        each crossing. The number of allowed colourings is a link invariant.
        This number is a multiple of three because the three colours can be
        interchanged. If the number of colourings is N then the number
        returned by this function is N/3 - 1.

        This should be rewritten using backtracking.

        >>> c = DT([4,6,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.three_colourings
        2
        >>> c = DT([4,6,8,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.three_colourings
        0
        >>> c = DT([4,8,10,2,6])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.three_colourings
        0
        """
        ac = self.arcs
        seq = product( * [range(3)] * (len(ac)-1) )
        count = 0
        label = dict()

        def allowed(p):
            for a in ac[0]:
                label[a] = 0
            for i, x in enumerate(ac[1:]):
                for a in x:
                    label[a] = p[i]

            init = ( a for a in self.graph.he if\
              a.decorations.directed == 'head' and\
              a.decorations.over == True )

            for a in init:
                if label[a] != label[a.c.c]:
                    raise RuntimeError
                if (2*label[a] - label[a.c] - label[a.c.c.c]) % 3 != 0:
                    return False
            return True

        for p in seq:
            if allowed(p):
                count += 1
        return count - 1

    @property
    def braid(self):
        """Given a link diagram find a braid whose closure is the link.

        The existence of the braid is known as Alexander's theorem.
        This is an implementation of Vogel's algorithm. This does not
        change the number of Seifert circles but does increase the number
        of crossings.

        EXAMPLES:

        >>> c = DT([4,6,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.braid #doctest: +ELLIPSIS
        <pivotal.Morphism instance at 0x...>

        >>> c = DT([4,6,8,2])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.braid #doctest: +ELLIPSIS
        <pivotal.Morphism instance at 0x...>

        c = DT([4,8,10,2,6])
        g = LinkDiagram.from_DT(c)
        g.braid #doctest: +ELLIPSIS
        <pivotal.Morphism instance at 0x...>

        >>> c = DT([8,10,2,12,4,6])
        >>> g = LinkDiagram.from_DT(c)
        >>> g.braid #doctest: +ELLIPSIS
        <pivotal.Morphism instance at 0x...>

        """

        def get_arc(f):
            """Finds an arc."""
            sf = f.seifert
            DS = dict()
            for x in sf:
                for a in x:
                    DS[a] = x

            # Could use product and ifilter from itertools
            for fc in f.faces:
                for j, v in enumerate(fc):
                    for i in range(j-1):
                        u = fc[i]
                        if DS[u] != DS[v] and u.decorations.directed == v.decorations.directed:
                            return u,v
            return None

        def vogel_move(f,u,v):
            # This goes into an infinite loop
            phi = f.graph.copy()
            new = phi.codomain
            a = phi.map[u]
            b = a.e
            c = phi.map[v]
            d = c.e
            x = [ ribbon.halfedge() for i in range(4) ]
            for i in range(4):
                x[i-1].c = x[i]
            y = [ ribbon.halfedge() for i in range(4) ]
            for i in range(4):
                y[i-1].c = y[i]
            a.e = x[0]; x[0].e = a
            d.e = x[3]; x[3].e = d
            b.e = y[1]; y[1].e = b
            c.e = y[2]; y[2].e = c
            x[1].e = y[0]; y[0].e = x[1]
            x[2].e = y[3]; y[3].e = x[2]
            switch = {'head':'tail','neither':'neither','tail':'head'}
            ut = a.decorations.directed
            ot = switch[ut]

            if False:
                x[0].decorations._replace(a.decorations.colour)
                x[1].decorations._replace(c.decorations.colour)
                x[2].decorations._replace(a.decorations.colour)
                x[3].decorations._replace(c.decorations.colour)
                y[0].decorations._replace(d.decorations.colour)
                y[1].decorations._replace(b.decorations.colour)
                y[2].decorations._replace(d.decorations.colour)
                y[3].decorations._replace(b.decorations.colour)

            for a in x:
                a.decorations._replace(colour='red')
            for a in y:
                a.decorations._replace(colour='red')


            g = ribbon.justgraph( new.he.union( set(x+y) ) )

            u = phi.map[f.outside[0]]
            outside = [u]
            s = u.e.c
            while s != u:
                outside.append(s)
                s = s.e.c

            return LinkDiagram(g,outside)


        f = self
        while 1:
            a = get_arc(f)
            if a == None:
                break
            f = vogel_move(f,a[0],a[1])
            print f.genus
            #f.show()

        # The code below appears to be correct
        faces = f.faces
        fc = [ frozenset(x) for x in faces ]

        def start():
            for x in f.seifert:
                if frozenset(x) in fc:
                    if x[0].decorations.directed == 'head':
                        return x
            raise RuntimeError

        index = dict()
        for a in f.graph.he:
            index[a] = None
        for a in start():
            index[a] = 0
            index[a.e] = 0

        def v_find(i):
            for x in f.vertices:
                u = [ a for a in x if index[a] == None ]
                v = [ a for a in x if index[a] == i ]
                if len(u) == 2 and len(v) == 2:
                    return u,v
            raise RuntimeError

        sf = f.seifert
        DS = dict()
        for x in sf:
            for a in x:
                DS[a] = x

        n = len(sf)/2 # This is #braid strings = #Seifert circles
        for i in range(n-1):
            c = v_find(i)
            for x in c[0]:
                for a in DS[x]:
                    index[a] = i+1
                    index[a.e] = i+1

        if any([ index[a] == None for a in f.graph.he ]):
            raise RuntimeError


        for a in start():
            if a.decorations.directed == 'head':
                cut_path = [ a ]
                break

        DF = dict()
        for x in faces:
            for a in x:
                DF[a] = x

        for i in range(n-1):
            x = DF[ cut_path[i].e ]
            for a in x:
                if index[a] == i+1 and a.decorations.directed == 'head':
                    cut_path.append(a)
                    break

        if len(cut_path) != n:
            raise RuntimeError

        phi = f.graph.copy()
        do = [ phi.map[a] for a in cut_path ]
        co = [ phi.map[a.e] for a in cut_path ]

        for a in cut_path:
            phi.map[a].e = None
            phi.map[a.e].e = None

        g = ribbon.justgraph(phi.codomain.he)

        return pivotal.Morphism(g,do,co)


class DT(object):
    """Implements Dowker-Thistlewaite codes."""
    def __init__(self,code):
        # Should do checking here.
        self.code = code

    @property
    def full_code(self):
        n = len(self.code)
        m = 2*n
        seq = [0] * m
        for i, a in enumerate(self.code):
            k = abs(a)-1
            seq[2*i] = k
            seq[ k ] = 2*i

        return seq


    @property
    def orientation(self):
        """ Determines the orientation for a Dowker-Thistlewaite code.

        INPUT: A list of non-negative integers.

        OUTPUT: A list of integers.

        EXAMPLES:

        >>> DT([4,6,2]).orientation
        [1, 1, 1]

        >>> DT([4,6,8,2]).orientation
        [1, -1, 1, -1]

        >>> DT([4,8,10,2,6]).orientation
        [1, 1, 1, 1, 1]

        >>> DT([8,10,2,12,4,6]).orientation
        [1, -1, 1, 1, -1, 1]

        """
        first_non_zero = lambda L: min(i for i in range(len(L)) if L[i])
        # Returns the index of the frist non-zero entry in the list - dies on an all 0 list.

        code = self.full_code

        M = len(code) # Uusualy denoted 2*N
        seq = code * 2  # seq is two copies of full DT involution on crossings numbered 0 to 2N-1.
        emb, A = [0] * M, [0] * M  # zero emb and A. A will only ever contain zeroes and ones.

        # Set initial conditions.
        A[0], A[seq[0]] = 1, 1
        emb[0], emb[seq[0]] = 1, -1

        # Determine the possible phi's
        all_phi = [[0] * M for i in range(M)]
        for i in range(M):
            all_phi[i][i] = 1
            for j in range(i, i+M):
                all_phi[i][j % M] = 1 if i == j else -all_phi[i][(j-1) % M] if i <= seq[j] <= seq[i] else all_phi[i][(j-1) % M ]

        while any(A):
            i = first_non_zero(A)  # let i be the index of the first non-zero member of A
            psi = all_phi[i]

            D = [1] * M
            D[i:seq[i]+1] = [0] * (seq[i] - i + 1)
            while any(D):
                x = first_non_zero(D)  # let x be the index of the first non-zero member of D
                D[x] = 0

                if i <= seq[x] <= seq[i] and emb[x] != 0 and psi[x] * psi[seq[x]] * emb[i] != emb[x]:
                    raise ValueError("Something bad has happened, sequence is not realizable.")
                if (seq[x] < i or seq[i] < seq[x]) and psi[x] * psi[seq[x]] != 1 and x < i:
                    # This extra AND conditions shouldn't be needed.
                    raise ValueError("Something bad has happened, sequence is not realizable.")

                if seq[i] < seq[x] or seq[x] < i:
                    D[seq[x]] = 0
                elif emb[x] == 0: # emb[x] is already defined
                    assert D[seq[x]] == 0
                    emb[x] = psi[x] * psi[seq[x]] * emb[i]
                    emb[seq[x]] = -emb[x]
                    if abs(seq[x]-seq[x-1]) % M != 1:
                        A[x] = 1
                        A[seq[x]] = 1

                A[i], A[seq[i]] = 0, 0

        return emb[::2]
        # Note [emb[pairs_dict[2*i]] for i in range(N)] is also a valid code.

# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()

















