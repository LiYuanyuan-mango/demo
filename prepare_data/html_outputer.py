# -*- coding: utf-8 -*- 
#@Time: 2022/1/29 15:59
#@Author: Li Yuanyuan
#@File: html_outputer.py
#@Software: PyCharm
import csv
import traceback



class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open('output.html', 'w', encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<a>")

        for data in self.datas:
            # 屏蔽掉原来的，重新写一个更美观的输出效果
           fout.write("<tr>")
           fout.write("<td>%s</td>" % data['url'])
           fout.write("<td>%s</td>" % data['title'])
           fout.write("<td>%s</td>" % data['summary'])
           fout.write("</tr>")
            # fout.write('<p>%s</p>' % data['title'])
            # fout.write('<p>%s</p>' % data['summary'])

        fout.write("</a>")
        fout.write("</body>")
        fout.write("</html>")

        fout.close()

    def save_to_csv(self):
        try:
            headers = ['title','summary','basicinfo','paras']
            # with open('data.file', 'a+') as csvfile:
            with open('data.csv', 'a+') as csvfile:
                writer = csv.writer(csvfile)
                for data in self.datas:
                    writer.writerow(data)
        except IOError:
            traceback.print_exc()
            print("Write Error!")
