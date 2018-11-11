import sys
import time
import logging
import urllib.request
import urllib.parse
from lxml import etree

class gnp:
    def __init__(self,root_url='https://news.google.com/',lang='hl=en-US&gl=US&ceid=US:en',
                 log_level=logging.DEBUG):
        self.root_url=root_url
        self.lang=lang
        self.search_url=root_url+'search?q={q}&'+lang
        self.log_level=log_level
        self.news={}
    def seed_news(self,seed_news):
        for theme in seed_news:
            self.news[theme['label']]={'links':set(),'topic_url':self.search_url.format(q=theme['term'])}
    def parse_url(self,url):
        logger=logging.getLogger('parse_url')
        logger.setLevel(self.log_level)
        logger.info('Parsing {}...'.format(url))
        try:
            request=urllib.request.Request(url) 
            response=urllib.request.urlopen(request).read()
            page=etree.HTML(response)
            return page
        except:
            logger.warning('Error parsing {}!'.format(url))
            return False        
    def extract_main_news(self):
        logger=logging.getLogger('extract_main_news')
        logger.setLevel(self.log_level)
        logger.info('Extracting news from the front page...')
        page=self.parse_url(self.root_url+'?'+self.lang)
        if page!=False:
            try:
                logger.debug('Getting a hold of the news section...')
                main=page[1][1][3][0][0][0][0][1][0]
                label='Unknown'
                for node in main:
                    if node[0].find('h2') is not None:
                        logger.debug('Label node detected. Extracting label...')
                        try:
                            label=node[0][0][0].text
                            logger.debug('New label {} extracted...'.format(label))
                        except:
                            logger.warning('Error extracting label from label node!')
                            logger.warning(sys.exc_info()[1])
                            label='Unknown'
                        logger.debug('Extracting topic link...')
                        try:
                            topic_url=self.root_url+node[0][0][0].attrib['href'][2:]+'?'+self.lang
                        except:
                            logger.warning('Error extracting topic link from label node!')
                            logger.warning(sys.exc_info()[1])
                            topic_url=''
                        if label not in self.news:
                            self.news[label]={'links':set(),'topic_url':topic_url}
                    else:
                        logger.debug('Articles node detected. Extracting articles...')
                        for subnode in node.iterdescendants(tag='article'):
                            logger.debug('Extracting article link...')
                            try:
                                self.news[label]['links'].add(self.root_url+subnode[0].attrib['href'][2:])
                            except:
                                logger.warning('Error extracting article link from article node!')
                                logger.warning(sys.exc_info()[1])

            except:
                logger.warning('Error parsing front page!')
                logger.warning(sys.exc_info()[1])
        else:
            logger.warning('Could not get the front page! Giving up...')
    def extract_topic_news(self,topic_url,label):
        logger=logging.getLogger('extract_topic_news')
        logger.setLevel(self.log_level)
        logger.info('Extracting news about {} from {}...'.format(label,topic_url))
        page=self.parse_url(topic_url)
        if page!=False:
            try:
                logger.debug('Getting a hold of the articles section...')
                for subnode in page.iterdescendants(tag='article'):
                    logger.debug('Extracting article link...')
                    try:
                        self.news[label]['links'].add(self.root_url+subnode[0].attrib['href'][2:])
                    except:
                        logger.warning('Error extracting article link! Skipping article...')
                        logger.warning(sys.exc_info()[1])
            except:
                logger.warning('Error parsing topic specific page! Giving up...')
                logger.warning(sys.exc_info()[1])               
        else:
            logger.warning('Could not get the topic specific page! Giving up...')
    def extract_all_topic_news(self):
        logger=logging.getLogger('extract_all_topic_news')
        logger.setLevel(self.log_level)
        logger.info('Extracting all topic news...')
        for label in self.news:
            self.extract_topic_news(self.news[label]['topic_url'],label)
    def export_news_list(self):
        out={}
        for label in self.news:
            out[label]=list(self.news[label]['links'])
        return out
