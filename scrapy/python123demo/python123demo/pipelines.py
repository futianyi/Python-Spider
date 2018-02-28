# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests,re
import os.path


class Python123DemoPipeline(object):

    def process_item(self, item, spider):
        headers = {
            'Referer': 'http://www.mzitu.com/xinggan/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        root = 'E:/mz/'
        # 去掉名字中的非法字符
        item['name'] = re.sub('[\/:*?"<>|]', '', item['name'])

        #经过验证按下面的方案可以
        #该方案是先得到10个大目录,再打开文件时候再把url后缀写入路径
        path = root + item['name']
        if not os.path.exists(path):
            os.mkdir(path)

        #这个方案是直接一步到位就是先把所有文件先建好,错误
        #所以应该是我不知道的关于创建文件目录的实现过程,这样创建应该是行不通的(猜测)
        #经过验证原因如下
        # 子目录item['name'],item['imgurl'].split('/')[-1]不能一步创建
        res = requests.get(item['imgurl'], headers=headers)
        #path = root + item['name']+'/'+item['imgurl'].split('/')[-1]
        #if not os.path.exists(path):
                #os.mkdir(path)

        try:
            with open(path+'/'+item['imgurl'].split('/')[-1], 'wb') as f:
                f.write(res.content)
        except:
            print('failed')

        return item








