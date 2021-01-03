import unittest
from unittest import TestCase

from money import Money

from dubloon import Transaction


class TestTransaction(TestCase):
    def test_equals(self):
        a = Transaction()
        b = Transaction()
        self.assertTrue(a == b)
        a.amount = Money(2, 'EUR')
        b.amount = Money(2, 'USD')
        self.assertFalse(a == b)
        a.amount = Money(2, 'USD')
        a.description = 'steam'
        b.description = 'steam'
        a.transaction_date = '2020-01-01'
        b.transaction_date = '2020-01-02'
        self.assertFalse(a == b)
        b.transaction_date = '2020-01-01'
        self.assertTrue(a == b)


if __name__ == '__main__':
    unittest.main()
