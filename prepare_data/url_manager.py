# -*- coding: utf-8 -*- 
#@Time: 2022/1/29 15:57
#@Author: Li Yuanyuan
#@File: url_manager.py
#@Software: PyCharm

class UrlManager(object):

    # url管理器里面需要两个set来分别记录已经爬去的类和未爬取的类
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        self.new_urls.clear()
        self.old_urls.clear()

    # 判断待爬取url是否在容器中
    def add_new_url(self, url):#如果待添加的url为有效的url，且该url既不在已爬去的set里，也不在未爬去的set里，则添加
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # 添加新url到待爬取集合中
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    # 检查是否还有未爬取的url。
    def has_new_url(self):
        return len(self.new_urls) != 0

    # 获取待爬取url并将url从待爬取移动到已爬取
    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url