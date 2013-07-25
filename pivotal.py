
#!/usr/bin/env python

#*****************************************************************************
#       Copyright (C) 2011 Bruce Westbury Bruce.Westbury@warwick.ac.uk
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

"""
Implementation of pivotal categories. This uses ribbon graphs to implement
pivotal categories. The morphisms are ribbon graphs with boundary divided
into input and output.

The function compose() defines a category (with the identity morphisms implicit.
The function tensor() makes this a strict monoidal category. The four raising
and lowering functions then make this a strict pivotal category.

In any strict monoidal category the objects form a monoid under tensor product.
In these strict monoidal categories this monoid is a free monoid.
In any strict pivotal category this is a monoid with an anti-involution.
In this examples the anti-involution is given by defining an involution
on the generators and then extending to an anti-homomorphism.

AUTHOR:

- Bruce Westbury (2011-08-03): initial version

"""

__all__ = [ 'Morphism', 'Artin_generator' ]

import ribbon
import spider


class Morphism():
    """This is the class of morphisms in the category."""
    def __init__(self, jg, do, co):
        if not set(do).issubset(jg.he):
            raise ValueError
        if not set(co).issubset(jg.he):
            raise ValueError

        self.domain = tuple(do)
        self.codomain = tuple(co)
        self.graph = jg


    @property
    def web(self):
        """Construct a ribbon graph from a morphism.

        EXAMPLE:

        >>> g = spider.RibbonGraph.polygon(5)
        >>> m = g.morphism(2,3)
        >>> m.web # doctest:+ELLIPSIS
        <spider.RibbonGraph object at 0x...>

        """
        a = list(self.codomain)
        a.reverse()
        bd = self.domain + tuple(a)
        return spider.RibbonGraph(self.graph, bd)

    def show(self, style, name=None):
        n = len(self.domain)
        m = len(self.codomain)
        self.web.closure(bv=[n,0,m,0]).show(style, name)

    def copy(self):
        """Copies a morphism.

        EXAMPLE:

        >>> g = spider.RibbonGraph.polygon(6)
        >>> om = g.morphism(3,3)
        >>> om.copy() # doctest:+ELLIPSIS
        <pivotal.Morphism instance at 0x...>
        """
        phi = self.graph.copy()
        h = phi.codomain
        do = [ phi.map[a] for a in self.domain ]
        co = [ phi.map[a] for a in self.codomain ]
        return Morphism(h,do,co)

    def compose(self,other):
        """Composition of morphisms.

        INPUT: Two morphisms

        OUTPUT: A morphism

        EXAMPLES:

        >>> s1 = Artin_generator(3,1)
        >>> s2 = Artin_generator(3,2)
        >>> s1.compose(s2) # doctest:+ELLIPSIS
        <__main__.Morphism instance at 0x...>

        >>> s1 = Artin_generator(3,1)
        >>> t1 = Artin_generator(3,-1)
        >>> s1.compose(t1) # doctest:+ELLIPSIS
        <__main__.Morphism instance at 0x...>

        """

        if len(self.codomain) != len(other.domain):
            raise ValueError

        sm = self.copy()
        om = other.copy()
        jg = ribbon.justgraph(sm.graph.he.union(om.graph.he))
        for u, v in zip(sm.codomain,om.domain):
            jg.stitch(u, v)
        jg.normal()
        return Morphism(jg,sm.domain,om.codomain)

    def __mul__(self,other):
        return self.compose(other)

    def tensor(self,other):
        """Tensor product of morphisms.

        INPUT: Two morphisms

        OUTPUT: A morphism

        EXAMPLES:

        """
        sm = self.copy()
        om = other.copy()
        jg = justgraph(sm.jg.he.union(om.jg.he))

        domain = self.domain + other.domain
        codomain = self.codomain + other.codomain
        return morphism(jg, domain, codomain)

    def __xor__(self, other):
        return tensor(self,other)

    def raise_left(self):
        """Raising operator applied on left of morphism.

        INPUT: A morphism

        OUTPUT: A morphism

        EXAMPLES:

        """

        if self.codomain == []:
            raise ValueError
        sm = self.copy()
        co = list(self.codomain)
        do = list(self.domain)
        a = co.pop(0)
        return morphism(sm.jg, do.insert(0,a),co)

    def raise_right(self):
        """Raising operator applied on right of morphism.

        INPUT: A morphism

        OUTPUT: A morphism

        EXAMPLES:

        """

        if self.codomain == []:
            raise ValueError
        sm = self.copy()
        co = list(self.codomain)
        do = list(self.domain)
        a = co.pop(len(do)-1)
        return morphism(sm.jg, do.append(a),co)

    def lower_left(self):
        """Lowering operator applied on left of morphism.

        INPUT: A morphism

        OUTPUT: A morphism

        EXAMPLES:

        """

        if self.domain == []:
            raise ValueError
        sm = self.copy()
        co = list(sm.codomain)
        do = list(sm.domain)
        a = do.pop(0)
        return morphism(sm.jg, do, co.insert(0,a))


    def lower_right(self):
        """Lowering operator applied on right of morphism.

        INPUT: A morphism

        OUTPUT: A morphism

        EXAMPLES:

        """

        if self.domain == []:
            raise ValueError
        sm = self.copy()
        co = list(sm.codomain)
        do = list(sm.domain)
        a = do.pop(len(do)-1)
        return morphism(sm.jg, do, co.append(a))

    def dual(self):
        sm = self.copy()
        return(sm.jg, sm.codomain.reverse(), sm.domain.reverse())


def Artin_generator(n,k):
    """Constructs the Artin generator s_k of n string braif group.

    INPUT: n a positive integer, k an integer with 0 < |k| < n

    OUTPUT: A Morphism

    >>> s1 = Artin_generator(3,1)
    >>> s2 = Artin_generator(3,2)
    """
    if not 0 < abs(k) < n:
        raise ValueError

    # These are also defined in knots.py
    in_over = ribbon.Features('head','blue',True)
    in_under = ribbon.Features('head','blue',False)
    out_over = ribbon.Features('tail','blue',True)
    out_under = ribbon.Features('tail','blue',False)

    r = range(n)
    do = [ ribbon.halfedge() for i in r ]
    co = [ ribbon.halfedge() for i in r ]
    for a in do:
        a.decorations = in_over
        a.IsI = True
    for a in co:
        a.decorations = out_over
        a.IsI = True
    for i in r:
        do[i].c = co[i]
        co[i].c = do[i]
        
    p =abs(k)
    do[p-1].IsI = False
    do[p].IsI = False
    co[p-1].IsI = False
    co[p].IsI = False
    do[p-1].c = do[p]
    do[p].c = co[p]
    co[p].c = co[p-1]
    co[p-1].c = do[p-1]

    if k > 0:
        do[k-1].decorations = in_over
        do[k].decorations = in_under
        co[k-1].decorations = out_under
        co[k].decorations = out_over
    elif k < 0:
        do[p-1].decorations = in_under
        do[p].decorations = in_over
        co[p-1].decorations = out_over
        co[p].decorations = out_under
    else:
        raise RuntimeError

    g = ribbon.justgraph( set(do+co) )
    return Morphism(g, do, co)


def braid(word):
    """Constructs a braid diagram from a word.

    INPUT: A list of non-zero integers

    OUTPUT: A Morphism

    EXAMPLES:

    >>> braid([1]) #doctest: +ELLIPSIS
    <__main__.Morphism instance at 0x...>

    """

    m = max( map(abs, word) )
    A = map( lambda i: Artin_generator(m+1,i), word )
    def prod(f,g):
        return f.compose(g)
    return reduce( prod, A )
    

# This is to run the tests in the examples.
# http://docs.python.org/library/doctest.html
if __name__ == "__main__":
    import doctest
    doctest.testmod()



