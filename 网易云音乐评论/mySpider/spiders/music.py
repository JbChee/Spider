from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from lxml import etree
#负责循环等待
from selenium.webdriver.support.ui import WebDriverWait
#负责条件
from selenium.webdriver.support import expected_conditions as EC
import csv
from selenium.webdriver import DesiredCapabilities


basic_path = 'E:/python_code/Search/datas/网易云音乐/'
class CloudMusic():
    def __init__(self):
        self.url = 'https://music.163.com/#/discover/toplist?id=19723756'

        self.csv = open(basic_path+'飙升榜.csv','a',newline='',encoding='utf-8')
        self.headname = ['用户名','保存文档时间','评论时间','点赞数','评论']
        self.writer = csv.DictWriter(self.csv, self.headname)    #生成写对象
        self.writerheader = self.writer.writeheader() #写入表头

    #获取飙升榜歌单链接
    def parse_page(self,d):
        # 打开网页
        d.get(self.url)
        time.sleep(2)

        #快照
        d.save_screenshot('open.png')
        # 最大化浏览器
        d.maximize_window()

        # 进入frame
        frame = d.find_elements_by_tag_name('iframe')[0]
        d.switch_to.frame(frame)

        #显示等待
        WebDriverWait(d,3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,'f-ff2'))
        )
        time.sleep(2)

        #获取歌曲 top100
        paths = d.find_elements_by_xpath('//tbody/tr')
        list1 = []
        i = 1
        for path in paths:
            item = {}
            if i>3:
                music_url = path.find_element_by_xpath('./td[2]/div/div/div/span/a').get_attribute('href')
            else:
                music_url = path.find_element_by_xpath('./td[2]/div/div/a').get_attribute('href')
            title = path.find_element_by_xpath('./td[2]/div/div/div/span/a/b').get_attribute('title')
            user = path.find_element_by_xpath('./td[4]/div').get_attribute('title')

            item['music_url'] = music_url   #音乐链接
            item['title'] = title           #歌名
            item['user'] = user             #歌手
            print(user)
            print(music_url)
            print(title)
            list1.append(item)
            i +=1
            break
        # d.close()
        print(f'歌曲数量{len(list1)}')
        return list1

    #获取每一首歌曲评论
    def parse_music(self, d, url):
        # 打开网页
        d.get(url)
        time.sleep(3)
        # 最大化浏览器
        d.maximize_window()

        #记录当前页数
        pagenum = 1
        while True:
            # 进入frame
            frame = d.find_elements_by_tag_name('iframe')[0]
            d.switch_to.frame(frame)
            print('已进入iframe')
            #显示等待
            WebDriverWait(d,10).until(
                EC.presence_of_all_elements_located((By.LINK_TEXT,'下一页'))
            )
            # js1 = 'document.body.scrollTop=5000'
            # d.execute_script(js1)
            time.sleep(5)

            #xpath 获取当前歌曲的所有评论
            paths = d.find_elements_by_xpath('//div[@class="cmmts j-flag"]/div[@class="itm"]')
            d.save_screenshot('comment.png')
            print(len(paths))
            # print('=====================')
            if len(paths) >0:
                for path in paths:
                    item = {}
                    username = path.find_element_by_xpath('./div[2]/div[1]/div/a').text     #用户名
                    comment = path.find_element_by_xpath('./div[2]/div[1]/div').text        #评论

                    re_comment = path.find_element_by_xpath('./div[2]/div[2]').text[:-1]        #评论回复

                    stars = path.find_element_by_xpath('./div[2]/div[2]/a[1]').text[1:-1]           #点赞数
                    star = 0 if not stars else stars
                    # comment_time = path.find_element_by_xpath('./div[2]/div[2]/div').text           #时间

                    re_comment_time = path.find_element_by_xpath('./div[2]/div[3]/div').text           #回复时间



                    print(username)
                    item['用户名'] = username
                    item['保存文档时间'] = time.asctime(time.localtime(time.time()))
                    item['评论时间'] = comment_time
                    item['点赞数'] = star
                    item['评论'] = comment
                    print(comment_time)
                    self.save_comment(item)

            #xpath 获取当前页面的下一页元素
            nextpagebtn = d.find_element_by_xpath("//div[contains(@class,'u-page')]/a[text()='下一页']")
            print(nextpagebtn)
            if "js-disable" in nextpagebtn.get_attribute("class"):
                print("已经是最后一页")
                print(f'一共{pagenum}页')
                break
            else:
                nextpagebtn.click()
                pagenum += 1
                print(f'当前为：第{pagenum}页评论')
                time.sleep(2)

        #退出浏览器
        d.quit()

    #保存数据
    def save_comment(self,item):
        self.writer.writerow(item)

    #运行
    def go(self):
        # //PHANTOMJS自定义userAgent，避免被反爬
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        )
        #设置PhantomJS 缓存和禁用图片加载 提高爬取效率
        SERVICE_ARGS = ['--load-images=false','--disk-cache=true']

        d = webdriver.PhantomJS(desired_capabilities=dcap, service_args=SERVICE_ARGS)
        # 设置一个很长的网页加载数据，省的有些情况还得滚动页面
        d.set_window_size(1920, 8000)

        items = self.parse_page(d)  #返回列表数据
        print(items)
        for item in items:        #遍历获取每一首歌曲评论
            # 查看歌曲链接
            url = item['music_url']
            print(url)

            #获取评论  用户名 点赞数
            self.parse_music(d, url)
            break

if __name__ == '__main__':
    c = CloudMusic()
    c.go()