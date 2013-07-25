
#*****************************************************************************
#       Copyright (C) 2011 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

"""
The basic construction in this module is to take a ribbon graph and add a
boundary to get a closed ribbon graph with a boundary. This is the first stage
in drawing the ribbon graph.
"""

from collections import namedtuple

Circle = namedtuple('Circle',['type','angle','boundary','halfedges'])

from math import pi

import spider # Only required for testing.
import surface
import graphics

class ClosedGraph(object):

    default_options = {'graph':True, 'circles':False, 'medial':False, 'medialV':False,\
                  'triangles':False, 'radicalcircles':False}

    def __init__(self, g, outside, geometry='Euclidean', bc='Neumann', name=None, options=None):
        """
         EXAMPLES:

        >>> g = spider.RibbonGraph.polygon(5).closure()
        """

        if set([a.e for a in g.he]) != set(g.he):
            raise ValueError, "e is not a bijection."
        if not bc in ['Dirichlet','Neumann','Cauchy']:
            raise ValueError, boundary_condition

        fc = g.get_orbits( lambda a: a.e.c )
        ot = set(outside)
        if not any( set(x) == ot for x in fc ):
            raise ValueError("Second argument is not a face.")

        self.graph = g
        self.outside = outside
        self.geometry = geometry
        self.boundary_condition = bc

        if options == None:
            options = ClosedGraph.default_options

        self.name = name
        self.options = options

        for a in self.faces:
            for x in a:
                if x.e in a:
                    print "There is a problem with a face."
                    return
       
        V, E, F = self.set_circles()
        self.Vcircles = V
        self.Ecircles = E
        self.Fcircles = F

        self.triangles = self.set_triangles()

    def set_circles(self):
        if hasattr(self, 'circles'):
            print "Why are you calling the function closedgraph.ClosedGraph.get_circles()?"

        Fcircles = [ Circle('FC',2*pi,False,frozenset(x)) for x in self.faces ]
        Fcircles.remove(Circle('FC',2*pi,False,frozenset(self.outside)))

        if self.boundary_condition == 'Dirichlet':
            if self.geometry == 'hyperbolic':
                boundary = self.outside + [ a.e for a in self.outside ]
                inside = [ a for a in self.graph.he if not a in boundary ]

                vertices = self.graph.vertices
                in_vertices = [ x for x in vertices if set(x).issubset(inside) ]
                out_vertices = [ x for x in vertices if not x in in_vertices ]
                if len(vertices) != len(out_vertices) + len(in_vertices):
                    raise RuntimeError

                corners = [ x for x in out_vertices if len(x) == 2 ]
                #bd_vertices = [ x for x in out_vertices if len(x) == 3 ]
                bd_vertices = [ x for x in out_vertices if not x in corners ]
                C = len(corners)
                B = len(bd_vertices)
                if len(out_vertices) != C + B:
                    raise RuntimeError

                CRcircles = [ Circle('CR', (1-2.0/C)*pi,False, frozenset(x)) for x in corners ]
                BVcircles = [ Circle('BV',pi,False,frozenset(x)) for x in bd_vertices ]
                IVcircles = [ Circle('IV',2*pi,False,frozenset(x)) for x in in_vertices ]
                Vcircles  = CRcircles + BVcircles + IVcircles

                edges = self.edges
                bd_edges = [ x for x in edges if set(x).issubset(boundary) ]
                BEcircles = [ Circle('BE',pi,False,frozenset(x)) for x in bd_edges ]
                in_edges = [ x for x in edges if not set(x).issubset(boundary) ]
                IEcircles = [ Circle('IE',2*pi,False,frozenset(x)) for x in in_edges ]
                Ecircles = BEcircles + IEcircles

            else:
                raise NotImplementedError, 'Only hyperbolic geometry has been implemented.'

        elif self.boundary_condition == 'Neumann':
            boundary = self.outside + [ a.e for a in self.outside ]
            inside = [ a for a in self.graph.he if not a in boundary ]

            vertices = self.graph.vertices
            in_vertices = [ x for x in vertices if set(x).issubset(inside) ]
            out_vertices = [ x for x in vertices if not x in in_vertices ]
            if len(vertices) != len(out_vertices) + len(in_vertices):
                raise RuntimeError

            corners = [ x for x in out_vertices if len(x) == 2 ]
            #bd_vertices = [ x for x in out_vertices if len(x) == 3 ]
            bd_vertices = [ x for x in out_vertices if not x in corners ]
            C = len(corners)
            B = len(bd_vertices)
            if len(out_vertices) != C + B:
                raise RuntimeError

            CRcircles = [ Circle('CR', (1-2.0/C)*pi,False, frozenset(x)) for x in corners ]
            BVcircles = [ Circle('BV',pi,False,frozenset(x)) for x in bd_vertices ]
            IVcircles = [ Circle('IV',2*pi,False,frozenset(x)) for x in in_vertices ]
            Vcircles  = CRcircles + BVcircles + IVcircles

            edges = self.edges
            bd_edges = [ x for x in edges if set(x).issubset(boundary) ]
            BEcircles = [ Circle('BE',pi,False,frozenset(x)) for x in bd_edges ]
            in_edges = [ x for x in edges if not set(x).issubset(boundary) ]
            IEcircles = [ Circle('IE',2*pi,False,frozenset(x)) for x in in_edges ]
            Ecircles = BEcircles + IEcircles

        elif self.boundary_condition == 'Cauchy':
            print "These boundary conditions have not been implemented."

        else:
            raise RuntimeError, "This can't happen."

        return Vcircles, Ecircles, Fcircles

    def set_triangles(self):
        if hasattr(self, 'triangles'):
            print "Why are you calling the function closedgraph.ClosedGraph.get_triangles()?"

        DV = dict()
        for x in self.Vcircles:
            for a in x.halfedges:
                DV[a] = x

        DE = dict()
        for x in self.Ecircles:
            for a in x.halfedges:
                DE[a] = x

        DF = dict()
        for x in self.Fcircles:
            for a in x.halfedges:
                DF[a] = x

        if set(DV.keys()) != set(DE.keys()):
            raise RuntimeError
        #if set(DE.keys()) != set(DF.keys()).union(set(outside)):
            #raise RuntimeError

        return [(DV[a],DE[a],DF[a],True,) for a in DF]\
                   + [(DV[a.e],DE[a.e],DF[a],False,) for a in DF]


    @property
    def vertices(self):
        return self.graph.get_orbits( lambda a: a.c )

    @property
    def edges(self):
        return self.graph.get_orbits( lambda a: a.e )

    @property
    def faces(self):
        return self.graph.get_orbits( lambda a: a.e.c )

    @property
    def genus(self):
        chi = len(self.vertices) - len(self.edges) + len(self.faces)
        if chi % 2 != 0:
            raise RuntimeError
        return 1 + chi/2

    def anytadpole(self):
        """This checks if there is a tadpole which will cause problems when it
        comes to the drawing."""
        faces = self.faces
        for f in faces:
            if any( a.e in f for a in f):
                return True
        return False

    def __latex__(self,options):
        surface.SurfaceComplex(self).show('Tikz','stdout')

    def show(self, style='SVG', name=None):
        #V, E, F = self.set_circles()
        #self.Vcircles = V, self.Ecircles = E, self.Fcircles = F
        #self.triangles = self.set_triangles()

        surface.SurfaceComplex(self).show(style, options=ClosedGraph.default_options, name=name)


# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()
