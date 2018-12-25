import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import logging
from bs4 import BeautifulSoup as soup
logger = logging.getLogger(__name__)
SITE = 'http://www.xnxx.com/search/Chinese'
from selenium.webdriver import ActionChains
import re
import json

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class XNXXCrawlerVideoList(object):
    """
    爬虫类，用来构建爬虫
    """

    def __init__(self, driver, data_url):
        self._driver = driver
        if data_url == '' or data_url is None:
            raise SyntaxError("数据采集地址不能为空")
        self._data_url = data_url

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver


    def start_data_mining(self):
        """
        开始数据采集
        :return:
        """
        self._get_page()

    def _get_page(self):
        """
        根据不同的URL请求网页数据
        :param url: 爬取网页网址
        :return: 网页的HTML
        """
        logging.info("正在爬取页面")
        self.driver.get(self._data_url)
        html = self.driver.page_source
        bsObj = soup(html, "html5lib")
        self.parse_page(bsObj)

    def parse_page(self, bsObj):
        """
        解析列表页面
        :param bsObj:
        :return:
        """
        thumb_block_list = bsObj.find_all("div", class_="thumb-block", )
        pagination = bsObj.find_all('div', class_='pagination')[0]
        pages_num = pagination.find_all('a', class_=False)
        # 获取所有的页码
        pages = list(map(lambda i: '%s%s' % (SITE, i), list(map(lambda i: i['href'], pages_num))))
        # TODO: 需要编写递归页面调用
        print(pages)
        result = []
        for video_wrap in thumb_block_list:
            videoId = video_wrap['id'].split('_')[1]
            thumb = video_wrap.find("div", class_="thumb", recursive=True)
            (imageUrl, videoUrl) = self.parse_thumb(thumb)
            videoUrl = self.processUrl(videoUrl)
            thumb_under = video_wrap.find("div", class_="thumb-under")
            (title, duration, hits, definition) = self.parse_thumb_under(thumb_under)
            result.append({'videoId': videoId,
                           'imageUrl': imageUrl,
                           'videoUrl': videoUrl,
                           'title': title,
                           'duration': duration,
                           'hits': hits,
                           'definition': definition})
        return result

    def parse_thumb(self, thumb):
        """
        解析缩略图，获取视频封面信息
        :param thumb:
        :return:
        """
        image = thumb.find("img")
        imageUrl = ""
        try:
            imageUrl = image['data-src']
        except Exception as e:
            print(e.__str__())
            imageUrl = image["src"]
        finally:
            print(imageUrl)
        a = thumb.find("a")
        videoUrl = a["href"]
        return imageUrl, videoUrl

    # 解析视频信息
    def parse_thumb_under(self, thumb_under):
        """
        解析视频缩略图的基础视频信息
        :param thumb_under:
        :return:
        """
        definition = ""
        hits = ""
        duration = ""
        title = ""
        title = thumb_under.find('p').find('a').string
        meta_data_tag = thumb_under.find('p', class_='metadata')
        meta_data = meta_data_tag.get_text().split('-')

        if len(meta_data) >= 3:
            duration = meta_data[0].strip()
            hits = meta_data[1].strip()
            definition = meta_data[2].strip()
        elif len(meta_data) == 2:
            duration = meta_data[0].strip()
            hits = meta_data[1].strip()
        elif len(meta_data) == 1:
            duration = meta_data[0].strip()
        else:
            logging.warning('不存在视频元数据')
        return title, duration, hits, definition

    def close(self):
        if self._driver:
            self._driver.close()


    def processUrl(self,url):
        """
        处理url问题
        :param url: 视频地址url
        :return:
        """
        pattern = re.compile(r'http[s]*[:]?[//]*www.xnxx.com')
        url = pattern.sub('', url)
        return url