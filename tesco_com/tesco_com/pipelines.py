# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, JSON, Text
from dotenv import dotenv_values
import os

Base = declarative_base()
os.chdir("..")
dotenv_path = os.path.join(os.getcwd(), '.env')
config_env = dotenv_values(dotenv_path)


class ProductsTable(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product_url = Column(String(200), nullable=False)
    product_id = Column(Integer, nullable=False)
    product_image_url = Column(String(200))
    product_title = Column(String(200), nullable=False)
    product_category = Column(String(50))
    product_price = Column(DECIMAL(precision=2))
    product_description = Column(Text)
    return_address = Column(String(1000))
    net_contents = Column(String(100))
    name_and_address = Column(String(1000))
    reviews = Column(JSON, nullable=True)
    ubnps = Column(JSON, nullable=True)

    def __init__(self,
                 product_url,
                 product_id,
                 product_image_url,
                 product_title,
                 product_category,
                 product_price,
                 product_description,
                 return_address,
                 net_contents,
                 name_and_address,
                 reviews,
                 ubnps):
        self.product_url = product_url
        self.product_id = product_id
        self.product_image_url = product_image_url
        self.product_title = product_title
        self.product_category = product_category
        self.product_price = product_price
        self.product_description = product_description
        self.return_address = return_address
        self.net_contents = net_contents
        self.name_and_address = name_and_address
        self.reviews = reviews
        self.ubnps = ubnps


class TescoComPipeline(object):
    def __init__(self):
        basehost = config_env["HOST"]
        basename = config_env["DB_NAME"]
        admin = config_env["ADMIN"]
        pass_admin = config_env["PASS_ADMIN"]

        self.engine = create_engine(f"mysql+pymysql://{admin}:{pass_admin}@{basehost}/{basename}")

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)

    def process_item(self, item, spider):
        dt = ProductsTable(item['product_url'],
                           item['product_id'],
                           item['product_image_url'],
                           item['product_title'],
                           item['product_category'],
                           item['product_price'],
                           item['product_description'],
                           item['return_address'],
                           item['net_contents'],
                           item['name_and_address'],
                           item['reviews'],
                           item['ubnps'])
        self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
