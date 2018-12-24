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




class Crawler(object):
    """
    爬虫类，用来构建爬虫
    """
    # __slots__ = ("_name", "_config") # 只对当前类有效，目的是限制该类的属性

    # def __init__(self, name, config):
    #     """
    #     爬虫对象初始化
    #     """
    #     self.name(name)
    #     self.config(config)

    # @property
    # def name(self):
    #     return self._name
    #
    # @name.setter
    # def name(self,value):
    #     self._name = value
    #
    # @property
    # def config(self):
    #     return self._config
    #
    # @config.setter
    # def config(self, value):
    #     self._config = value

    def __init__(self):
        self._driver = None

    def start_data_mining(self):
        """
        开始数据采集
        :return:
        """

        # data_mining_engine = minning_engine.factory(self.config)

    def get_page(self):
        """
        根据不同的URL请求网页数据
        :param url: 爬取网页网址
        :return: 网页的HTML
        """
        logging.info("正在爬取页面")
        driver = webdriver.Chrome(chrome_options=self.chrome_options())
        driver.get(SITE)
        html = driver.page_source
        driver.close()
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
            print('视频ID：%s' % videoId)
            thumb = video_wrap.find("div", class_="thumb", recursive=True)
            (imageUrl, videoUrl) = self.parse_thumb(thumb)
            print("图片URL %s，视频相对路径：%s" % (imageUrl, videoUrl))
            videoUrl = self.processUrl(videoUrl)
            thumb_under = video_wrap.find("div", class_="thumb-under")
            (title, duration, hits, definition) = self.parse_thumb_under(thumb_under)
            print('标题：%s，视频长度：%s，视频点击次数 %s，视频清晰度：%s' % (title, duration, hits, definition))
            result.append({'videoId': videoId,
                           'imageUrl': imageUrl,
                           'videoUrl': videoUrl,
                           'title': title,
                           'duration': duration,
                           'hits': hits,
                           'definition': definition})

            self.parse_video_page("http://www.xnxx.com%s" % videoUrl)
        logging.info("页面数据解析完成")
        return result


    def processUrl(self,url):
        """
        处理url问题
        :param url: 视频地址url
        :return:
        """
        pattern = re.compile(r'http[s]*[:]?[//]*www.xnxx.com')
        url = pattern.sub('', url)
        return url

    def get_video_url(self, script_content):
        """
        获取视频URL
        :param script_content:
        :return:
        """
        pattern = re.compile(r"[.]*setVideoUrlHigh\(\'(.*)\'\)")
        str = "".join(pattern.findall(script_content))
        if str.strip() == '':
            raise SyntaxError("无法找到URL,原文为：'%s'" % script_content)
        return str

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

    def parse_video_page(self, video_page_url):
        """
        解析视频页面
        :param video_page_url: 视频页面URL
        :return: 解析成功的视频URL
        """
        print(video_page_url)
        driver = webdriver.Chrome(chrome_options=self.chrome_options())
        driver.get(video_page_url)
        # self.getHttpStatus(driver)
        try:
            # TODO 尝试获取查询信息，否则使用while true 的形式获取查询进度
            if WebDriverWait(driver, 30,500).until(EC.presence_of_element_located((By.ID, "video-player-bg"))):
                html = soup(driver.page_source, "html5lib")
                bgs =  html.select("#video-player-bg script")
                for s in bgs:
                    script_content = s.get_text()
                    start = script_content.find("setVideoUrlHigh", 0, len(script_content))
                    if start != -1 and script_content:
                        video_url = self.get_video_url(script_content)
                        print(video_url)
                        return video_url
        except Exception as e :
            print(e)
        finally:
            driver.close()
            self.close()

    def getHttpStatus(self, driver):
        """
        获取HTTP请求状态
        :param driver:
        :return:
        """
        for responseReceived in driver.get_log('browser'):
            try:
                response = json.loads(responseReceived[u'message'])[u'message'][u'params'][u'response']
                print(response)
                if response[u'url'] == driver.current_url:
                    print(response[u'status'])
                    print(response[u'statusText'])
                    return (response[u'status'], response[u'statusText'])
            except:
                pass
            return None

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

    def chrome_options(self):
        """
        配置Chrome 选项
        :return: chrome 选项
        """
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

