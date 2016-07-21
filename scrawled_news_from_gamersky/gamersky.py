from selenium import webdriver
import pymongo
import time

client = pymongo.MongoClient('localhost',27017)
gamersky = client['gamersky']
news = gamersky['news']
#开场白

def page_parse(browser):
    titles = browser.find_elements_by_css_selector('div.con > div.tit > a')
    imgs = browser.find_elements_by_css_selector('div.img > a > img.pe_u_thumb')
    descs = browser.find_elements_by_css_selector('div.con > div.txt')
    times = browser.find_elements_by_css_selector('div.con > div.tme > div.time')
    comments = browser.find_elements_by_css_selector('div.con > div.tme > div.pls.cy_comment')

    for title,img,desc,time,comment in zip(titles,imgs,descs,times,comments):
        biaoti = title.text
        miaoshu = desc.text
        tupian = img.get_attribute('src')
        shijian = time.text
        pinglun = comment.text
        dizhi = title.get_attribute('href')
        data={
            'title':biaoti,
            'desc':miaoshu,
            'img':tupian,
            'time':shijian,
            'comment':pinglun,
            'link':dizhi
        }
        print(data)
        news.insert_one(data)
browser = webdriver.Firefox()
browser.get('http://www.gamersky.com/news/pc/zx/')

page_parse(browser)
i = 0
while(i<5):
    next_page = browser.find_element_by_css_selector('a.p1.nexe')
    next_page.click()
    time.sleep(5)
    if not browser.find_element_by_css_selector('div.con > div.tit > a'):
        browser.refresh()
        if not browser.find_element_by_css_selector('div.con > div.tit > a'):
            pass
    page_parse(browser)
    i+=1
browser.close()
