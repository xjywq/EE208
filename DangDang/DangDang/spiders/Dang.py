import scrapy
from ..settings import PROXIES
import random
class DangSpider(scrapy.Spider):
    name = 'Dang'  # 爬虫名
    allowed_domains = ['dangdang.com']  # 允许域
    start_urls = ['http://category.dangdang.com/cid4002378.html']  # 开始链接

    def parse(self, response):
        # 处理start_url
        item_list = response.xpath('//li[@dd_name="品牌"]//span')
        for _item in item_list:
            item = {}
            item["dealwith"] = "Category"
            item["Id"] = _item.xpath("./@rel").extract_first()
            item["name"] = _item.xpath(".//a/@title").extract_first() # 品牌的名字
            item["url"] = "http://category.dangdang.com" + \
                _item.xpath(".//a/@href").extract_first()
            # Todo 可以在此处把item的图标也存进去 暂时不做
            yield item
            yield scrapy.Request(
                item["url"],
                callback=self.Categoryparse,
                meta={'proxy': "http://" + random.choice(PROXIES)['ip_port']}
            )

    def Categoryparse(self, response):
        # 处理分类页面
        # print("Call for category spider")
        li_list = response.xpath('//div[@dd_name="普通商品区域"]//li[@ddt-pit]')
        From = response.xpath(
            '//*[@id="breadcrumb"]/div/div[2]/span[2]/@title').extract_first() # 这件商品的来源品牌
        for li in li_list:
            item = {}
            item["dealwith"] = "Item" # 
            item["title"] = li.xpath('./a/@title').extract_first()
            item["url"] = li.xpath('./a/@href').extract_first()
            item["price"] = li.xpath(
                './p[@class="price"]/span/text()').extract_first()
            item["hot_word"] = li.xpath(
                './p[@class="search_hot_word"]/text()').extract_first()
            item["from"] = From
            yield item
            yield scrapy.Request(
                item["url"],
                callback=self.Itemparse,
                meta={'proxy': "http://" + random.choice(PROXIES)['ip_port']}
            )
        next_url = response.xpath('//li[@class="next"]')
        if next_url:
            yield scrapy.Request(
                "http://category.dangdang.com/" +
                next_url.xpath('./a/@href').extract_first(),
                callback=self.Categoryparse,
                meta={'proxy': "http://" + random.choice(PROXIES)['ip_port']}
            )

    def Itemparse(self, response):
        # print("Call for item spider")
        # 处理商品细节页面
        item = {}
        item["dealwith"] = "Detail"
        # Todo 此处处理Item的相关页面, 需要爬取[商品图片, 商品分类, 商品评分, 商品评论, 评论标签]
        # page_url serves as 
        item['page_url'] = response.url
        # item['img_urls'] stores all five figures of this item
        item['img_urls'] = response.xpath('//*[@id="main-img-slider"]/li/a/img/@src').extract()
        categories = response.xpath('/html/body/div[3]/div[2]//text()').extract()
        all_category = ""
        for category in categories:
            if '\n' in category or '...' in category:
                continue
            all_category += category
        # item['category'] stores the category with format like xxx > xxx > xxx > xxxxxxx
        item['category'] = all_category
        score_temp = response.xpath('//*[@id="product_info"]/div[2]/div/span/span/@style').extract_first()
        if score_temp:
            item['score'] = score_temp[6:-1]
        else:
            item['score'] = "NULL"
        # TODO the comment of this item is placed by Ajax, namely the js script, which is hard to extract
        # TODO A big problem
        item['comments'] = "NULL"
        item['comment_tag'] = "NULL"
        return item
