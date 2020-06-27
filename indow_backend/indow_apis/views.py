from django.shortcuts import render
from django.conf import settings
from scrapyd_api import ScrapydAPI
from uuid import uuid4
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CrawlerStats, InstagramUserMedia
from zipfile import ZipFile
from wsgiref.util import FileWrapper

scrapyd = ScrapydAPI(settings.SCRAPYD_SERVER_URL)


class StartInstagramCrawlerView(APIView):

    def post(self, request):
        unique_id = str(uuid4())
        public_username = request.data.get('username')
        crawler_triggered = self._trigger_crawler(
            public_username, unique_id)
        if crawler_triggered:
            return Response({"Success": "Instagram crawler triggered from scrapy", 'CrawlerID': unique_id})
        return Response({"Error": "Error in triggering crawler, scrapyd server is down"})

    def _trigger_crawler(self, public_username, unique_id):
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
        except Exception as e:
            raise e
            return False


class DownloadCrawledImages(APIView):

    def get(self, request, crawler_id):
        zip_file_path = self.zip_images(crawler_id)
        if zip_file_path:
            wrapper = FileWrapper(open(zip_file_path, 'rb'))
            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=crawledMedia.zip'
            return response
        return Response({'error': 'could not save zip'})

    def zip_images(self, crawler_id, folder_name=None):
        media = InstagramUserMedia.objects.filter(crawler_id=crawler_id)
        if not folder_name:
            folder_name = crawler_id
        zip_file_dir = f"{settings.MEDIA_ROOT}/{str(folder_name)}"

        if(_create_directory(zip_file_dir)):
            zip_file_path = f"{zip_file_dir}/crawledMedia.zip"

            with ZipFile(zip_file_path, 'w') as zip:
                count = 0
                for image in media:
                    count += 1
                    image_url = image.media_url
                    r = requests.get(image_url, allow_redirects=True)
                    zip.writestr(f"image{count}.jpeg", r.content)
                zip.close()
            return zip_file_path
        return False


def _create_directory(path):
    if os.path.exists(path):
        return True
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
        return False
    else:
        print("Successfully created the directory %s " % path)
        return True