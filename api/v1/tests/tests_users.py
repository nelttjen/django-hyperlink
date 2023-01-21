from django.test import TestCase
from django.urls import resolve, reverse
from rest_framework.test import RequestsClient, APITestCase

from .test_items_base import TestItemsBase
from users.api import *

client = RequestsClient()


class TestUsersCorrectView(TestCase):
    def test_users_activate_correct_view(self):
        resolved = resolve('api-users-activate')
        # self.assertEqual(reverse(resolved))