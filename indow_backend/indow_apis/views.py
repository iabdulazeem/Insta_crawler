from django.shortcuts import render

from scrapyd_api import ScrapydAPI
from uuid import uuid4
scrapyd = ScrapydAPI(settings.SCRAPYD_SERVER_URL)


class StartInstagramCrawlerView(APIView):

    def post(self, request):
        app_user_id = request.user.id
        unique_id = str(uuid4())
        public_username = request.data.get('username')
        crawler_triggered = self._trigger_crawler(
            public_username, unique_id, app_user_id)
        if crawler_triggered:
            return Response({"Success": "Instagram crawler triggered from scrapy", 'CrawlerID': unique_id})
        return Response({"Error": "Error in triggering crawler, scrapyd server is down"})

    def _trigger_crawler(self, public_username, unique_id, app_user_id):
        setting = {
            'unique_id': unique_id,
            'USER_AGENT': settings.SCRAPER_AGENT
        }
        try:
            task = scrapyd.schedule('default', 'insta_crawler', settings=setting,
                                    username=public_username, unique_id=unique_id)
            crawler_stats = CrawlerStats()
            crawler_stats.unique_id = unique_id
            crawler_stats.task_id = task
            crawler_stats.status = "Started"
            crawler_stats.save()
            return True
        except:
            return False