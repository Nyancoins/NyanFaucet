from django.test import TestCase

from web.forms import check_bc

# Create your tests here.

class CheckAddressTest(TestCase):
    def test_btc_addr(self):
        addr = "1F8af39c5eheqL319okb7A8MZ5chfwEWTs"
        self.assertFalse(check_bc(addr))
    
    def test_nyan_addr(self):
        addr = "KQm7yxJ4EWoohRHv3NaSH8VMxT3owf1oWk"
        self.assertTrue(check_bc(addr))

    def test_doge_addr(self):
        addr = "DSempai2FjnuVc2tXsfsbNBVGJ5QUBtQtz"
        self.assertFalse(check_bc(addr))