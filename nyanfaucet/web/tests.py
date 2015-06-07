from django.test import TestCase

from web.btc import validate

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