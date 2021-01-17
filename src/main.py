from scrapy import cmdline
import sys

# cmdline.execute(f"scrapy crawl {sys.argv[1]}".split())
cmdline.execute("scrapy crawl tesco_com_spider".split())
