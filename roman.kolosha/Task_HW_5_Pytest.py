from unittest import TestCase
from task_4.task import BaseAPI

class TestBaseAPI(TestCase):

    @classmethod
    def setUpClass(self):
        self.item = 'qwerty', 123456
        self.baseapi = BaseAPI()
        self.baseapi.login('http://localhost:5002', 'test', 'test')

    @classmethod
    def tearDownClass(self):
        self.baseapi.close_connection()

    def test_login(self):
        self.baseapi.login('http://localhost:5002', 'test', 'test')
        self.assertTrue(True)

    def test_keys(self):
        tokens = self.baseapi.get_tokens()
        self.assertEqual(2, len(tokens))

    def test_create_item(self):
        item_id = self.baseapi.create_item(self.item)
        self.assertTrue(isinstance(item_id, int))

    def test_read_item(self):
        item_id = self.baseapi.create_item(self.item)
        new_item = self.baseapi.read_item(item_id)
        new_item = type(self.item)(new_item)
        self.assertEqual(self.item, new_item)

    def test_delete_item(self):
        item_id = self.baseapi.create_item(self.item)
        status = self.baseapi.delete_item(item_id)
        self.assertTrue(status)