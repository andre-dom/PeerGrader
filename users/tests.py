from django.test import TestCase
from .models import AppUser
from .forms import AppUserCreationForm

def setUp(self):
    # Setup run before every test method.
    pass


def tearDown(self):
    # Clean up run after every test method.
    pass


def test_something_that_will_pass(self):
    self.assertFalse(False)


def test_something_that_will_fail(self):
    self.assertTrue(False)
