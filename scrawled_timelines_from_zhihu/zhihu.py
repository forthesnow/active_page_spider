from selenium import webdriver
import pymongo
import time

# 数据库
client = pymongo.MongoClient('localhost',27017)
zhihu = client['zhihu']
content = zhihu['content']
# 使用火狐浏览器
browser = webdriver.Firefox()
browser.get('https://www.zhihu.com/')

time.sleep(1)  #等它加载
browser.maximize_window()   #窗口最大化
browser.find_element_by_xpath('//a[2]').click()   #点击登录区域
browser.find_element_by_xpath('//input[@name="account"]').send_keys('552***11@qq.com')  #输入账号
browser.find_element_by_xpath('//input[@name="password"]').send_keys('*******')  #输入密码
# time.sleep(10)
browser.find_element_by_xpath('//button[@type="submit"]').click()  #点击登录按钮
i = 0
while(i<10):   # 每次滚动条拉到底部会加载约10条内容
    time.sleep(2)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')  #使用javascript实现窗口滚动
    i+=1
time.sleep(2)
def page_parse(browser):
    for i in range(110):
        #  要获取的几个元素的CSS位置
        title_css = '#feed-{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > h2:nth-child(3) > a:nth-child(1)'.format(i)
        img_css = '#feed-{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(4) > div:nth-child(5) > div:nth-child(2) > img:nth-child(1)'.format(i)
        desc_css = '#feed-{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(6) > div:nth-child(2)'.format(i)
        topic_css = '#feed-{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)'.format(i)
        author_css = '#feed-{} > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(4) > a:nth-child(1)'.format(i)
        title = ""
        # 因为是遍历的方式，所以有的时候会出现元素序号不连续的情况
        try:
            title = browser.find_element_by_css_selector(title_css).text
        except:
            pass
        if title == "":
            pass
        else:
            # 如果有题目，那就是有块，如果连题目都没有，证明就是一个空的div
            link ='http://www.zhihu.com/'+ browser.find_element_by_css_selector(title_css).get_attribute('href')
            img = ""
            try:
                img = browser.find_element_by_css_selector(img_css).get_attribute('src')
            except:
                pass
            desc = ""
            try:
                desc = browser.find_element_by_css_selector(desc_css).text.replace('显示全部','')
            except:
                pass
            topic = ''
            try:
                topic = browser.find_element_by_css_selector(topic_css).text
            except:
                pass
            author = ''
            try:
                author = browser.find_element_by_css_selector(author_css).text
            except:
                pass
            # feed-97 > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(5) > div:nth-child(4) > a:nth-child(1)
            data = {
                'title':title,
                'img':img,
                'desc':desc,
                'link':link,
                'topic':topic,
                'author':author
            }
            content.insert_one(data)

page_parse(browser)
