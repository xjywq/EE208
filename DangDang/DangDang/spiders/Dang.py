import json
import logging
import random

import scrapy

logger = logging.getLogger(__name__)


class DangSpider(scrapy.Spider):
    name = 'Dang'  # 爬虫名
    allowed_domains = ['dangdang.com']  # 允许域
    start_urls = ['http://category.dangdang.com/cid4003819.html']  # 开始链接
    # start_urls = ['http://category.dangdang.com/cid4002378.html']

    def parse(self, response):
        # 处理start_url
        print("start DangDang project from: ", self.start_urls)
        item_list = response.xpath('//li[@dd_name="品牌"]//li')
        for _item in item_list:
            item = {}
            item["dealwith"] = "Category"
            item["Id"] = _item.xpath("./@rel").extract_first()
            item["name"] = _item.xpath(".//a/@title").extract_first()  # 品牌的名字
            item["url"] = "http://category.dangdang.com" + \
                _item.xpath(".//a/@href").extract_first()
            # Todo 可以在此处把item的图标也存进去 暂时不做
            yield item
            yield scrapy.Request(
                item["url"],
                callback=self.Categoryparse,
                meta = {'from': item['name'], 'id': item["Id"]}
            )

    def Categoryparse(self, response):
        # 处理分类页面
        # print("Call for category spider")
        li_list = response.xpath('//div[@dd_name="普通商品区域"]//li[@ddt-pit]')
        for li in li_list:
            item = {}
            item["dealwith"] = "Item"
            item["title"] = li.xpath('./a/@title').extract_first()
            item["url"] = li.xpath('./a/@href').extract_first()
            item['id'] = item['url'][28:-5]
            item["price"] = li.xpath(
                './p[@class="price"]/span/text()').extract_first()
            item['price'] = str(float(item["price"][1:]))
            item["hot_word"] = li.xpath(
                './p[@class="search_hot_word"]/text()').extract_first()
            item["from"] = response.meta['from']
            item['brand'] = response.meta['id']
            yield item
            yield scrapy.Request(
                item["url"],
                callback=self.Itemparse,
                meta={'item': item}
            )
        next_url = response.xpath('//li[@class="next"]')
        if next_url:
            yield scrapy.Request(
                "http://category.dangdang.com/" +
                next_url.xpath('./a/@href').extract_first(),
                callback=self.Categoryparse,
            )

    def Itemparse(self, response):
        # 处理商品细节页面
        # print("Call for item spider")
        item = response.meta['item']
        item["dealwith"] = "Detail"
        # Todo 此处处理Item的相关页面, 需要爬取[商品图片, 商品分类, 商品评分, 商品评论, 评论标签]

        item['img_urls'] = response.xpath(
            '//*[@id="main-img-slider"]/li/a/@data-imghref').extract()
        categories = response.xpath(
            '/html/body/div[3]/div[2]//text()').extract()
        all_category = ""
        for category in categories:
            if '\n' in category or '...' in category:
                continue
            all_category += category
        # item['category'] stores the category with format like xxx > xxx > xxx > xxxxxxx
        item['category'] = all_category
        score_temp = response.xpath(
            '//*[@id="product_info"]/div[2]/div/span/span/@style').extract_first()

        if score_temp:
            item['score'] = score_temp[6:-1]
        else:
            item['score'] = "0"
        # TODO the comment of this item is placed by Ajax, namely the js script, which is hard to extract
        # TODO A big problem
        item['comments'] = str({})
        item['comment_tag'] = str([])

        item_comment_url = 'http://product.dangdang.com/index.php?r=comment%2Flist&productId=' + \
            item['id']+'&categoryPath=58.61.03.16.00.00&mainProductId='+item['id']
        yield scrapy.Request(
            item_comment_url,
            callback=self.Commentparse,
            meta={'item': item}
        )

        item_comment_tag_url = 'http://product.dangdang.com/index.php?r=comment%2Flabel&productId=' + \
            item['id']+'&categoryPath=58.61.03.16.00.00'
        yield scrapy.Request(
            item_comment_tag_url,
            callback=self.CommentHeadparse,
            meta={'item': item}
        )

        yield item

    def Commentparse(self, response):
        # 处理商品评论
        item = response.meta['item']
        item["dealwith"] = "comment"
        defaultcomment = {"summary": {"main_product_id": item["id"], "long_comment_count": "0", "pageCount": "0", "pageIndex": "1"}, "html": "\n    \n        <div class=\"item_wrap\">\n           <div class=\"comment_items comment_items_none\" style=\"border-top: none\">\n               <i class=\"icon\"></i>暂无长评\n           </div>\n        </div>\n   "}
        try:
            lists = json.loads(response.text)['data']['list']
            item['comment'] = lists
        except Exception as Err:
            logger.error(Err)
            logger.error(item['id'], item['url'])
            item['comment'] = defaultcomment

        yield item

    def CommentHeadparse(self, response):
        # 处理商品评论头部
        item = response.meta['item']
        item["dealwith"] = "comment_tag"
        try:
            tags = json.loads(response.text)['data']['tags']
            item['comment_tag'] = tags
        except Exception as Err:
            item['comment_tag'] = []
            logger.error(Err)
            logger.error(item)
        yield item
