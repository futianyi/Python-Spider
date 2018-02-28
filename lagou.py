# -*- coding: utf-8 -*-

#爬取拉勾网关于python爬虫的相关招聘

import requests,re,json,pandas,math,time
from bs4 import BeautifulSoup

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python%22%E7%88%AC%E8%99%AB%22?px=default&city=%E5%B9%BF%E5%B7%9E',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest'
}
#得到相关搜索最大页数
def get_page(url):
    html = requests.post(url, headers=headers, data=params, timeout=10).text
    data = json.loads(html)
    # 此处counts是int不是str
    counts = data['content']['positionResult']['totalCount']
    # 向上取整
    pages = math.ceil(counts / 15)
    page_number = pages if pages <= 30 else 30
    return page_number

#抓取想要的相关数据,page = page_number
def get_info(url, page):
    infos = []
    for i in range(1, page + 1):
        params = {
            'first': 'false',
            'pn': str(i),
            'kd': 'python"爬虫"'
        }
        html = requests.post(url, data =params, headers=headers, timeout = 10).text
        data = json.loads(html)
        info = data['content']['positionResult']['result']
        for workinfo in info:
            try:
                companyName = workinfo['companyFullName']
                companySize = workinfo['companySize']
                formatCreateTime = workinfo['formatCreateTime']
                workYear = workinfo['workYear']
                education = workinfo['education']
                salary = workinfo['salary']
            except:
                #此处个人认为其他几个一定会有,这几个不一定
                companySize = ''
                workYear = ''
                education = ''
            finally:
                informatiaon = {
                    '公司': companyName,
                    '公司大小': companySize,
                    '发布时间': formatCreateTime,
                    '工作经验': workYear,
                    '学历': education,
                    '薪水': salary
                }
                infos.append(informatiaon)
        # 爬取完一页记得停一下,减少网站压力,若太快,会被判定为"机器人"
        # 所谓与人方便,与己方便
        #>>>>>可用来表达进度
        print('>>>>>>>>>>>>>>>>>')
        time.sleep(2)
    return infos

if __name__ == '__main__':
    #该参数可修改,定位城市
    city = '全国'
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false&isSchoolJob=0'.format(city)
    params = {
        'first': 'false',
        'pn': '1',
        'kd': 'python"爬虫"'
    }
    page = get_page(url)
    print(page)
    #转换成DataFrame格式
    all = get_info(url, page)
    allInfo = pandas.DataFrame(all)
    print(allInfo)