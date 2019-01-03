
import multiprocessing as mp
import time
import os

class CrawlerEngine(object):
    # 当前进程数量
    _currentProcessCount = 0
    # 最大线程数量
    _processMaxCount = 10 # 后面修改成CPU核数

    # 待爬取网页队列
    _siteQueue=[]
    # 待解析网页源码队列
    _pageSourceQueue=[]
    # 待下载数据队列
    _dataQueue = []

    def __init__(self, baseSiteConfig, analyzeConfig, fileStorageConfig, crawlerConfig):
        """
        初始化爬虫引擎,构建基础进程池
        :param baseSiteConfig: 基础网站配置
        :param analyzeConfig: 基础分析配置，指定需要抓取数据的元素标记或者模板
        :param fileStorageConfig: 基础数据存放位置，数据库或者文件路径，本地或者是云服务器
        :param crawlerConfig: 基础爬虫配置，包括最大进程数，进程限制等
        """
        self._baseSiteConfig = baseSiteConfig
        self._analyzeConfig = analyzeConfig
        self._fileStorageConfig = fileStorageConfig
        self._crawlerConfig = crawlerConfig
        self._prepareProcessPool()
        self._calculateMaxProcessCount()
        pass

    def startCrawler(self):
        """
        1. 分配进程
        TODO: 处理启动逻辑，分配进程，启动网页爬取进程，等待该进程返回数据，如果数据返回，则启动网页分析进程，获取元数据,并等待
        TODO: 元数据返回，如果还有下级网页需要爬取，则尝试获取进程标识，如果获取进程标识，则启动新的网页爬取进程，将元数据发送
        TODO: 进行爬取，
        1. 创建网页爬取队列
        2. 启动爬取进程，等待进程数据返回
        3. 如果数据返回，创建待分析队列，启动网页分析进程，分析元数据，返回
        4. 如果分析数据返回，如果还有下级网页需要爬取，将该元数据和类型加入网页爬取队列，队列按照优先级排序
        6. 如果分析数据返回，有需要下载的数据，则启动下载进程，创建下载队列，下载数据，当下载队列为空时，判断是否全部爬取完毕，如果结束
        则终止下载进程，否则等待下载队列再次填充
        :return:
        """
        p = mp.Pool()
        for i in range(10):
            print('添加任务')
            p.apply_async(self._getBrowser)
        p.close()
        p.join()
        # browsser = self._getBrowser()
        pass

    def _prepareProcessPool(self):
        """
        0. 计算每个进程池最大可以启动的进程限制
        1. 构建网页下载器的进程池
        2. 构建网页分析器的进程池
        3. 构建数据下载器的进程池
        :return:
        """
        self._calculateMaxProcessCount()
        self._buildBrowserProcessPool()
        self._buildPageAnalyzerPool()
        self._buildDataDownloadPool()

    def _calculateMaxProcessCount(self):
        """
        计算每个进程池最大可以启动的进程限制，如果配置中有指定最大进程数量，使用配置指定的，否则使用CPU核数
        :return:
        """
        # if self._crawlerConfig["maxProcessCount"] is None:
        #     self._processMaxCount = 10 # TODO：计算CPU核数
        # self._processMaxCount = self._crawlerConfig["maxProcessCount"]
        # return self._processMaxCount
        pass

    def _buildBrowserProcessPool(self):
        """
        TODO：构建网页下载器的进程池
        :return:
        """
        pass

    def _buildPageAnalyzerPool(self):
        """
        TODO：构建网页分析器的进程池
        :return:
        """
        pass

    def _buildDataDownloadPool(self):
        """
        TODO：构建数据下载器的进程池
        :return:
        """
        pass

    def _getBrowser(self):
        """
        判断网页下载器进程是否达到最大限制，如果达到最大限制返回None
        否则返回一个进程标识
        :return:
        """
        time.sleep(4)
        print('进程ID：------%s------' % os.getpid())


        # if self._currentProcessCount < self._processMaxCount:
        #     return self._getIdleProcess()
        return None

    def _getIdleProcess(self):
        """
        TODO：获取空闲进程标识
        :return:
        """
        pass


if __name__ == '__main__':
    c = CrawlerEngine('','','','')
    c.startCrawler()
