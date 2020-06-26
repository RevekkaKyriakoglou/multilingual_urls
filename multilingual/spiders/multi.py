# -*- coding: utf-8 -*-
import scrapy
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.loader import ItemLoader
#from pdf_downloader.items import PdfDownloaderItem
#from datablogger_scraper.items import DatabloggerScraperItem

import csv
from scrapy.http import Request
import urllib #to download pdf
from scrapy.http import TextResponse
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
#import requests
import logging

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

#import regex as reov
import re
import multilingual.spiders.similar as mu

class DatabloggerScraperItem(scrapy.Item):
    # The source URL
    url_from = scrapy.Field()
    # The destination URL
    url_to = scrapy.Field()




class MySpider(CrawlSpider):
    
    name = "multi"
    
    f = open("/home/igm/projects/multilingual/biotechnology_sorted_clean.txt")
    #f = open("/home/igm/projects/multilingual/url_test.txt")
    """companies  = [url.strip() for url in f.readlines()]
    

    start_urls = companies
    allow_domains = []
    for link in companies:

        # strip http and www
        domain = link.replace('http://', '').replace('https://', '').replace('www.', '')
        print(domain)
        
        allow_domains.extend([domain])
    """
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    
    rules = [
        Rule(
            LinkExtractor(
                #allow_domains=allow_domains, 
                deny_domains=('.*\twitter.+'),
                #|facebook|linkedin|pinterest|youtube|instagram|github|tiktok)
                canonicalize=True,
                unique=True
            ),
            #follow=True,
            #callback="parse"
        )
    ]
    

    def parse(self, response):
        #logging.warning('+++INSIDE PARSE_LINKS+++')
        #category='hardware'
        #sel=Selector(response)
        restrictions_url = ['google','facebook', 'twitter', 'linkedin','pinterest','youtube','instagram','github','tiktok']
        other_language =  []
        for href in response.xpath('//link[@href][@hreflang]'):
            relative_url = href.xpath("./@href").extract_first()
            absolute_url = response.urljoin(relative_url)
            if absolute_url not in other_language:
                other_language.append(absolute_url)
                
        if len(other_language) > 1:
            #logging.warning("++++++ CASE 1 +++++++++")
            with open('biotechnology_2_1_test.txt','a') as f:
                # write out the url.
                f.write(str(response.url)+ "\n")
                f.write(str(other_language)+ "\n")
                #f.write(str(type(other_language))+ "\n")
                f.write("\n")      

        else:
            #logging.warning("------------OTHER 1---------------")
            #print(other_language)

            for href in response.xpath('//*[not(contains(@href,".css"))][not(contains(@href,"cookies"))][@lang][@href]'):
                relative_url = href.xpath("./@href").extract_first()
                absolute_url = response.urljoin(relative_url)
                if absolute_url not in other_language:
                    other_language.append(absolute_url)
                
            if len(other_language) > 1:
                #logging.warning("++++++ CASE 2 +++++++++")
                #logging.warning(str(absolute_url))
                with open('biotechnology_2_2_test.txt','a') as f:
                    f.write(str(response.url)+ "\n")
                    f.write(str(other_language)+ "\n")
                    f.write("\n")
            
            #only different lang???
            else:
                other_language =  []
                logging.warning("------------OTHER 2---------------")
                #print(other_language)
                other_language.append(response.url)
                lang_original = re.search(r'/[a-zA-z]{2}(-[a-zA-z]{2})?/',str(response.url))

                for href in response.xpath("//*[not(contains(@href,'.ico'))][not(contains(@href,'.svg'))][not(contains(@href,'.jpeg'))][not(contains(@href,'.css'))][not(contains(@href,'.png'))][not(contains(@href,'.css'))][not(contains(@href,'.json'))][not(contains(@href,'.pdf'))][not(contains(@href,'javascript'))][not(contains(@href,'cookies'))][@href]"):
                    relative_url = href.xpath("./@href").extract_first()
                    absolute_url = response.urljoin(relative_url)
                    logging.info(str(absolute_url))
                    condition_lang = re.search(r'/[a-zA-z]{2}(-[a-zA-z]{2})?/',str(absolute_url))
                    logging.warning('LANG_CONDITION : '+str(condition_lang))
                    logging.warning(('LANG_ORIGINAL : '+str(lang_original)))
                    logging.warning('++++++++++++ comparison 1 ++++++++++++')
                    print(mu.comparison(response.url,absolute_url))
                    logging.warning('++++++++++++ comparison 2++++++++++++')
                    if all(res not in absolute_url for res in restrictions_url) and  absolute_url not in other_language and str(condition_lang)!=str(lang_original):
                        #logging.warning("------------TRUE---------------")
                        other_language.append(absolute_url)
                #logging.warning("------------OTHER---------------")
                #print(other_language)

                if len(other_language)> 1:
                    #logging.warning("++++++ CASE 3 +++++++++")
                    with open('biotechnology_2_3_test.txt','a') as f:
                        f.write(str(response.url)+ "\n")
                        f.write(str(other_language)+ "\n")
                        f.write("\n")
