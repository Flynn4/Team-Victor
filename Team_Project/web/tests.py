from django.test import TestCase


# Create your tests here.
class WebPageTest(TestCase):
    # def test_game_info(self):
    #     response = self.client.get('/game/730')
    #     self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_game(self):
        response = self.client.get('/search/dota')
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        response = self.client.get('/category/action')
        self.assertEqual(response.status_code, 200)
