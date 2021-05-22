from bs4 import BeautifulSoup as bs
import requests
import datetime
from dateutil.parser import parse

class Crawler:
    #### constructor ####
    def __init__(self, __titles = None, __scores = None, __reviews = None, __reviewDate = None, __acNum = None):
        self.__titles = __titles or []
        self.__scores = __scores or []
        self.__reviews = __reviews or []
        self.__reviewDate = __reviewDate or []
        self.__acNum = __acNum or []


    #### function ####

    # 현재 페이지 크롤링 #
    def crawl(self, url):
        """
        주어진 페이지의 정보를 파싱하는 함수
        :param url: ChromeDriver 가 탐색중인 페이지의 url 으로 bs4로 파싱할 목표 주소
        """
        self.url = url
        resp = requests.get(self.url)
        soup = bs(resp.text, 'lxml')
        titles = []
        scores = []
        reviews = []
        reviewDate = []
        rd = soup.select('td.num')[1::2]
        for i in range(len(soup.select('.title'))):
            titles.append(soup.select('.title a.movie')[i].text)
            scores.append(soup.select('.title em')[i].text)
            reviews.append(soup.select('.title a.report')[i]['onclick'].split("', '")[2])
            """
            parse 모듈
            """
            reviewDate.append(parse(rd[i].text[-8:]))
            """
            datetime 모듈
            """
            # date = rd[i].text[-8:][:2] + rd[i].text[-8:][3:5] + rd[i].text[-8:][6:]
            # reviewDate.append(datetime.datetime.strptime(date, '%Y%m%d'))
            """
            String형식
            """
            # reviewDate.append(rd[i].text[-8:])
        self.__titles += titles
        self.__scores += scores
        self.__reviews += reviews
        self.__reviewDate += reviewDate

    # 첫 페이지 acNum 크롤링 #
    def crawlAc(self, url):
        """
        첫 페이지의 acNum만을 가져오는 함수
        :param url: ChromeDriver 가 탐색중인 페이지의 url 으로 bs4로 파싱할 목표 주소
        :return: self.__acNum (list형식의 댓글 번호)
        """
        self.url = url
        resp = requests.get(self.url)
        soup = bs(resp.text, 'lxml')
        acNum = []
        for i in soup.select('.ac.num'):
            acNum.append(i.text)
        self.__acNum += acNum
        return self.__acNum


    #### __getter__ ####
    def getTitles(self):
        return self.__titles

    def getScores(self):
        return self.__scores

    def getReviews(self):
        return self.__reviews

    def getReviewDate(self):
        return self.__reviewDate

    def getAcNum(self):
        return self.__acNum

    #### __setter__ ####
    # 값 초기화
    def clearCrawlData(self):
        self.__titles.clear()
        self.__scores.clear()
        self.__reviews.clear()
        self.__reviewDate.clear()
        self.__acNum.clear()