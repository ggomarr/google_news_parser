import sys
import time
import random
import logging
import urllib2 
from lxml import etree

class gnp:
    def __init__(self,params='hl=en&ned=us',root_url='https://news.google.com/news/',
                 max_retries=10,wait_between_requests=5,
                 log_level=logging.DEBUG):
        self.root_url=root_url+'?'+params
        self.search_url=root_url+'search/section/q/{q}/{q}'+'?'+params
        self.explore_url=root_url+'explore/section/q/{q}/{q}'+'?'+params
        self.max_retries=max_retries
        self.wait_between_requests=wait_between_requests
        self.log_level=log_level
        self.news={}
        self.checked_news=set()
    def dig_into_news(self,dig_levels=0,seed_news=None,seed_headlines=True,seed_sections=True):
        logger=logging.getLogger('parse_url')
        logger.setLevel(self.log_level)
        logger.info('Digging for news {} levels down...'.format(dig_levels))
        logger.debug('Adding main news...')
        if seed_news!=None:
            self.seed_news(seed_news)
        if self_headlines:
            self.add_news(self.extract_main_news())
        if seed_sections:
            news_lst=[]
            for theme in self.news:
                logger.debug('Adding main news about {}...'.format(theme))
                time.sleep((1+random.random())*self.wait_between_requests)
                news_lst.append(self.extract_topic_news(theme))
                self.checked_news.add(theme)
            logger.debug('Merging theme news into main...')
            for news in news_lst:
                self.add_news(news)
        for depth in range(dig_levels):
            logger.debug('Digging down to level {}...'.format(depth))
            news_lst=[]
            for theme in self.news:
                logger.debug('Adding deeper news about {}...'.format(theme))
                for topic in self.news[theme]['extra_topics']:
                    if topic not in self.checked_news:
                        logger.debug('Adding news about {} {}...'.format(theme,topic))
                        time.sleep((1+random.random())*self.wait_between_requests)
                        news_lst.append(self.extract_topic_news(topic,theme=theme))
                        self.checked_news.add(topic)
            logger.debug('Merging level {} news into main...'.format(depth))
            for news in news_lst:
                self.add_news(news)
    def seed_news(self,seed_news):
        for theme in seed_news:
            self.news[theme]={'cards':[],'extra_topics':set(seed_news[theme])}
    def add_news(self,news):
        for theme in news:
            if theme not in self.news:
                self.news[theme]=news[theme]
            else:
                self.news[theme]['cards'].extend(news[theme]['cards'])
                self.news[theme]['extra_topics'].update(news[theme]['extra_topics'])
    def export_news_list(self):
        out={}
        for theme in self.news:
            out[theme]=[link for card in self.news[theme]['cards'] for link in card]
        return out
    def page_is_new(self,page):
        try:
            if page[1][2][0][0][0].text=='Search':
                return False
        except:
            return True
    def parse_url(self,url):
        logger=logging.getLogger('parse_url')
        logger.setLevel(self.log_level)
        retry=0
        while retry<self.max_retries:
            logger.info('Parsing {}...'.format(url))
            request=urllib2.Request(url) 
            response=urllib2.urlopen(request).read() 
            page=etree.HTML(response)
            page_is_new=self.page_is_new(page)
            if page_is_new:
                return page
            logger.debug('{} had the old format! Waiting and retrying...'.format(url))
            time.sleep(self.wait_between_requests)
        logger.warning('Error grabbing {} in the right format!'.format(url))
        return False        
    def grab_node_links(self,node,node_level='',node_path='',full_address=False):
        out=[]
        if 'href' in node.keys():
            node_link=node.attrib['href']
            if not full_address or node_link[:4]=='http':
                out.append(node_link)
        for n in range(len(node)):
            out.extend(self.grab_node_links(node[n],node_level+'|{}'.format(n),
                                            node_path+'|{}'.format(node[n].tag),
                                            full_address=full_address))
        return list(set(out))
    def grab_card_related_topics(self,card):
        related_topics=[]
        if len(card[0][0][0])>3:
            related_topics_node=card[0][0][0][3]
            for topic_node in related_topics_node[1:]:
                topic=topic_node[0][0].text.encode('iso-8859-1')
                related_topics.append(topic)
        return related_topics
    def extract_main_news(self):
        logger=logging.getLogger('extract_main_news')
        logger.setLevel(self.log_level)
        logger.info('Extracting news from the front page...')
        main_news={}
        page=self.parse_url(self.root_url)
        if page!=False:
            try:
                logger.debug('Getting a hold of the news section...')
                groups=page[1][1][3][0][0][0]
                for group in groups:
                    try:
                        logger.debug('Grabbing new section...')
                        topic=group[0][0][0][0][0].text
                        main_news[topic]={'cards':[],'extra_topics':set()}
                        logger.debug('Grabbing cards about {}...'.format(topic))
                        cards=group[0][0]
                        for card_pos in range(1,len(cards)):
                            try:
                                logger.debug('Grabbing card {} about {}...'.format(card_pos,topic))
                                card=cards[card_pos]
                                links=card[0][0]
                                logger.debug('Crawling card {} about {} for links...'.format(card_pos,topic))
                                main_news[topic]['cards'].append(self.grab_node_links(links,full_address=True))
                                logger.debug('Crawling card {} about {} for extra topics...'.format(card_pos,topic))
                                main_news[topic]['extra_topics'].update(self.grab_card_related_topics(card))
                            except:
                                logger.warning('Error grabbing card {} about {}! Card skipped'.format(card_pos,topic))
                                logger.warning(sys.exc_info()[1])
                    except:
                        logger.warning('Failed grabbing section! Section skipped')
                        logger.warning(sys.exc_info()[1])
            except:
                logger.warning('Error parsing front page!')
                logger.warning(sys.exc_info()[1])
        else:
            logger.warning('Could not get the new version of the front page! Giving up...')
        return main_news
    def extract_topic_news(self,topic,theme='',use_explore=True):
        logger=logging.getLogger('extract_topic_news')
        logger.setLevel(self.log_level)
        logger.info('Extracting news about {} from the search page...'.format(topic))
        topic_key=(theme+' '+topic).strip()
        topic_news={topic_key:{'cards':[],'extra_topics':set()}}
        if use_explore:
            aux_url=self.explore_url
        else:
            aux_url=self.search_url
        page=self.parse_url(aux_url.format(q=urllib2.quote(topic)))
        if page!=False:
            try:
                logger.debug('Grabbing cards about {}...'.format(topic))
                cards=page[1][1][3][0][0][0][0][0]
                for card_pos in range(1,len(cards)):
                    try:
                        logger.debug('Grabbing card {} about {}...'.format(card_pos,topic))
                        card=cards[card_pos]
                        links=card[0][0]
                        logger.debug('Crawling card {} about {} for links...'.format(card_pos,topic))
                        topic_news[topic_key]['cards'].append(self.grab_node_links(links,full_address=True))
                        logger.debug('Crawling card {} about {} for extra topics...'.format(card_pos,topic))
                        topic_news[topic_key]['extra_topics'].update(self.grab_card_related_topics(card))
                    except:
                        logger.warning('Error grabbing card {} about {}! Card skipped'.format(card_pos,topic))
                        logger.warning(sys.exc_info()[1])
            except:
                logger.warning('Failed grabbing cards! Search skipped')
                logger.warning(sys.exc_info()[1])               
        else:
            logger.warning('Could not get the new version of the search page! Giving up...')
        return topic_news
