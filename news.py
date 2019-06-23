import json
import datetime
from collections import OrderedDict, defaultdict


class News:

    def __init__(self):
        self.news = self.prepare_news()
        self.comments = self.prepare_comments()
        self.count_comments()

    def get_valid_news(self):
        curr_date = str(datetime.datetime.now()).replace(" ", "T")
        valid_news = [new for new in self.news.values() if new["date"] < curr_date and not new["deleted"]]
        return valid_news

    def get_new(self, new_id):
        if new_id in self.news.keys():
            new = dict(self.news[new_id])
            new["comments"] = self.comments[new_id]
            return new
        return None

    def count_comments(self):
        for new in self.news.values():
            new["comments_count"] = len(self.comments[new["id"]])

    def prepare_news(self):
        result = OrderedDict()
        with open("news.json", "r") as f:
            news = json.load(f)
            news["news"].sort(key=lambda new: new['date'])
        for new in news["news"]:
            result[new["id"]] = new
        return result

    def prepare_comments(self):
        result = defaultdict(list)
        with open("comments.json", "r") as f:
            comments = json.load(f)
        for com in comments["comments"]:
            result[com["news_id"]].append(com)
        for comments in result.values():
            comments.sort(key=lambda comm: comm['date'])
        return result
