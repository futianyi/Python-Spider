# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
'''
chs_arabic_map = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                  '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                  '十': 10, '百': 100, '千': 10 ** 3, '万': 10 ** 4,
                  '〇': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4,
                  '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
                  '拾': 10, '佰': 100, '仟': 10 ** 3, '萬': 10 ** 4,
                  '亿': 10 ** 8, '億': 10 ** 8, '幺': 1,
                  '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                  '7': 7, '8': 8, '9': 9}

num_list = ['1', '2', '4', '5', '6', '7', '8', '9', '0', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '零', '千',
            '百', '万']


def get_tit_num(title):
	result = ''
	for char in title:
		if char in num_list:
			result += char
	return result


def Cn2An(chinese_digits):
	result = 0

	for count in range(0, len(chinese_digits), 2):
		curr_char1 = chinese_digits[count]
		curr_digit1 = chs_arabic_map[curr_char1]
		try:
			curr_char2 = chinese_digits[count + 1]
			curr_digit2 = chs_arabic_map[curr_char2]
		except:
			curr_digit2 = 1
		result = result + curr_digit1 * curr_digit2

	return result

# test
headers = {



	'Referer':'http://www.mzitu.com/xinggan/',


}
imgurl = 'http://i.meizitu.net/2018/02/20d01.jpg'
response = requests.get(imgurl, headers = headers)
path = 'E:/yibu/' + response.url.split('/')[-1]
with open(path, 'wb') as f:
	f.write(response.content)
print(Cn2An(get_tit_num('第一万一千三百九十一章 你妹妹被我咬了！')))
'''

##import requests
##from bs4 import BeautifulSoup
##from lxml import etree


#print(s)



#result = etree.tostring(html)







#li = r.xpath('//div[@class="postlist"]/ul/li[position()<5]')
