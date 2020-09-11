# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
from Tachie_get.settings import IMAGES_STORE
from urllib.parse import urlparse
from urllib.request import unquote


# 修改管道类的父类为 scrapy.pipelines.images.ImagesPipeline
class TachieGetPipeline(ImagesPipeline):
    # 重载get_media_requests()函数，可以为url生成request
    def get_media_requests(self, item, info):
        url = item['img_url']
        yield Request(url)

    # # 图片下载完毕后，处理结果会以二元组result的方式返回给item_completed()函数
    # # 二元数组的定义如下：(success, image_info_or_failure)
    # # 第一个元素为下载是否成功，第二个元素是一个字典
    # def item_completed(self, results, item, info):
    #     # 列表推倒式，获取图片的保存路径
    #     image_url = [x["path"] for ok, x in results if ok]
    #     print(results)
    #     # 对文件进行重命名
    #     os.rename(IMAGES_STORE + '/' + image_url[0], IMAGES_STORE + '/' + item['name'] + '.' + item['img_class'])
    #     return item

    # 或者使用下列命名方式
    def file_path(self, request, response=None, info=None):
        return os.path.basename(unquote(urlparse(request.url).path))  # 获取相对路径，将url中的中文进行解码
