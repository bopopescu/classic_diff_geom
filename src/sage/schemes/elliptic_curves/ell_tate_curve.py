r"""
Tate's parametrisation of `p`-adic curves with multiplicative reduction

Let `E` be an elliptic curve defined over the `p`-adic numbers `\QQ_p`.
Suppose that `E` has multiplicative reduction, i.e. that the `j`-invariant
of `E` has negative valuation, say `n`. Then there exists a parameter
`q` in `\ZZ_p` of valuation `n` such that the points of `E` defined over
the algebraic closure `\bar{\QQ}_p` are in bijection with
`\bar{\QQ}_p^{\times}\,/\, q^{\ZZ}`. More precisely there exists
the series `s_4(q)` and `s_6(q)` such that the
`y^2+x y = x^3 + s_4(q) x+s_6(q)` curve is isomorphic to `E` over
`\bar{\QQ}_p` (or over `\QQ_p` if the reduction is *split* multiplicative). There is `p`-adic analytic map from
`\bar{\QQ}^{\times}_p` to this curve with kernel `q^{\ZZ}`.
Points of good reduction correspond to points of valuation
`0` in `\bar{\QQ}^{\times}_p`.
See chapter V of [Sil2] for more details.

REFERENCES :

- [Sil2] Silverman Joseph, Advanced Topics in the Arithmetic of Elliptic Curves,
   GTM 151, Springer 1994.


AUTHORS:

- chris wuthrich (23/05/2007): first version

- William Stein (2007-05-29): added some examples; editing.

- chris wuthrich (04/09): reformatted docstrings.

"""

######################################################################
#       Copyright (C) 2007 chris wuthrich
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
######################################################################

from sage.rings.integer_ring import ZZ
from sage.rings.padics.factory import Qp
from sage.structure.sage_object import SageObject
from sage.rings.arith import LCM
from sage.modular.modform.constructor import EisensteinForms, CuspForms
from sage.schemes.elliptic_curves.constructor import EllipticCurve
from sage.misc.functional import log
from sage.misc.all import denominator, prod
import sage.matrix.all as matrix

class TateCurve(SageObject):
    r"""
    Tate's `p`-adic uniformisation of an elliptic curve with
    multiplicative reduction.

    .. note::

       Some of the methods of this Tate curve only work when the
       reduction is split multiplicative over `\QQ_p`.

    EXAMPLES::

        sage: e = EllipticCurve('130a1')
        sage: eq = e.tate_curve(5); eq
        5-adic Tate curve associated to the Elliptic Curve defined by y^2 + x*y + y = x^3 - 33*x + 68 over Rational Field
        sage: eq == loads(dumps(eq))
        True

    REFERENCES :

    - [Sil2] Silverman Joseph, Advanced Topics in the Arithmetic of Elliptic Curves,
      GTM 151, Springer 1994.

    """
    def __init__(self,E,p):
        r"""
        INPUT:

        - ``E`` - an elliptic curve over the rational numbers

        - ``p`` - a prime where `E` has multiplicative reduction,
                 i.e., such that `j(E)` has negative valuation.

        EXAMPLES::

            sage: e = EllipticCurve('130a1')
            sage: eq = e.tate_curve(2); eq
            2-adic Tate curve associated to the Elliptic Curve defined by y^2 + x*y + y = x^3 - 33*x + 68 over Rational Field
        """
        if not p.is_prime():
            raise ValueError("p (=%s) must be a prime"%p)
        if E.j_invariant().valuation(p) >= 0:
            raise ValueError("The elliptic curve must have multiplicative reduction at %s"%p)
        self._p = ZZ(p)
        self._E = E
        self._q = self.parameter()

    def __cmp__(self, other):
        r"""
        Compare self and other.

        TESTS::

            sage: E = EllipticCurve('35a')
            sage: eq5 = E.tate_curve(5)
            sage: eq7 = E.tate_curve(7)
            sage: eq7 == eq7
            True
            sage: eq7 == eq5
            False
        """
        c = cmp(type(self), type(other))
        if c: return c
        return cmp((self._E, self._p), (other._E, other._p))


    def _repr_(self):
        r"""
        Return print representation.

        EXAMPLES::

            sage: e = EllipticCurve('130a1')
            sage: eq = e.tate_curve(2)
            sage: eq._repr_()
            '2-adic Tate curve associated to the Elliptic Curve defined by y^2 + x*y + y = x^3 - 33*x + 68 over Rational Field'
        """
        s = "%s-adic Tate curve associated to the %s"%(self._p, self._E)
        return s

    def original_curve(self):
        r"""
        Returns the elliptic curve the Tate curve was constructed from.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.original_curve()
            Elliptic Curve defined by y^2 + x*y + y = x^3 - 33*x + 68 over Rational Field
        """
        return self._E

    def prime(self):
        r"""
        Returns the residual characteristic `p`.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.original_curve()
            Elliptic Curve defined by y^2 + x*y + y = x^3 - 33*x + 68 over Rational Field
            sage: eq.prime()
            5
       """
        return self._p


    def parameter(self,prec=20):
        r"""
        Returns the Tate parameter `q` such that the curve is isomorphic
        over the algebraic closure of `\QQ_p` to the curve
        `\QQ_p^{\times}/q^{\ZZ}`.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.parameter(prec=5)
            3*5^3 + 3*5^4 + 2*5^5 + 2*5^6 + 3*5^7 + O(5^8)
        """
        try:
            qE = self._q
            if qE.absolute_precision() >= prec:
                return qE
        except AttributeError:
            pass

        jE = self._E.j_invariant()
        E4 = EisensteinForms(weight=4).basis()[0]
        Delta = CuspForms(weight=12).basis()[0]
        j = (E4.q_expansion(prec+3))**3/Delta.q_expansion(prec+3)
        jinv = (1/j).power_series()
        q_in_terms_of_jinv = jinv.reversion()
        R = Qp(self._p,prec=prec)
        qE = q_in_terms_of_jinv(R(1/self._E.j_invariant()))
        self._q = qE
        return qE

    __sk = lambda e,k,prec: sum( [n**k*e._q**n/(1-e._q**n) for n in range(1,prec+1)] )

    __delta = lambda e,prec: e._q* prod([(1-e._q**n)**24 for n in range(1,prec+1) ] )

    def curve(self,prec=20):
        r"""
        Returns the `p`-adic elliptic curve of the form `y^2+x y = x^3 + s_4 x+s_6`.
        This curve with split multiplicative reduction is isomorphic to the given curve
        over the algebraic closure of `\QQ_p`.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.curve(prec=5)
            Elliptic Curve defined by y^2 + (1+O(5^5))*x*y  = x^3 +
            (2*5^4+5^5+2*5^6+5^7+3*5^8+O(5^9))*x + (2*5^3+5^4+2*5^5+5^7+O(5^8)) over 5-adic
            Field with capped relative precision 5
        """
        try:
            Eq = self.__curve
            if Eq.a6().absolute_precision() >= prec:
                return Eq
        except AttributeError:
            pass


        qE = self.parameter(prec=prec)
        n = qE.valuation()
        precp = (prec/n).floor() + 2;
        R = qE.parent()

        tate_a4 = -5  * self.__sk(3,precp)
        tate_a6 = (tate_a4 - 7 * self.__sk(5,precp) )/12
        Eq = EllipticCurve([R(1),R(0),R(0),tate_a4,tate_a6])
        self.__curve = Eq
        return Eq

    def _Csquare(self,prec=20):
        r"""
        Returns the square of the constant `C` such that the canonical Neron differential `\omega`
        and the canonical differential `\frac{du}{u}` on `\QQ^{\times}/q^{\ZZ}` are linked by
        `\omega = C \frac{du}{u}`. This constant is only a square in `\QQ_p` if the curve has split
        multiplicative reduction.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq._Csquare(prec=5)
            4 + 2*5^2 + 2*5^4 + O(5^5)
        """
        try:
            Csq = self.__Csquare
            if Csq.absolute_precision() >= prec:
                return Csq
        except AttributeError:
            pass

        Eq = self.curve(prec=prec)
        tateCsquare = Eq.c6() * self._E.c4()/Eq.c4()/self._E.c6()
        self.__Csquare = tateCsquare
        return tateCsquare

    def E2(self,prec=20):
        r"""
        Returns the value of the `p`-adic Eisenstein series of weight 2 evaluated on the elliptic
        curve having split multiplicative reduction.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.E2(prec=10)
            4 + 2*5^2 + 2*5^3 + 5^4 + 2*5^5 + 5^7 + 5^8 + 2*5^9 + O(5^10)

            sage: T = EllipticCurve('14').tate_curve(7)
            sage: T.E2(30)
            2 + 4*7 + 7^2 + 3*7^3 + 6*7^4 + 5*7^5 + 2*7^6 + 7^7 + 5*7^8 + 6*7^9 + 5*7^10 + 2*7^11 + 6*7^12 + 4*7^13 + 3*7^15 + 5*7^16 + 4*7^17 + 4*7^18 + 2*7^20 + 7^21 + 5*7^22 + 4*7^23 + 4*7^24 + 3*7^25 + 6*7^26 + 3*7^27 + 6*7^28 + O(7^30)
        """

        p = self._p
        Csq = self._Csquare(prec=prec)
        qE = self._q
        n = qE.valuation()
        R = Qp(p,prec)

        e2 = Csq*(1 - 24 * sum( [ qE**i/(1-qE**i)**2 for i in range(1,(prec/n).floor() + 5) ]))

        return R(e2)


    def is_split(self):
        r"""
        Returns True if the given elliptic curve has split multiplicative reduction.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.is_split()
            True

            sage: eq = EllipticCurve('37a1').tate_curve(37)
            sage: eq.is_split()
            False
        """
        return self._Csquare().is_square()

    def parametrisation_onto_tate_curve(self,u,prec=20):
        r"""
        Given an element `u` in `\QQ_p^{\times}`, this computes its image on the Tate curve
        under the `p`-adic uniformisation of `E`.

        INPUT:

        - ``u`` - a non-zero `p`-adic number.

        - ``prec`` - the `p`-adic precision, default is 20.


        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.parametrisation_onto_tate_curve(1+5+5^2+O(5^10))
            (5^-2 + 4*5^-1 + 1 + 2*5 + 3*5^2 + 2*5^5 + 3*5^6 + O(5^7) :
            4*5^-3 + 2*5^-1 + 4 + 2*5 + 3*5^4 + 2*5^5 + O(5^6) : 1 + O(5^20))
        """
        if u == 1:
            return self.curve(prec=prec)(0)

        q = self._q
        un = u * q**(-(u.valuation()/q.valuation()).floor())

        precn = (prec/q.valuation()).floor() + 4

        # formulas in Silverman II (Advanced Topics in the Arithmetic of Elliptic curves, p. 425)

        xx = un/(1-un)**2 + sum( [q**n*un/(1-q**n*un)**2 + q**n/un/(1-q**n/un)**2-2*q**n/(1-q**n)**2 for n in range(1,precn) ])

        yy = un**2/(1-un)**3 + sum( [q**(2*n)*un**2/(1-q**n*un)**3 - q**n/un/(1-q**n/un)**3+q**n/(1-q**n)**2 for n in range(1,precn) ])

        return self.curve(prec=prec)( [xx,yy] )



    # From here on all function need that the curve has split multiplicative reduction.

    def L_invariant(self,prec=20):
        r"""
        Returns the *mysterious* `\mathcal{L}`-invariant associated
        to an elliptic curve with split multiplicative reduction. One
        instance where this constant appears is in the exceptional
        case of the `p`-adic Birch and Swinnerton-Dyer conjecture as
        formulated in [MTT]. See [Col] for a detailed discussion.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        REFERENCES:

        - [MTT] B. Mazur, J. Tate, and J. Teitelbaum,
          On `p`-adic analogues of the conjectures of Birch and
          Swinnerton-Dyer, Inventiones mathematicae 84, (1986), 1-48.

        - [Col] Pierre Colmez, Invariant `\mathcal{L}` et derivees de
          valeurs propores de Frobenius, preprint, 2004.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.L_invariant(prec=10)
            5^3 + 4*5^4 + 2*5^5 + 2*5^6 + 2*5^7 + 3*5^8 + 5^9 + O(5^10)
        """

        if not self.is_split():
               raise RuntimeError("The curve must have split multiplicative reduction")
        qE = self.parameter(prec=prec)
        n = qE.valuation()
        u = qE/self._p**n  # the p-adic logarithm of Iwasawa normalised by log(p) = 0
        return log(u)/n


    def _isomorphism(self,prec=20):
        r"""
        Returns the isomorphism between ``self.curve()`` and the given curve in the
        form of a list ``[u,r,s,t]`` of `p`-adic numbers. For this to exist
        the given curve has to have split multiplicative reduction over `\QQ_p`.

        More precisely, if `E` has coordinates `x` and `y` and the Tate curve
        has coordinates `X`, `Y` with `Y^2 + XY = X^3 + s_4 X +s_6` then
        `X = u^2 x +r` and `Y = u^3 y +s u^2 x +t`.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq._isomorphism(prec=5)
            [2 + 3*5^2 + 2*5^3 + 4*5^4 + O(5^5), 4 + 3*5 + 4*5^2 + 2*5^3 + O(5^5),
             3 + 2*5 + 5^2 + 5^3 + 2*5^4 + O(5^5), 2 + 5 + 3*5^2 + 5^3 + 5^4 + O(5^5)]
        """

        if not self.is_split():
            raise RuntimeError("The curve must have split multiplicative reduction")

        Csq = self._Csquare(prec=prec+4)
        C = Csq.sqrt()
        R = Qp(self._p,prec)
        C = R(C)
        s = (C * R(self._E.a1()) -R(1))/R(2)
        r = (C**2*R(self._E.a2()) +s +s**2)/R(3)
        t = (C**3*R(self._E.a3()) - r)/R(2)
        return [C,r,s,t]

    def _inverse_isomorphism(self,prec=20):
        r"""
        Returns the isomorphism between the given curve and ``self.curve()`` in the
        form of a list ``[u,r,s,t]`` of `p`-adic numbers. For this to exist
        the given curve has to have split multiplicative reduction over `\QQ_p`.

        More precisely, if `E` has coordinates `x` and `y` and the Tate curve
        has coordinates `X`, `Y` with `Y^2 + XY = X^3 + s_4 X +s_6` then
        `x = u^2 X +r` and `y = u^3 Y +s u^2 X +t`.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq._inverse_isomorphism(prec=5)
            [3 + 2*5 + 3*5^3 + O(5^5), 4 + 2*5 + 4*5^3 + 3*5^4 + O(5^5),
            1 + 5 + 4*5^3 + 2*5^4 + O(5^5), 5 + 2*5^2 + 3*5^4 + O(5^5)]
        """
        if not self.is_split():
            raise RuntimeError("The curve must have split multiplicative reduction")
        vec = self._isomorphism(prec=prec)
        return [1/vec[0],-vec[1]/vec[0]**2,-vec[2]/vec[0],(vec[1]*vec[2]-vec[3])/vec[0]**3]

    def lift(self,P, prec = 20):
        r"""
        Given a point `P` in the formal group of the elliptic curve `E` with split multiplicative reduction,
        this produces an element `u` in `\QQ_p^{\times}` mapped to the point `P` by the Tate parametrisation.
        The algorithm return the unique such element in `1+p\ZZ_p`.

        INPUT:

        - ``P`` - a point on the elliptic curve.

        - ``prec`` - the `p`-adic precision, default is 20.

        EXAMPLES::

            sage: e = EllipticCurve('130a1')
            sage: eq = e.tate_curve(5)
            sage: P = e([-6,10])
            sage: l = eq.lift(12*P, prec=10); l
            1 + 4*5 + 5^3 + 5^4 + 4*5^5 + 5^6 + 5^7 + 4*5^8 + 5^9 + O(5^10)

        Now we map the lift l back and check that it is indeed right.::

            sage: eq.parametrisation_onto_original_curve(l)
            (4*5^-2 + 2*5^-1 + 4*5 + 3*5^3 + 5^4 + 2*5^5 + 4*5^6 + O(5^7) : 2*5^-3 + 5^-1 + 4 + 4*5 + 5^2 + 3*5^3 + 4*5^4 + O(5^6) : 1 + O(5^20))
            sage: e5 = e.change_ring(Qp(5,9))
            sage: e5(12*P)
            (4*5^-2 + 2*5^-1 + 4*5 + 3*5^3 + 5^4 + 2*5^5 + 4*5^6 + O(5^7) : 2*5^-3 + 5^-1 + 4 + 4*5 + 5^2 + 3*5^3 + 4*5^4 + O(5^6) : 1 + O(5^9))
        """
        p = self._p
        R = Qp(self._p,prec)
        if not self._E == P.curve():
            raise ValueError("The point must lie on the original curve.")
        if not self.is_split():
            raise ValueError("The curve must have split multiplicative reduction.")
        if P.is_zero():
            return R(1)
        if P[0].valuation(p) >= 0:
            raise  ValueError("The point must lie in the formal group.")

        Eq = self.curve(prec=prec)
        isom = self._isomorphism(prec=prec)
        C = isom[0]
        r = isom[1]
        s = isom[2]
        t = isom[3]
        xx = r + C**2 * P[0]
        yy = t + s * C**2 * P[0] + C**3 * P[1]
        try:
            Pq = Eq([xx,yy])
        except Exception:
            raise RuntimeError("Bug : Point %s does not lie on the curve "%[xx,yy])

        tt = -xx/yy
        eqhat = Eq.formal()
        eqlog = eqhat.log(prec + 3)
        z = eqlog(tt)
        u = ZZ(1)
        fac = ZZ(1)
        for i in range(1,2*prec+1):
            fac = fac * i
            u = u + z**i/fac
        return u

    def parametrisation_onto_original_curve(self,u,prec=20):
        r"""
        Given an element `u` in `\QQ_p^{\times}`, this computes its image on the original curve
        under the `p`-adic uniformisation of `E`.

        INPUT:

        - ``u`` - a non-zero `p`-adic number.

        - ``prec`` - the `p`-adic precision, default is 20.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.parametrisation_onto_original_curve(1+5+5^2+O(5^10))
            (4*5^-2 + 4*5^-1 + 4 + 2*5^3 + 3*5^4 + 2*5^6 + O(5^7) :
            3*5^-3 + 5^-2 + 4*5^-1 + 1 + 4*5 + 5^2 + 3*5^5 + O(5^6) : 1 + O(5^20))

        Here is how one gets a 4-torsion point on `E` over `\QQ_5`::

            sage: R = Qp(5,10)
            sage: i = R(-1).sqrt()
            sage: T = eq.parametrisation_onto_original_curve(i); T
            (2 + 3*5 + 4*5^2 + 2*5^3 + 5^4 + 4*5^5 + 2*5^7 + 5^8 + 5^9 + O(5^10) :
            3*5 + 5^2 + 5^4 + 3*5^5 + 3*5^7 + 2*5^8 + 4*5^9 + O(5^10) : 1 + O(5^20))
            sage: 4*T
            (0 : 1 + O(5^20) : 0)
        """
        if not self.is_split():
            raise ValueError("The curve must have split multiplicative reduction.")
        P = self.parametrisation_onto_tate_curve(u,prec=20)
        isom = self._inverse_isomorphism(prec=prec)
        C = isom[0]
        r = isom[1]
        s = isom[2]
        t = isom[3]
        xx = r + C**2 * P[0]
        yy = t + s * C**2 * P[0] + C**3 * P[1]
        R = Qp(self._p,prec)
        E_over_Qp = self._E.base_extend(R)
        return E_over_Qp([xx,yy])



    __padic_sigma_square = lambda e,u,prec: (u-1)**2/u* prod([((1-e._q**n*u)*(1-e._q**n/u)/(1-e._q**n)**2)**2 for n in range(1,prec+1)])

    # the following functions are rather functions of the global curve than the local curve
    # we use the same names as for elliptic curves over rationals.

    def padic_height(self,prec=20):
        r"""
        Returns the canonical `p`-adic height function on the original curve.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        OUTPUT:

        - A function that can be evaluated on rational points of `E`.

        EXAMPLES::

            sage: e = EllipticCurve('130a1')
            sage: eq = e.tate_curve(5)
            sage: h = eq.padic_height(prec=10)
            sage: P=e.gens()[0]
            sage: h(P)
            2*5^-1 + 1 + 2*5 + 2*5^2 + 3*5^3 + 3*5^6 + 5^7 + O(5^8)

        Check that it is a quadratic function::

            sage: h(3*P)-3^2*h(P)
            O(5^8)
        """

        if not self.is_split():
            raise NotImplementedError("The curve must have split multiplicative reduction")

        p = self._p

        # we will have to do it properly with David Harvey's _multiply_point(E, R, Q)
        n = LCM(self._E.tamagawa_numbers()) * (p-1)

        # this function is a closure, I don't see how to doctest it (PZ)
        def _height(P,check=True):
            if check:
                assert P.curve() == self._E, "the point P must lie on the curve from which the height function was created"
            Q = n * P
            cQ = denominator(Q[0])
            uQ = self.lift(Q,prec = prec)
            si = self.__padic_sigma_square(uQ, prec=prec)
            nn = self._q.valuation()
            qEu = self._q/p**nn
            return -(log(si*self._Csquare()/cQ) + log(uQ)**2/log(qEu)) / n**2

        return _height


    def padic_regulator(self,prec=20):
        r"""
        Computes the canonical `p`-adic regulator on the extended Mordell-Weil group as in [MTT]
        (with the correction of [Wer] and sign convention in [SW].)
        The `p`-adic Birch and Swinnerton-Dyer conjecture
        predicts that this value appears in the formula for the leading term of the
        `p`-adic L-function.

        INPUT:

        - ``prec`` - the `p`-adic precision, default is 20.

        REFERENCES:

        - [MTT] B. Mazur, J. Tate, and J. Teitelbaum,
          On `p`-adic analogues of the conjectures of Birch and
          Swinnerton-Dyer, Inventiones mathematicae 84, (1986), 1-48.

        - [Wer] Annette Werner, Local heights on abelian varieties and rigid analytic unifomization,
          Doc. Math. 3 (1998), 301-319.

        - [SW] William Stein and Christian Wuthrich, Computations About Tate-Shafarevich Groups
          using Iwasawa theory, preprint 2009.

        EXAMPLES::

            sage: eq = EllipticCurve('130a1').tate_curve(5)
            sage: eq.padic_regulator()
            2*5^-1 + 1 + 2*5 + 2*5^2 + 3*5^3 + 3*5^6 + 5^7 + 3*5^9 + 3*5^10 + 3*5^12 + 4*5^13 + 3*5^15 + 2*5^16 + 3*5^18 + 4*5^19 + O(5^20)

        """
        prec = prec + 4

        K = Qp(self._p, prec=prec)
        rank = self._E.rank()
        if rank == 0:
            return K(1)

        if not self.is_split():
            raise NotImplementedError("The p-adic regulator is not implemented for non-split multiplicative reduction.")


        basis = self._E.gens()
        M = matrix.matrix(K, rank, rank, 0)

        height =   self.padic_height(prec= prec)
        point_height = [height(P) for P in basis]
        for i in range(rank):
            for j in range(i+1, rank):
                M[i, j] = M[j, i] = (- point_height[i] - point_height[j] + height(basis[i] + basis[j]))/2
        for i in range(rank):
            M[i,i] = point_height[i]

        return M.determinant()

