
#*****************************************************************************
#       Copyright (C) 2013 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

"""
This module is for surfaces. This is a simplicial complex obtained by
identifying edges of oriented triangles by orientation reversing isomorphisms.
The simplicial complex is constructed from a closed graph and the aim is to
encapsulate the combinatorial book-keeping associated with the closed graph.
This information is then available for different implementations of circle packing.
"""

#For arbitrary precision we could import decimal and use Decimal

import spider
import closedgraph
import graphics

from cmath import rect
from math import pi, sin, acos, asin, sqrt

def euc_tri01(u):
    a = [ u[i-2]+u[i-1] for i in range(3) ]
    ai = [ 1/x for x in a]
    aa = [ x*x for x in a ]
    return [ acos( (aa[i-1]+aa[i-2]-aa[i])*ai[i-1]*ai[i-2]*0.5 )
             for i in range(3) ]

def hyp_tri01(u):
    raise NotImplementedError, "Hyperbolic geometry has not been implemented."

def euc_tri02(u):
    a = [ (u[i-1]/(u[i]+u[i-1])) * (u[i-2]/(u[i]+u[i-2])) for i in range(3) ]
    return [ 2*asin(sqrt(x)) for x in a ]

def hyp_tri02(u):
    a = [ ((1-u[i-1])/(1-u[i]*u[i-1])) * ((1-u[i-2])/(1-u[i]*u[i-2])) for i in range(3) ]
    return [ 2*asin(sqrt(u[i]*a[i])) for i in range(3) ]

def euc_adj(c,a,k,d,r):
    beta = sin( a/(2*k) )
    f = (d-1)/d
    return r * f * beta / (beta-1)

def hyp_adj(c,a,k,d,r):
    beta = sin( a/(2*k) )
    v = max( (beta-sqrt(r))/(beta*r-sqrt(r)) , 0 )
    den = sqrt((1-v)*(1-v)+4*d*d*v) + 1 - v
    t = 2*d/den
    return t*t

class SurfaceComplex(object):

    error = 0.0000001
    vr = 10.0
    er = 10.0
    tolerance = 0.1


    def __init__(self,gc):
        """
        EXAMPLES:

        >>> g = spider.RibbonGraph.polygon(5)
        >>> SurfaceComplex(g.closure()) #doctest: +ELLIPSIS
        <__main__.SurfaceComplex object at 0x...>

        """

        if not isinstance(gc, closedgraph.ClosedGraph):
            return ValueError, "This construction takes a closed graph."

        self.Vcircles = gc.Vcircles
        self.Ecircles = gc.Ecircles
        self.Fcircles = gc.Fcircles

        self.triangles = gc.triangles

        self.outside = gc.outside
        self.boundary_condition = gc.boundary_condition
        self.options = gc.options

        self.geometry = gc.geometry
        self.boundary_condition = gc.boundary_condition

    def rim(self):
        """Assumes Neumann boundary conditions."""
        if not hasattr(self, 'radius'):
            self.layout()

        bV = [[ a for a in self.Vcircles if x in a.halfedges ][0] \
              for x in self.outside ]
        bE = [[ a for a in self.Ecircles if x in a.halfedges ][0] \
              for x in self.outside ]
        n = len(bV)
        if n != len(bE):
            raise RuntimeError

        #print [ x.type for x in bV ]
        #print [ x.type for x in bE ]

        angles = [ pi-a.angle for a in bV ]
        ta = sum(angles)
        if 2*pi != ta:
            print "Warning sum of exterior angles is %s" % ta
        ag = [0]*n
        #ag[0] = angles[0]
        for i in range(n-1):
            ag[i+1] = ag[i] + angles[i]

        sr = [ self.radius[bV[i]] for i in range(n) ]
        lengths = [ sr[i] + 2*self.radius[bE[i]] + sr[i-1] \
                    for i in range(n) ]
        #print "Lengths (rim): ", [ "%3.4f " % lengths[i] for i in range(n) ]
        #cenV = [ self.centre[bV[i]] for i in range(n) ]
        #print "Lengths (pos): ", [ "%3.4f " % abs(cenV[i] - cenV[i-1]) for i in range(n) ]

        sides = [ -rect(r, phi) for r, phi in zip(lengths, ag) ]
        #print [ "%3.4f " % abs(cenV[i]-cenV[i-1]-sides[i]) for i in range(n) ]

        from math import log10
        print "Accurate to %3.2f decimal places." % log10(abs(sum(sides)))

        co = [0]*n
        #co[0] = sides[0]
        for i in range(n-1):
            co[i+1] = co[i] + sides[i+1]
        pos = {bV[i]:co[i] for i in range(n)}


        #print [ "%3.4f " % abs(cenV[i]-co[i]) for i in range(n) ]

        for i in range(n):
            s = self.radius[bV[i-1]] + self.radius[bE[i]]
            r = self.radius[bV[i]]   + self.radius[bE[i]]
            pos[ bE[i-1] ] = (r*co[i-1]+s*co[i])/(r+s)

        #cenE = [ self.centre[bE[i]] for i in range(n) ]
        #print [ "%3.4f " % abs(cenE[i]-pos[ bE[i] ]) for i in range(n) ]

        return pos

    def packing_basic(self):
        """This implements the algorithm in:

        Introduction to Circle Packing by Ken Stephenson, Practicum III

        (without using either of the acceleration schemes).
        """

        if self.geometry == 'Euclidean':
            _tri   = euc_tri02
            _adj   = euc_adj
        elif self.geometry == 'hyperbolic':
            _tri   = hyp_tri02
            _adj   = hyp_adj
        else:
            raise RuntimeError, "This can't happen."

        if self.boundary_condition == 'Neumann':
            radius = {}

            circles = self.Vcircles + self.Ecircles + self.Fcircles
            for c in circles:
                radius[c] = SurfaceComplex.er

            for c in self.Vcircles:
                if c.boundary:
                    radius[c] = SurfaceComplex.vr

            # Dictionary for number of neighbours
            neighbours = dict([ (c,len([ t for t in self.triangles if c in t ])) for c in circles])

            int_circles = [ c for c in circles if not c.boundary ]
            # Dictionary for number used for correction.
            # This is delta in Stephenson's notation.
            delta = dict([ (c,sin(c.angle/(2*neighbours[c]))) for c in int_circles])

            #if int_circles != circles: # Dirichlet boundary conditions
            #    itcirc = int_circles
            #else: # von Neumann boundary conditions
            itcirc = int_circles[1:]

            angle = {}

            # Speed this up using numpy arrays

            packing = False
            count = 0
            while not packing:
                packing = True
                count += 1
                for c in circles:
                    angle[c] = 0.0

                #nangle = numpy.zeros(len(circles))
                #nt = [ t for t in self.triangles ]
                #nu = numpy.array([ [ radius[t[i]] for i in range(3) ] for t in nt ])
                #na = nu + numpy.roll(nu,1,axis=1)
                #nb = numpy.roll(na,1,axis=1)
                #nc = numpy.roll(na,2,axis=1)
                #ng = numpy.arccos( (na*na+nb*nb-nc*nc)/(2*na*nb) )
                # Now we have the problem of assigning these angles to the vertices.


                for t in self.triangles:
                    u = [ radius[t[i]] for i in range(3) ]
                    ac = _tri(u)
                    for i in range(3):
                        angle[t[i]] += ac[i]

                for c in itcirc:
                    r = _adj(c,angle[c],neighbours[c],delta[c],radius[c])
                    if abs(r-radius[c]) > SurfaceComplex.error:
                        packing = False
                    radius[c] = r

            self.radius = radius

    def packing_accelerated(self):
        """This implements the Uniform Neighbour Model in

        A Circle Packing Algorithm by Charles R. Collins & Ken Stephenson

        (using the acceleration scheme).
        """
        if self.geometry == 'Euclidean':
            _tri   = euc_tri01
            _adj   = euc_adj
        elif self.geometry == 'hyperbolic':
            _tri   = hyp_tri01
            _adj   = hyp_adj
        else:
            raise RuntimeError, "This can't happen."

        circles = self.Vcircles + self.Ecircles + self.Fcircles
        radius_new = { x:SurfaceComplex.er for x in circles }

        for c in self.Vcircles:
            if c.boundary:
                radius_new[c] = SurfaceComplex.vr

        # Dictionary for number of neighbours
        neighbours = dict([ (c,len([ t for t in self.triangles if c in t ])) for c in circles])
        mx = max( n for n in neighbours.values() )

        # Dictionary for number used for correction.
        # This is delta in Stephenson's notation.
        delta = dict([ (c,sin(c.angle/(2*neighbours[c])))
                       for c in circles if not c.boundary ])

        #if int_circles != circles: # Dirichlet boundary conditions
        #    itcirc = [ c for c in circles if not c.boundary ]
        #else: # von Neumann boundary conditions
        itcirc = circles[1:]

        angle = {}
        error_new = 1 + SurfaceComplex.error
        lambda_new = -1
        flag_new = False

        packing = False
        count = 0
        while not packing:
            count += 1
            error_old  = error_new
            lambda_old = lambda_new
            flag_old   = flag_new
            radius_old = radius_new

            for c in circles:
                angle[c] = 0.0
            
            for t in self.triangles:
                u = [ radius_old[t[i]] for i in range(3) ]
                ac = _tri(u)
                for i in range(3):
                    angle[t[i]] += ac[i]

            total = 0
            for c in circles:
                ae = c.angle - angle[c]
                total += ae*ae
            error_new = sqrt(total)
            packing = error_new < SurfaceComplex.error

            radius_new = {circles[0]:SurfaceComplex.vr}

            for c in itcirc:
                radius_new[c] = _adj(c,angle[c],neighbours[c],delta[c],radius_old[c])

            lambda_new = error_new / error_old
            flag_new = True

            if flag_old and lambda_new < 1:
                error_new *= lambda_new
                if abs( lambda_new - lambda_old ) < SurfaceComplex.tolerance:
                    lambda_new = lambda_new / (1-lambda_new)
                lambda_max = min( radius_new[c] / (radius_old[c]-radius_new[c])
                        for c in itcirc if radius_old[c] > radius_new[c] )
                lambda_new = min( lambda_new, lambda_max * 0.5 )
                for c in itcirc:
                    r = radius_new[c]
                    radius_new[c] = r + lambda_new * (r-radius_old[c])
                flag_new = False

        self.radius = radius_new

    def edge(self):

        circles = self.Vcircles + self.Ecircles + self.Fcircles

        if not hasattr(self,'radius'):
            #self.packing_basic()
            self.packing_accelerated()
        radius = self.radius

        centre = {c:None for c in circles}

        if self.boundary_condition == 'Dirichlet':
            #Set first two centres
            u = self.outside[0]
            tr = [ t for t in self.triangles if t[3] and u in t[0].halfedges ][0]
            centre[tr[0]] = complex(0)
            centre[tr[1]] = complex(radius[tr[0]]+radius[tr[1]])

        elif self.boundary_condition == 'Neumann':
            ##Set boundary centres
            #pos = self.rim()
            #for x in pos:
            #    centre[x] = pos[x]
            u = self.outside[0]
            tr = [ t for t in self.triangles if t[3] and u in t[0].halfedges ][0]
            centre[tr[0]] = complex(0)
            centre[tr[1]] = complex(radius[tr[0]]+radius[tr[1]])

        else:
            raise RuntimeError, "Not yet implemented."

        self.centre = centre

    def layout(self):
        circles = self.Vcircles + self.Ecircles + self.Fcircles
        #Place the remaining circles
        if not hasattr(self,'centre'):
            self.packing_accelerated()

        def euc_place(x,t):
            z, w = centre[x[0]], centre[x[1]]
            r, s = radius[x[0]], radius[x[1]]
            #t = radius[tri[i]]
            theta = acos( 1 - 2*s*t/((r+s)*(r+t)) )
            return rect((r+t)/(r+s),theta)*(w-z)+z

        def hyp_place(x):
            raise NotImplementedError, "Hyperbolic geometry has not been implemented."

        if self.geometry == 'Euclidean':
            _place = euc_place
        elif self.geometry == 'hyperbolic':
            _place = hyp_place
        else:
            raise RuntimeError, "This can't happen."


        radius = self.radius
        if not hasattr(self,'centre'):
            self.edge()

        centre = self.centre
        
        done = False
        while not done:
            done = True
            for tri in self.triangles:
                pt = [ tri[i] for i in xrange(3) ]
                pc = [ centre[a] for a in pt ]
                if pc.count(None) == 1:
                    done = False
                    i = pc.index(None)
                    if tri[3]:
                        x = (pt[i-1],pt[i-2])
                    else:
                        x = (pt[i-2],pt[i-1])
                    t = radius[tri[i]]
                    centre[tri[i]] = _place(x,t)

        self.centre = centre

        #rimpos = self.rim()

        #print max( abs(centre[x]-rimpos[x]) for x in rimpos.keys() )
        #print max( abs(centre[x])-abs(rimpos[x]) for x in rimpos.keys() )

        self.bbox = ( min([ centre[c].real for c in circles ]),\
                      min([ centre[c].imag for c in circles ]),\
                      max([ centre[c].real for c in circles ]),\
                      max([ centre[c].imag for c in circles ]) )

    def conjgrad(self):
        """This is an iterative procedure for finding the positions
        of the centres of the circles. This implements the conjugate
        gradient method as described on the wikipedia page.

        The idea is that once the boundary circles are placed the
        positions of the remaining circles are the solution to a linear
        equation. This follows from the harmonic property described in
        'Circle packing'."""
        # x, r, p, Ap are vectors stored as dictionaries.

        circles = self.Vcircles + self.Ecircles + self.Fcircles
        int_circles = [ c for c in circles if not c.boundary ]

        if not hasattr(self,'centre'):
            self.rim()
            self.layout()
        x = self.centre

        # Construct neighbours with cyclic ordering.
        
        def multiply(v):
            # Calculates A * v for a vector v
            u = { c:0 for c in int_circles }
            # Do a sum over edges
            return u

        def transition(u,v,a,b):
            """This is (90) on page 237 of 'Circle Packing'."""
            s = u+v
            return (sqrt(u*v)/s)*(sqrt(a/(s+a))+sqrt(b/(s+b)))
        
        Ax = multiply(x)
        # b has not been defined
        r = { c:b[c]-Ax[c] for c in int_circles }
        p = r
        rsold = sum( a*a for a in r.values() )
        while rsold > error:
            Ap = multiply(p)
            alpha = rsold / sum( p[c]*Ap[c] for c in int_circles )
            x = { c:x[c]+alpha*p[c] for c in int_circles }
            r = { c:r[c]-alpha*Ap[c] for c in int_circles }
            rsnew = sum( a*a for a in r.values() )
            rs = rsnew / rsold
            p = { c:r[c]+rs*p[c] for c in int_circles }
            rsold = rsnew
        return x
    
    def report(self):
        """
        EXAMPLES:

        g = spider.RibbonGraph.polygon(5)
        SurfaceComplex(g.closure()).report()

        """
        if not hasattr(self, 'centre'):
            self.layout()

        #for a in self.Vcircles:
            #vc = set([ x.decorations.colour for x in a.halfedges ])
            #if 'None' not in vc and 'black' not in vc:
            #    print "Ramification index: %s, Centre: %3.5f %3.5f\nColours: %s" \
            #      % (len(a.halfedges), self.centre[a].real, self.centre[a].imag, vc)

        #print "*******************"

        print "["
        for a in self.Vcircles:
            if set([ x.decorations.colour for x in a.halfedges ]) == set(['green', 'red']):
                #print "Ramification index: %s, Centre: %3.5f %3.5f" \
                # % (len(a.halfedges)/2, self.centre[a].real, self.centre[a].imag)
                print "[ %s, %3.5f, %3.5f]," \
                 % (len(a.halfedges)/2, self.centre[a].real, self.centre[a].imag)
        print "]\n"
        #print "*******************"

        print "["
        for a in self.Vcircles:
            if set([ x.decorations.colour for x in a.halfedges ]) == set(['blue', 'red']):
                #print "Ramification index: %s, Centre: %3.5f %3.5f" \
                # % (len(a.halfedges)/2, self.centre[a].real, self.centre[a].imag)
                print "[ %s, %3.5f, %3.5f]," \
                 % (len(a.halfedges)/2, self.centre[a].real, self.centre[a].imag)
        print "]\n"

        #print "*******************"
        print "["
        for a in self.Vcircles:
            if set([ x.decorations.colour for x in a.halfedges ]) == set(['green', 'blue']):
                #print "Ramification index: %s, Centre: %3.5f %3.5f" \
                # % (len(a.halfedges)/2, self.centre[a].real, self.centre[a].imag)
                print "[ %s, %3.5f, %3.5f]," \
                 % (len(a.halfedges)/2, self.centre[a].real, self.centre[a].imag)
        print "]\n"
       # print "*******************"

    def transform(self,z):
        b = self.bbox
        scale = 400 / max(b[2]-b[0],b[3]-b[1])
        midpoint = complex(b[0]+b[2],b[1]+b[3])/2
        shift = complex(250,250)
        w = (z-midpoint) * scale + shift
        return  w.real, w.imag


    def show(self, style='SVG', options=None, name=None):
        """Draw a surface complex.

        INPUT: A SurfaceComplex

        OUTPUT: None

        EXAMPLES:

        >>> g = spider.RibbonGraph.polygon(5).closure()
        >>> SurfaceComplex(g).show('Tk','pentagon')

        >>> f = spider.RibbonGraph.vertex(4)
        >>> g = spider.RibbonGraph.vertex(3)
        >>> spider.glue(f,g,0).show('Tk')

        g = spider.RibbonGraph.polygon(5).closure()
        SurfaceComplex(g).show('SVG')

        g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
        SurfaceComplex(g).show('Tk',withcircles=True)

        g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
        g.show('SVG',withcircles=True)

        g = knots.LinkDiagram.from_DT(knots.DT([8,10,2,12,4,6]))
        g.show('SVG',withcircles=True,withradicalcircles=True)

        """
        if not hasattr(self, 'centre'):
            self.layout()

        if style == 'Tk':
            grph = graphics.Tk(name)
        if style == 'SVG':
            grph = graphics.SVG(name)
        if style == 'PS':
            grph = graphics.Postscript(name)
        if style == 'Tikz':
            grph = graphics.Tikz(name)
        if style == 'MP':
            grph = graphics.Metapost(name)
        if style == 'Matplot':
            grph = graphics.Matplotlib(name)
        if style == 'html':
            grph = graphics.HTML5(name)


        if self.options['graph']:
            grph.draw_graph(self)

        if self.options['circles']:
            grph.draw_circles(self)

        if self.options['medial']:
            grph.draw_medial(self)

        if self.options['triangles']:
            grph.draw_triangles(self)

        if self.options['radicalcircles']:
            grph.draw_radicalcircles(self)

        grph.close()

    def __latex__(self):
        self.show('Tikz','stdout')

# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()
