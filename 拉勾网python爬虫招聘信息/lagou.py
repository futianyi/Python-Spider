# -*- coding: utf-8 -*-

#爬取拉勾网关于python爬虫的相关招聘
#headers中没有添加Cooike,就不行,会被反爬虫机制识别,使用Session会话也没用
#先通过POST方法得到cookies,然后再请求,把cookies传进去也是失败,fk.....
#区别就是前者的cookies是程序得到的,而后者是浏览器抓包得到的
#这样看来应该是cookie来源的问题.待续....

import requests,re,json,pandas,math,time

#这个个是Session得到的令牌ID,的确,Session是简化的cookie,只是一个独一无二的ID,保存在服务端
#{'user_trace_token': '20180301141931-1a8065ad-161b-409a-a9cf-e6e33f0879f7'}
#这个是普通Cookie,包含很多信息
#{'user_trace_token': '20180301143139-eb4e797a-c06f-4267-bd2f-bba3de40d65c', 'JSESSIONID': 'ABAAABAABEEAAJACB11C394F38A851DD5F188E20AD73905'}
#不管是否使用requests.Session(),该爬虫都行得通
s = requests.Session()
#得到相关搜索最大页数
def get_page(url):
    r = s.post(url, data=params, headers=headers, timeout=10)
    data = json.loads(r.text)
    # 此处counts是int不是str
    counts = data['content']['positionResult']['totalCount']
    # 向上取整
    pages = math.ceil(counts / 15)
    page_number = pages if pages <= 30 else 30
    return page_number

#抓取想要的相关数据,page = page_number
def get_info(url, page):
    infos = []
    counts = 0
    for i in range(1, page+1):
        params = {
            'first': 'false',
            'pn': str(i),
            'kd': 'python"爬虫"'
        }
        r = s.post(url, data =params, headers=headers, timeout = 10)

        data = json.loads(r.text)
        info = data['content']['positionResult']['result']
        for workinfo in info:
            try:
                informatiaon = {
                    '公司': workinfo['companyFullName'],
                    '所在地': workinfo['city'],
                    '公司大小': workinfo['companySize'],
                    '职位名称': workinfo['positionName'],
                    #经过爬取发现某些标签过多时,是在companyLabelList里面
                    '标签': ','.join([i for i in workinfo['positionLables'] or workinfo['companyLabelList']]),
                    '发布时间': workinfo['formatCreateTime'],
                    '工作经验': workinfo['workYear'],
                    '学历': workinfo['education'],
                    '薪水': workinfo['salary']
                }
            except:
                informatiaon = {}
            infos.append(informatiaon)
            #time.sleep(1)
        # 爬取完一页记得停一下,减少网站压力,若太快,可能会被判定为"机器人"
        # 所谓与人方便,与己方便
        #>>>>>可用来表达进度
        counts = counts + 1
        print('>>>>>>>>>>>>>>>>>', counts)
        time.sleep(2)
    return infos
if __name__ == '__main__':
    # 该参数可修改,定位城市
    city = '全国'
    headers = {
        'Referer': 'https://www.lagou.com/jobs/list_python%22%E7%88%AC%E8%99%AB%22?px=default',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Cookie': 'user_trace_token=20180224151528-86357976-65b7-4b68-853a-77a305cd7ac5; _ga=GA1.2.1208832788.1519456528; LGUID=20180224151529-7e547311-1932-11e8-8eef-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.112591580.1519812421; JSESSIONID=ABAAABAACEBACDG0E85CB9D90A6CA73385B0D74B4CB7389; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519584108,1519812421,1519812629,1519817087; TG-TRACK-CODE=search_code; LGSID=20180301022111-279946df-1cb4-11e8-b106-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%2522%25E7%2588%25AC%25E8%2599%25AB%2522%3Fpx%3Ddefault%26city%3D%25E5%2585%25A8%25E5%259B%25BD; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%2522%25E7%2588%25AC%25E8%2599%25AB%2522%3Fpx%3Ddefault%26city%3D%25E5%25B9%25BF%25E5%25B7%259E; SEARCH_ID=0ac557ad35674285a3a697110a0d424b; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519842921; LGRID=20180301023523-230af366-1cb6-11e8-b106-5254005c3644'
    }
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
    #把数据导入Excel表格,文件名为jobs.xlsx
    allInfo.to_excel('jobs.xlsx')
    print(allInfo)