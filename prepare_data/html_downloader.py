# -*- coding: utf-8 -*- 
#@Time: 2022/1/29 15:58
#@Author: Li Yuanyuan
#@File: html_downloader.py
#@Software: PyCharm

import string
from urllib import request
from urllib.parse import quote


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None

        url_ = quote(url, safe=string.printable)#这个主要应对中文编码的问题。
        response = request.urlopen(url_)

        if response.getcode() != 200:#判断是否正常访问该网页
            return None

        return response.read()