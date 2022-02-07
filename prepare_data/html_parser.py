# -*- coding: utf-8 -*- 
#@Time: 2022/1/29 15:58
#@Author: Li Yuanyuan
#@File: html_parser.py
#@Software: PyCharm


import re
import urllib.parse
from bs4 import BeautifulSoup


class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # ('div', class_='main-content J-content')
        divs = soup.findAll('div', attrs={'class': 'main-content J-content'})
        for div in divs:
            # 搜索所有满足条件的url
            links = div.findAll('a', href=re.compile(r"/item/"))
            for link in links:
                new_url = link['href']
                # 以page_url为标准来格式化new_url
                new_full_url = urllib.parse.urljoin(page_url, new_url)
                # Py3中用到的模块名称变为urllib.parse
                new_urls.add(new_full_url)

        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        basic = {}
        paras = {}


        # url
        res_data['url'] = page_url


        # 去除注释
        regex = re.compile('\[.{0,7}\]')

        # 去除图片中的文字
        tags = soup.findAll('div', class_='lemma-picture text-pic layout-right')
        for tag in tags:
            tag.clear()

        # 获取标题和简介内容
        # <dd class="lemmaWgt-lemmaTitle-title"> <h1>...</h1>
        # 搜取满足条件的标题
        title_node = soup.find('dd', class_='lemmaWgt-lemmaTitle-title').find('h1')
        # print(title_node.get_text())
        res_data['title'] = title_node.get_text().strip()

        # <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_='lemma-summary')
        if summary_node is None:
            return
        res_data['summary'] = regex.sub('',summary_node.get_text().strip()).replace('\n','').strip()
        # print(summary_node.get_text())

        summary_node.clear()

        # 获取基本信息
        basic_name = soup.findAll('dt', class_='basicInfo-item name')
        basic_value = soup.findAll('dd', class_='basicInfo-item value')
        for i in range(len(basic_name)):
            name = str(basic_name[i].get_text()).replace('\xa0', '').strip()
            value = str(basic_value[i].get_text()).replace('\xa0', '').strip()
            # 去掉[1][12-13]这样的注释
            value = regex.sub('', value).strip()
            basic[name] = value
        res_data['basicinfo'] = basic


        # 获取段落
        # <div class ="para" label-module="para" data-pid="3" >
        catalog_nodes = soup.find_all('div', class_='para')
        if catalog_nodes is None:
            return

        catalog_name = catalog_nodes[0].find_previous('h2').get_text().replace(title_node.get_text().strip(),'')
        catalog_content = ''

        for i in range(len(catalog_nodes)):
            text = regex.sub('',catalog_nodes[i].get_text().strip()).replace('\n','').strip()
            h2 = catalog_nodes[i].find_previous('h2').get_text().replace(title_node.get_text().strip(),'')
            if h2 == catalog_name:
                catalog_content += text
            else:
                paras[catalog_name] = catalog_content
                catalog_content = text
                catalog_name = h2
            if i == len(catalog_nodes) - 1:
                paras[catalog_name] = catalog_content

        res_data['paras'] = paras

        print(res_data)

        return res_data


    def parse(self, page_url, html_cont):#对于下载的页面进行解析
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')#先用python自带库进行解析。

        #提取有用的信息
        new_urls = self._get_new_urls(page_url, soup)#提取新的url
        new_data = self._get_new_data(page_url, soup)#提取有价值的信息
        return new_urls, new_data