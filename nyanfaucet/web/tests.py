from django.test import TestCase

from cryptocoin.validation import validate
from dice import CalculateWinnings

# Create your tests here.

class CheckAddressTest(TestCase):
    def test_btc_addr(self):
        addr = "1F8af39c5eheqL319okb7A8MZ5chfwEWTs"
        self.assertTrue(validate(addr, 0))
    
    def test_nyan_addr(self):
        addr = "KQm7yxJ4EWoohRHv3NaSH8VMxT3owf1oWk"
        self.assertTrue(validate(addr, 45))

    def test_doge_addr(self):
        addr = "DSempai2FjnuVc2tXsfsbNBVGJ5QUBtQtz"
        self.assertTrue(validate(addr, 30))

class WinningsTest(TestCase):
    jackpot = 1000000.0
    
    def test_jackpot(self):
        w = CalculateWinnings(10000, self.jackpot)
        self.assertEquals(w, 1000000.0)

    def test_least(self):
        w = CalculateWinnings(1337, self.jackpot)
        self.assertEquals(w, 10)

    def test_medium(self):
        w = CalculateWinnings(9995, self.jackpot)
        self.assertEquals(w, 1000)

    def test_almost(self):
        w = CalculateWinnings(9999, self.jackpot)
        self.assertEquals(w, 100000)
