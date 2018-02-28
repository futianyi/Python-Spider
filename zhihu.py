# -*- coding: utf-8 -*-
#模拟浏览器登录知乎

import selenium,requests
import time
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By

#需要把下载的chromedriver拷贝到python.exe的"同级目录,否则需要把路径写明
browser = webdriver.Chrome()
#建立持久连接
s = requests.Session()
#去爬虫头部
s.headers.clear()
browser.get('https://www.zhihu.com')
#隐式等待3秒,也就是1秒加载完成就等待1秒
browser.implicitly_wait(3)
#知乎页面首先显示注册页面需要先点击登录按钮
browser.find_element_by_css_selector('.SignContainer-switch span').click()
#清空输入栏
browser.find_element_by_xpath('//input[@name="username"]').clear()
input_first = browser.find_element_by_xpath('//input[@name="username"]').send_keys('username')
browser.find_element_by_xpath('//input[@name="password"]').clear()
input_second = browser.find_element_by_xpath('//input[@name="password"]').send_keys('password')
#短时间内连续登录,会要求输入验证码,给5秒手动输入验证码
time.sleep(5)
#点击登录
browser.find_element_by_css_selector('.Login-options+button').click()
#等待页面刷新
browser.implicitly_wait(3)

#本打算登录之后直接得到Cookie,采用Xpath,bs4等熟悉方法提取想要的数据
#也不知道想取什么数据,留个坑
cookies = browser.get_cookies()
#点击个人头像
browser.find_element_by_xpath('//div[@class="Popover AppHeader-menu"]').click()
browser.implicitly_wait(3)
#点击个人主页
browser.find_element_by_xpath('//div[@class="Menu"]/a[1]').click()#点击个人主页
browser.implicitly_wait(3)
#点击更多
browser.find_element_by_xpath('//div[@class="Profile-main"]//div[@class="Popover Tabs-link"]').click()#2个
browser.implicitly_wait(3)
#点击关注
browser.find_element_by_xpath('//div[@class="Menu"]/a[2]').click()
browser.implicitly_wait(3)
#点击已关注者的ID,进入到他的主页
browser.find_element_by_xpath('//div[@class="ContentItem-head"]//a[@class="UserLink-link"]').click()
browser.implicitly_wait(5)
browser.quit()#关闭浏览器































