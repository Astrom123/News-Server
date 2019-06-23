import json
import datetime


class News:

    def __init__(self):
        with open("news.json", "r") as f:
            self.news = json.load(f)
        with open("comments.json", "r") as f:
            self.comments = json.load(f)
        self.news["news"].sort(key=lambda new: new['date'])
        self.count_comments()

    def get_valid_news(self):
        curr_date = str(datetime.datetime.now()).replace(" ", "T")
        valid_news = [new for new in self.news["news"] if new["date"] < curr_date and not new["deleted"]]
        return valid_news

    def count_comments(self):
        for new in self.news["news"]:
            new["comments_count"] = 0
        for comment in self.comments["comments"]:
            for new in self.news["news"]:
                if new["id"] == comment["news_id"]:
                    new["comments_count"] += 1

    def get_new(self, new_id):
        for new in self.news["news"]:
            if new["id"] == new_id:
                result = dict(new)
                result["comments"] = self.get_comments(new_id)
                return result

    def get_comments(self, new_id):
        comments = [com for com in self.comments["comments"] if new_id == com["news_id"]]
        comments.sort(key=lambda comm: comm['date'])
        return comments
