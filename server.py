from aiohttp import web
import news


class HttpNewsServer:

    def __init__(self):
        self.app = None
        self.news = news.News()

    def run(self):
        self.app = web.Application()
        self.setup_routes()
        web.run_app(self.app, host='127.0.0.1', port=80)

    def setup_routes(self):
        self.app.router.add_get('/', self.get_news)
        self.app.router.add_get("/news/{id}", self.get_new)

    async def get_news(self, request):
        news = self.news.get_valid_news()
        return web.json_response({"news": news, "news_count": len(news)})

    async def get_new(self, request):
        try:
            new = self.news.get_new(int(request.match_info["id"]))
        except ValueError:
            new = None

        if new and not new["deleted"]:
            return web.json_response(new)
        else:
            return web.Response(status=404)


def main():
    server = HttpNewsServer()
    server.run()


if __name__ == '__main__':
    main()
