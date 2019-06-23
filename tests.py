import unittest
import http.client
from server import HttpNewsServer
import json
import datetime
from multiprocessing import Process


class TestServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = HttpNewsServer()
        cls.process = Process(target=cls.server.run)
        cls.process.start()
        cls.conn = http.client.HTTPConnection("localhost", 80)
        cls.conn.request("GET", "/")
        cls.news = json.loads(cls.conn.getresponse().read())

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        cls.process.kill()

    def test_get_all_news_date(self):
        date = str(datetime.datetime.now()).replace(" ", "T")
        for new in self.news["news"]:
            self.assertLess(new["date"], date)

    def test_get_all_news_date_sorted(self):
        date = self.news["news"][0]["date"]
        for new in self.news["news"][1:]:
            self.assertGreaterEqual(new["date"], date)

    def test_get_all_news_not_deleted(self):
        for new in self.news["news"]:
            self.assertFalse(new["deleted"])

    def test_comments_count(self):
        for new in self.news["news"]:
            self.assertTrue(new["comments_count"] >= 0)

    def test_get_new_1(self):
        self.conn.request("GET", "/news/1")
        data = json.loads(self.conn.getresponse().read())
        self.assertEqual(data["id"], 1)
        self.assertFalse(data["deleted"])
        self.assertTrue(data["comments_count"] >= 0)
        self.assertEqual(len(data["comments"]), data["comments_count"])

    def test_get_nonexistent_new(self):
        self.conn.request("GET", "/news/0")
        response = self.conn.getresponse()
        self.assertEqual(response.getcode(), 404)
        self.assertEqual(response.read().decode(), "")


if __name__ == '__main__':
    unittest.main()
