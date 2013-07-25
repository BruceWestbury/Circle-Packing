
#*****************************************************************************
#       Copyright (C) 2013 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

"""This is the module that does the actual drawing."""

import sys
import Tkinter
import webbrowser

class DrawClosedGraph():
    """
    A graphical drawing tool for drawing a link diagram.

    """
    def __init__(self, root=None, title='Link Drawing'):
        self.title=title
        if root is None:
            self.window = Tkinter.Tk()
        else:
            self.window = Tkinter.Toplevel(root)
        self.window.title(title)
        # Frame and Canvas
        self.frame = Tkinter.Frame(self.window,
                               borderwidth=0,
                               relief=Tkinter.FLAT,
                               background='#dcecff')
        self.canvas = Tkinter.Canvas(self.frame,
                                 bg='#dcecff',
                                 width=500,
                                 height=500,
                                 highlightthickness=0)
        self.button_frame = Tkinter.Frame(self.window,
                           borderwidth=2,
                           relief=Tkinter.FLAT,
                           background='#dcecff')
        def done(event):
            self.window.destroy()

        self.window.bind_all("<space>",done)
        self.frame.pack(padx=0, pady=0, fill=Tkinter.BOTH, expand=Tkinter.YES)
        self.canvas.pack(padx=0, pady=0, fill=Tkinter.BOTH, expand=Tkinter.YES)
        self.button_frame.pack(padx=0, pady=0, fill=Tkinter.X, expand=Tkinter.NO,
                            side=Tkinter.BOTTOM)


        done = Tkinter.Button(self.button_frame, text="Quit", command=self.window.destroy)
        done.pack(expand=1, side=Tkinter.LEFT)


class Graphics():
    """This is an abstract class. There is a class which implements
    this for each type of output.

    """    
    def __init__(self, name):
        raise NotImplementedError

    def line(self, x0, y0, x1, y1, colour, arrow):
        """Draws a line from (x0,y0) to (x1,y1).
        If arrow is true then there is an arrwhead at the end of the line.
        """
        raise NotImplementedError

    def circle(self, x, y, r, colour):
        """Draws a circle with centre (x,y), radius r.
        """
        raise NotImplementedError

    def polygon(self, p, colour):
        """Draws a polygon filled with colour.
        """
        raise NotImplementedError

    def close(self):
        """Actions to be carried out after drawing.
        """
        raise NotImplementedError

    def draw_graph(self,g):
        """Draws the ribbon graph."""

        def connect(u,v):
            a = v.halfedges.intersection(u.halfedges)
            if len(a) != 1:
                raise RuntimeError
            ft = set(a).pop().decorations
            w = g.centre[v]
            if ft.over:
                z = g.centre[u]
            else:
                z = 0.8*g.centre[u] + 0.2*w
            x = g.transform(z)
            y = g.transform(w)
            self.line(x[0], x[1], y[0], y[1],  ft.colour, ft.directed == 'tail')

        for tri in g.triangles:
            if tri[3]:
                connect(tri[0],tri[1])
            elif (tri[0].boundary and tri[1].boundary) or tri[1].type == 'BE':
                connect(tri[0],tri[1])

    def draw_circles(self,g):
        """Draws the circles in the circle packing."""

        circles = g.Vcircles + g.Ecircles + g.Fcircles

        for c in circles:
            z = g.centre[c]
            r = g.radius[c]
            x = g.transform(z)
            scale = g.transform(1)[0]-g.transform(0)[0]
            self.circle(x[0], x[1], r*scale, 'yellow')

    def draw_medial(self, g):
        """Draws a filled polygon in each face."""

        for c in g.Fcircles:
            if len(c.halfedges) > 2:
                p = []
                for a in c.halfedges:
                    x = [ cr for cr in g.Ecircles if  a in cr.halfedges ]
                    p.append(g.transform(g.centre[x[0]]))
                self.polygon(p, 'purple')
            elif  len(c.halfedges) == 2:
                x0 = [ cr for cr in g.Ecircles if  list(c.halfedges)[0] in cr.halfedges ]
                x1 = [ cr for cr in g.Ecircles if  list(c.halfedges)[1] in cr.halfedges ]
                z0 = g.transform(g.centre[x0[0]])
                z1 = g.transform(g.centre[x1[0]])
                self.line(z0[0], z0[1], z1[0], z1[1], 'purple', False)

    def draw_triangles(self, g):
        """Draws the triangles in the triangulation."""

        for tri in g.triangles:
            p = g.transform(g.centre[tri[0]]) +\
                g.transform(g.centre[tri[1]]) +\
                g.transform(g.centre[tri[2]])
            if tri[3]:
                self.polygon(p, 'blue' )
            else:
                self.polygon(p, 'green' )

    def draw_radicalcircles(self, g):
        """Draws the radical circle of each triangle."""

        def modulus(z):
            return (z*z.conjugate()).real

        for tri in g.triangles:
            p = [ g.centre[tri[i]] for i in range(3) ]
            r = [ g.radius[tri[i]] for i in range(3) ]
            M11 = p[1].real-p[0].real
            M12 = p[1].imag-p[0].imag
            M21 = p[2].real-p[1].real
            M22 = p[2].imag-p[1].imag
            c = [ (modulus(p[i]) - r[i]**2)*(0.5) for i in range(3) ]
            det = M11*M22 - M12*M21
            x = M22*(c[1]-c[0]) - M12*(c[2]-c[1])
            y = -M21*(c[1]-c[0]) + M11*(c[2]-c[1])
            z = complex(x,y)/det
            rho = sqrt( modulus(p[1]-z) - r[1]**2 )
            x, y = g.transform(z)
            scale = g.transform(1)[0]-g.transform(0)[0]
            self.circle(x, y, scale*rho, 'red')


class Tk(Graphics):
    def __init__(self, name):
        self.output = DrawClosedGraph()
        # Put name in title

    def line(self, x0, y0, x1, y1, colour, arrow):
        if arrow:
            self.output.canvas.create_line( x0, y0, x1, y1, fill=colour, arrow=Tkinter.LAST )
        else:
            self.output.canvas.create_line( x0, y0, x1, y1, fill=colour, arrow=Tkinter.NONE )

    def circle(self, x, y, r, colour):
        self.output.canvas.create_oval( x-r, y-r, x+r, y+r, outline=colour )

    def polygon(self, p, colour):
        self.output.canvas.create_polygon( *p, fill=colour )

    def close(self):
        self.output.window.mainloop()


class SVG(Graphics):
    def __init__(self, name):
        if name == 'stdout':
            output = sys.stdout
        elif name == None:
            output = open("diagram.svg", 'w')
        else:
            # Should parse and look at extension, paths etc.
            output = open(name,'w')
        self.output = output

        output.write("<html>\n")
        output.write("<body>\n\n")
        output.write("<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\"")
        output.write(" width=\"500\" height=\"500\">\n\n")
        output.write("<title>A Link Diagram</title>\n")
        output.write("<desc>A link diagram produced using circle packing.</desc>\n\n")

        # This is for arrow heads.
        output.write("<defs>\n")
        output.write("  <marker id=\"Arrow\" markerWidth=\"5\" markerHeight=\"10\"\n")
        output.write("    refX=\"5\" refY=\"5\" orient=\"auto\">\n")
        output.write("    <path d=\"M 0 0 5 5 0 10 Z\" style=\"fill: blue;\"/>\n")
        output.write("  </marker>\n")
        output.write("</defs>\n")

    def line(self, x0, y0, x1, y1, colour, arrow):
        line = "<line x1=\"%f\" y1=\"%f\" x2=\"%f\" y2=\"%f\""\
                          % ( x0, y0, x1, y1 )
        self.output.write(line)
        if arrow:
            self.output.write( " style = \"stroke: %s ; marker-end: url(\#Arrow);\"/>\n" % colour )
        else:
            self.output.write( " style = \"stroke: %s ;\"/>\n" % colour )

    def circle(self, x, y, r, colour):
        line = "<circle cx=\"%f\" cy=\"%f\" r=\"%f\" stroke=\"%s\" fill=\"none\" />\n"\
               % (x, y, r, colour)
        self.output.write(line)

    def polygon(self, p, colour):
        pass

    def close(self):
        self.output.write("</svg>\n\n")
        self.output.write("</body>\n")
        self.output.write("</html>")

        if self.output != sys.stdout:
            self.output.close()
            webbrowser.open("diagram.svg")

# The manual for Version 2.00 can be found at
# http://www.ctan.org/tex-archive/graphics/pgf/base/doc/generic/pgf/pgfmanual.pdf
class Tikz(Graphics):
    def __init__(self, name):
        if name == 'stdout':
            output = sys.stdout
        elif name == None:
            output = open("diagram.tex", 'w')
        else:
            # Should parse and look at extension, paths etc.
            output = open(name,'w')
        self.output = output
        output.write("\\begin{tikzpicture}\n")

    def line(self, x0, y0, x1, y1, colour, arrow):
        if arrow:
            self.output.write("\\draw [->] (%f,%f) -- (%f,%f);\n"  %( x0, y0, x1, y1 ) )
        else:
            self.output.write("\\draw (%f,%f) -- (%f,%f);\n" % ( x0, y0, x1, y1 ) )

    def circle(self, x, y, r, colour):
        self.output.write("\\draw (%f,%f) circle %f;" % ( x, y, r ) )

    def polygon(self, p, colour):
        # Use -- cycle at the end
        pass

    def close(self):
        self.output.write("\\end{tikzpicture}\n")
        if self.output != sys.stdout:
            self.output.close()


# The file contains BoundingBox and DSC comment
# First line is %!PS
# An introduction to the language can be found at
# http://www.tailrecursive.org/postscript/postscript.html
class Postscript(Graphics):
    def __init__(self, name):
        if name == 'stdout':
            output = sys.stdout
        elif name == None:
            output = open("diagram.eps", 'w')
        else:
            # Should parse and look at extension, paths etc.
            output = open(name,'w')
        self.output = output

    def line(self, x0, y0, x1, y1, colour, arrow):
        # x0 y0 moveto x1 y1 lineto stroke
        pass

    def circle(self, x, y, r, colour):
        # newpath x0 y0 r 0 360 arc closepath
        # newpath x0 y0 r 0 360 arc closepath fill
        pass

    def polygon(self, p, colour):
        # End with closepath
        pass

    def close(self):
        if self.output != sys.stdout:
            self.output.close()

# The manual is at http://www.tug.org/docs/metapost/mpman.pdf
class Metapost(Graphics):
    count = 0
    def __init__(self, name):
        count += 1
        if name == 'stdout':
            output = sys.stdout
        elif name == None:
            output = open("diagram.mp", 'a')
        else:
            # Should parse and look at extension, paths etc.
            output = open(name,'w')
        self.output = output
        output.write("beginfig(%d)\n" % count)


    def line(self, x0, y0, x1, y1, colour, arrow):
        # draw (x0,y0) -- (x1,y1)
        pass

    def circle(self, x, y, r, colour):
        # p = fullcircle scaled r shifted (x0,y0)
        pass

    def polygon(self, p, colour):
        # p = (x0,y0) -- (x1,y1) -- ... -- cycle
        # fill p with color <colour>
        #
        # draw p
        pass

    def close(self):
        output.write("endfig;\n\n")
        if self.output != sys.stdout:
            self.output.close()


# The online manual can be found at
# http://matplotlib.sourceforge.net/users/index.html
#
# import matplotlib.pyplot as plt
# plt.figure(1)
class Matplotlib(Graphics):
    def __init__(self, name):
        pass

    def line(self, x0, y0, x1, y1, colour, arrow):
        pass

    def circle(self, x, y, r, colour):
        pass

    def polygon(self, p, colour):
        pass

    def close(self):
        pass

class HTML5(Graphics):
    def __init__(self, name):
        pass

    def line(self, x0, y0, x1, y1, colour, arrow):
        pass

    def circle(self, x, y, r, colour):
        pass

    def polygon(self, p, colour):
        pass

    def close(self):
        pass



# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()
