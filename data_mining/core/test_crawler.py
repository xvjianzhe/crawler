from unittest import TestCase
from data_mining.core.crawler import Crawler


class TestCrawler(TestCase):

    def test_parse_thumb_under(self):
        pass

    def test_get_video_url(self):
        RESULT = r"https://vid-egc.xnxx-cdn.com/videos/mp4/a/2/0/xvideos.com_a2036ac7c261793ba2c8e39fdf01ee97-1.mp4?U9z1WGpSAosgKAmlKbV--84cVurJLeAIFgOiQgw1dp2ZoVF1BQawV2-n5KFPWn1Qf6JeO49nsPZjVKZ1bF08CLLfkM7IL2SxCEUY4C42Paefn9wGdMN92p0VymvRpG6IzQFshG6rpQf0ldRjRxbsnHfJc8SHvljQ_jfBT6LBHgqK-QXLBDg16R0MPcZ4TDXvDcEkFXXQD-U_Fg"
        file = open("../test/videourl.html", mode="r", encoding="utf8")
        temp_file = file.read()
        file.close()
        crawler = Crawler()
        url = crawler.get_video_url(temp_file)
        self.assertEqual(url, RESULT)

        url = crawler.get_video_url("")
        self.assertEqual(url, "")

    def test_processUrl(self):
        crawler = Crawler()

        url = crawler.processUrl("https//www.xnxx.com/video-pb5f995/11/_")
        self.assertEqual(url , "/video-pb5f995/11/_")

        url = crawler.processUrl("/video-pb5f995/11/_")
        self.assertEqual(url, "/video-pb5f995/11/_")

