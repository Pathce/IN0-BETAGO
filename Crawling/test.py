from ChromeDriverController import ChromeDriver
from Crawler import Crawler
import pandas as pd

def CrawlPage(cnt=10):
    """
    cnt만큼 페이지 크롤링 하는 함수
    :param cnt: default 10, 크롤링 횟수 결정
    :return: {titles:(영화제목 리스트), scores:(평점리스트), reviews:(리뷰내용), reviewDate:(리뷰날짜)}
    """
    cr.clearCrawlData() # 크롤링 시작 전 데이터 초기화
    if(cnt == 1):
        cnt1 = 1
        for i in range(cnt1):
            try:
                cr.crawl(cd.__getUrl__())
            except () as e:
                print(f"Error!!!!!!!! : {e}")
    elif(cnt <= 5):
        cnt1 = 1
        cnt2 = cnt - cnt1
        for i in range(cnt1):
            try:
                cr.crawl(cd.__getUrl__())
                cd.buttonClick(f'//*[@id="old_content"]/div[2]/div/a[2]')
            except () as e:
                print(f"Error!!!!!!!! : {e}")
        for i in range(cnt2):
            try:
                cr.crawl(cd.__getUrl__())
                cd.buttonClick(f'//*[@id="old_content"]/div[2]/div/a[{i + 4}]')
            except () as e:
                print(f"Error!!!!!!!! : {e}")
    elif(cnt > 5 and cnt < 97):
        cnt1 = 1
        cnt2 = 4
        cnt3 = cnt - (cnt2 + cnt1)
        for i in range(cnt1):
            try:
                cr.crawl(cd.__getUrl__())
                cd.buttonClick(f'//*[@id="old_content"]/div[2]/div/a[2]')
            except () as e:
                print(f"Error!!!!!!!! : {e}")
        for i in range(cnt2):
            try:
                cr.crawl(cd.__getUrl__())
                cd.buttonClick(f'//*[@id="old_content"]/div[2]/div/a[{i + 4}]')
            except () as e:
                print(f"Error!!!!!!!! : {e}")
        for i in range(cnt3):
            try:
                cr.crawl(cd.__getUrl__())
                cd.buttonClick(f'//*[@id="old_content"]/div[2]/div/a[8]')
            except () as e:
                print(f"Error!! : {e}")
        cr.crawl(cd.__getUrl__())
    else:
        result = {[''], [''], [''], ['']}
        return result

    cTitles = cr.getTitles()
    cScores = cr.getScores()
    cReviews = cr.getReviews()
    cReviewDate = cr.getReviewDate()

    result = {"titles":cTitles,
              "scores":cScores,
              "reviews":cReviews,
              "reviewDate":cReviewDate}

    return result

# 마지막으로 시행된 크롤링 첫 페이지 저장
def lastRun(acNum):
    """
    acNum을 CSV형식 파일로 저장 (last_crawling_ac_num.csv)
    :param acNum: 크롤링한 댓글 id 리스트
    """
    ac = pd.Series(acNum)
    ac.to_csv('last_crawling_ac_num.csv', index=False)

def checkAcNum(acNum):
    """
    크롤링으로 새로 획득한 acNum 과 저장된 acNum 을 비교해 크롤링 횟수를 결정
    :param acNum:크롤링으로 새로 획득한 acNum 의 리스트
    :return:[크롤링할 페이지 수, 이미 크롤링해 제외할 데이터 수]
    """
    ac = list(pd.read_csv('last_crawling_ac_num.csv')['0'].values)
    num1 = int(ac[0])
    num2 = int(acNum[0])
    diff = num2 - num1
    cnt = int(diff / 10)
    print(f"diff : {diff}\n"
          f"cnt  : {cnt}")
    if cnt >= 50:
        return [50, 0]             # 크롤링 횟수(기본값 50), 마지막 페이지 크롤링 제외 범위(기본값 0)
    elif cnt == 0:
        if diff == 0:
            return [0, 0]
        else:
            return [0, (10 - diff % 10)]
    else:
        if diff == 0:
            return [cnt, 0]
        else:
            return [cnt, (10 - diff % 10)]

# 메인
if __name__ == '__main__':
    # 저장할 리스트 생성
    titles = []
    scores = []
    reviews = []
    reviewDate = []
    acNum = []
    crResult = {}       # 함수 결과값 받을 딕셔너리

    # 크롬 드라이버 컨트롤러 객체 cd 생성
    cd = ChromeDriver(f"https://movie.naver.com/movie/point/af/list.nhn")
    # 크롤러 객체 cr 생성
    cr = Crawler()

    acNum = cr.crawlAc(cd.__getUrl__())
    # 기록 검사해 크롤링 횟수 설정
    T_CNT = checkAcNum(acNum)
    # 다음 크롤링 중복 방지를 위해 첫페이지 acNum 기록 저장
    lastRun(acNum)

    # 크롤링
    crResult = CrawlPage(T_CNT[0])
    titles = crResult["titles"]
    scores = crResult["scores"]
    reviews = crResult["reviews"]
    reviewDate = crResult["reviewDate"]

    # 겹치는 데이터 존재시 삭제
    if(T_CNT[1]):
        del titles[-(T_CNT[1]):]
        del scores[-(T_CNT[1]):]
        del reviews[-(T_CNT[1]):]
        del reviewDate[-(T_CNT[1]):]

    # 크롬드라이버 종료
    cd.driverOff()

    # 객체 제거
    del cd
    del cr

    # 결과값 출력(테스트)
    for i in range(len(titles)):
        print(f'_____________________________________________________________________')
        print(f'title : {titles[i]}')
        print(f'score : {scores[i]}')
        print(f'review : {reviews[i]}')
        print(f'reviewDate : {reviewDate[i]}')

    print(f'total count : {len(titles)}')

