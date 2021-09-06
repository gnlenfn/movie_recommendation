from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from collections import defaultdict
import datetime

BASE_URL = "https://movie.naver.com/movie"

def get_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup, page

def get_current_movie_code(num, refresh=False):
    """
    현재 상영중인 영화 num개의 영화코드를 파일로 저장, 리턴.

    리턴:
        - 현재 상영중인 num개 영화의 제목과 코드 DataFrame
    """
    
    page_url = f'{BASE_URL}/running/current.naver'
    soup, _ = get_page(page_url)

    target = soup.select('#content > div.article > div > div.lst_wrap > ul > li > dl > dt > a')
    information = soup.select('#content > div.article > div:nth-of-type(1) > div.lst_wrap > ul > li > dl > dd > dl.info_txt1 > dd:nth-of-type(1)')     
    ticket = soup.select('#content > div.article > div:nth-of-type(1) > div.lst_wrap > ul > li > dl > dd.star > dl.info_exp > dd > div > span.num')

    if os.path.isfile("./app/services/current_movie_code.csv"):
        table = pd.read_csv("./app/services/current_movie_code.csv", names=['title', 'code'], sep=';', header=None)
    else:
        table = pd.DataFrame(columns=['title', 'code', 'opening_date', 'reserved'])
        
    for movie, opening, reserve in zip(target[:num], information[:num], ticket[:num]):
        title = movie.text
        code =  movie['href'].split("=")[1]
        opening_date = opening.text.split()[-2]
        ticketing = float(reserve.text)

        if table['title'].empty or title not in set(table['title']):
            table = table.append({"title": title, "code": code, 
                                "opening_date": opening_date, 'reserved': ticketing}, ignore_index=True)

    return table

def get_movie_code(movie_title):
    """
    영화 제목을 통해 해당 영화의 코드를 알아내는 함수.
    
    파라미터:
        - 영화제목 String
    리턴:
        - 영화 코드 String

    """
    page_url = f"{BASE_URL}/search/result.naver?query={movie_title}&section=all&ie=utf8"
    soup, _ = get_page(page_url)

    target = soup.select_one('#old_content > ul > li > dl > dt > a')
    code = target['href'].split("=")[1]

    return code


def get_reviews(movie_code, page_num=1):
    """
    영화의 리뷰를 페이지별로 스크레이핑.

    파라미터:
        - movie_code: 영화 코드
        - page_num: 스크레이핑 할 페이지 번호
    리턴:
        스크레이핑한 리뷰와 별점 딕셔너리 리스트
    """
    page_url = f"{BASE_URL}/point/af/list.naver?st=mcode&sword={movie_code}&target=after&page={page_num}"
    soup, _ = get_page(page_url)
    
    review_dict = defaultdict(list)
    text = soup.find_all('td', class_='title')
    for comment in text:
        review = comment.find('br').next.strip()
        score = comment.find('em').text
        review_dict['review_text'].append(review)
        review_dict['review_star'].append(score)

    return review_dict

def scrap_reviews_of_num(movie_code, review_num):
    """
    주어진 리뷰 수 만큼 스크레이핑 하여 리스트를 리턴.
    
    파라미터:
        - movie_code: 스크레이핑 할 영화 코드
        - review_num: 스크레이핑 할 리뷰 수
    리턴:
        - 리뷰와 별점으로 이루어진 딕셔너리의 리스트
    """
    reviews = []
    page_num = 1
    while True:
        on_this_page = get_reviews(movie_code, page_num)['review_text']
        if len(reviews) + len(on_this_page) > review_num:
            break

        reviews += on_this_page
        page_num += 1

    
    for r in on_this_page:
        if len(reviews) + 1 > review_num:
            break
        reviews.append(r)
    
    return reviews

def get_poster(movie_code):
    page_url = f"{BASE_URL}/point/af/list.naver?st=mcode&sword={movie_code}&target=after&page=1"
    soup, _ = get_page(page_url)

    target = soup.select_one('#old_content > div.choice_movie_box > div.choice_movie_info > div.fl > a > img')
    poster_url = target['src']

    return poster_url


def get_opening_date(movie_code):
    page_url = f"{BASE_URL}/bi/mi/basic.naver?code={movie_code}"
    soup, _ = get_page(page_url)

    target = soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd > p > span')[-1].select('a')
    #print(target)
    date = ''
    for i in target:
        print(i)
        date += i.text
    date = date.strip()
    if len(date) > 10:
        date = date.split()[-1]
    return datetime.datetime.strptime(date, '%Y.%m.%d')

