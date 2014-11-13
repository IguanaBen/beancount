__author__ = "Martin Blais <blais@furius.ca>"

import unittest
import io
from decimal import Decimal

from .display_context import DisplayContext


class TestDisplayPrecision(unittest.TestCase):

    number = Decimal('-1764.9876543')

    def test_precision_empty_default(self):
        dc = DisplayContext()
        self.assertEqual('-1764.9876543', dc.format(self.number))
        self.assertEqual('-1764.9876543', dc(self.number))

    def test_precision_empty_default_integers(self):
        dc = DisplayContext()
        self.assertEqual('4343', dc(Decimal('4343')))
        self.assertEqual('-4343', dc(Decimal('-4343')))

    def test_precision_commas(self):
        dc = DisplayContext()
        dc.set_commas(True)
        self.assertEqual('-1,764.9876543', dc.format(self.number))
        dc.set_commas(False)
        self.assertEqual('-1764.9876543', dc.format(self.number))

    def test_precision_default(self):
        dc = DisplayContext()
        dc.set_precision(4)
        self.assertEqual('-1764.9877', dc.format(self.number))
        dc.set_precision(3)
        self.assertEqual('-1764.988', dc.format(self.number))

    def test_precision_currency(self):
        dc = DisplayContext()
        dc.set_precision(5, 'RBF1010')
        self.assertEqual('-1764.9876543', dc.format(self.number))
        self.assertEqual('-1764.98765', dc.format(self.number, 'RBF1010'))
        dc.set_precision(1)
        dc.set_precision(3, 'RBF1010')
        self.assertEqual('-1765.0', dc.format(self.number))
        self.assertEqual('-1764.988', dc.format(self.number, 'RBF1010'))

    def test_precision_integer(self):
        dc = DisplayContext()
        dc.set_precision(0)
        self.assertEqual('-1765', dc.format(self.number))

    def test_precision_max(self):
        dc = DisplayContext()
        dc.set_precision(2)
        dc.set_precision_max(4)
        self.assertEqual('-1764.99', dc.format(self.number))
        self.assertEqual('-1764.9877', dc.format_max(self.number))

    def test_precision_dump(self):
        dc = DisplayContext()
        dc.set_precision(2)
        dc.set_precision(2, 'CAD')
        dc.set_precision_max(8, 'CAD')
        dc.set_precision(4, 'RBF1010')
        oss = io.StringIO()
        dc.dump(oss)
        self.assertTrue(oss.getvalue())