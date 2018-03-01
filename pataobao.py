# -*- coding: utf-8 -*-
#爬取淘宝,没想到大马云没设防...

import requests,re,pandas,time
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'referer': 'https://www.taobao.com/'
}

def get_html(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return r.status_code

def parse_page(html):
    list = []
    price_list = re.findall(r'\"view_price\"\:\"(.*?)\"', html)
    title_list = re.findall(r'\"raw_title\"\:\"(.*?)\"', html)
    location_list = re.findall(r'\"item_loc\"\:\"(.*?)\"', html)
    for i in range(len(price_list)):
        try:
            #这个里面都是字符串,eval把值转换成数字
            price = eval(price_list[i])
            title = title_list[i]
            location = location_list[i]
            dic = { '商品名': title, '单价': price, '发货地址': location}
            list.append(dic)
        except:
            list.append('')
    return list

if __name__ == '__main__':
    base_url = 'https://s.taobao.com/search?&q={}&s={}'
    #可修改,改了几个都可以,就是不知道为什么每次第一页只返回36组数据,讲道理应该是
    goods = 'macbookpro'
    #爬取前2页商品相关信息
    for i in range(2):
        url = base_url.format(goods, 44*i)
        html = get_html(url)
        info = parse_page(html)
        info = pandas.DataFrame(info)
        print(info)
        time.sleep()




