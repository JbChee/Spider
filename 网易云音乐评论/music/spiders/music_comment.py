import scrapy
from scrapy import Request
from ..items import *
import time
import json
from ..items import Music_comment

basic_path = 'E:/python_code/Search/datas/网易云音乐/'
class MusicSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['music.163.com']
    # start_urls = ['https://music.163.com/#/discover/toplist?id=19723756']


    def start_requests(self):
        url= 'https://music.163.com/#/discover/toplist?id=19723756'

        yield Request(url = url, callback=self.parse, meta={'type':'index_page','page':1})

    def parse(self, response):
        # 获取歌曲 top100
        paths = response.find_elements_by_xpath('//tbody/tr')
        i = 1
        for path in paths:
            item = Music_comment()
            if i > 3:
                music_url = path.find_element_by_xpath('./td[2]/div/div/div/span/a').get_attribute('href')
            else:
                music_url = path.find_element_by_xpath('./td[2]/div/div/a').get_attribute('href')
            title = path.find_element_by_xpath('./td[2]/div/div/div/span/a/b').get_attribute('title')
            user = path.find_element_by_xpath('./td[4]/div').get_attribute('title')

            item['music_url'] = music_url  # 音乐链接
            item['title'] = title  # 歌名
            item['user'] = user  # 歌手
            print(user)
            print(music_url)
            print(title)
            # list1.append(item)
            i += 1
            yield scrapy.Request(url = item['music_url'], meta={'item':item,'type':'comment'}, callback=self.parse_comment)
            break
        # d.close()
        # print(f'歌曲数量{len(list1)}')

    def parse_comment(self,response):
        #获取meta 数据
        before_item = response.meta.get('item')
        now_url = before_item['music_url']

        paths = response.xpath('//div[@class="cmmts j-flag"]/div[@class="itm"]')
        response.save_screenshot('comment.png')
        print('当前页评论数：',len(paths))
        print('=====================')
        while True:
            item = Music_comment()
            # 记录当前页数
            pagenum = 1
            if len(paths) > 0:
                for path in paths:
                    item = {}
                    username = path.xpath('./div[2]/div[1]/div/a').extract_first()  # 用户名
                    comment = path.path('./div[2]/div[1]/div').extract()[:-1]       # 评论
                    set_info = []
                    try:
                        re_comment = path.xpath('./div[2]/div[2]').extract()           # 评论回复
                        re_username = path.xpath('./div[2]/div[2]/a').extract_first()  # 回复用户名
                        re_info = (re_comment,re_username)
                        set_info = set_info.append(re_info)
                    except:
                        print('此评论没有人回复')

                    stars = path.xpath('./div[2]/div[2]/a[1]').extract()[1:-1]        # 点赞数
                    star = 0 if not stars else stars
                    comment_time = path.xpath("./div[2]//div[contains(@class,'u-time')]").extract()  #评论时间


                    print(username)
                    item['com_user'] = username
                    item['save_time'] = time.asctime(time.localtime(time.time()))
                    item['com_time'] = comment_time
                    item['star'] = star
                    item['comment'] = [comment,set_info]
                    item['music_url'] = before_item['music_url']
                    item['title'] = before_item['title']
                    item['song_user'] = before_item['user']
                    print(comment_time)
                    # self.save_comment(item)
                    yield item
                    yield Request(url=now_url,meta={'type':'comment','page':2}, callback=self.parse_comment)


            # xpath 获取当前页面的下一页元素class 属性值
            nextpagebtn = response.xpath("//div[contains(@class,'u-page')]/a[text()='下一页']/@class")
            print(nextpagebtn)
            if "js-disable" in nextpagebtn:
                print("已经是最后一页")
                print(f'一共{pagenum}页')
                break
            else:
                pagenum += 1
                print(f'当前为：第{pagenum}页评论')
                time.sleep(2)

            # 退出浏览器








