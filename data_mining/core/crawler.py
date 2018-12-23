
class Crawler(object):
    """
    爬虫类，用来构建爬虫
    """
    __slots__ = ("_name", "_config") # 只对当前类有效，目的是限制该类的属性

    def __init__(self, name, config):
        """
        爬虫对象初始化
        """
        self.name(name)
        self.config(config)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        self._name = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

