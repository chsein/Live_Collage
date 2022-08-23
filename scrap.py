import requests
import re
import os 
import numpy as np
import cairosvg 
import cv2
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def scrapSignalKeyword():
    url = 'https://api.signal.bz/news/realtime'
    resp = requests.get(url=url)
    top10dict = resp.json()['top10']
    return [t['keyword'] for t in top10dict]


def cleanArticle(content):
    cleanr_image = re.compile('<em class="img_desc">.*?</em>')
    cleanr_tag = re.compile('<.*?>')
    cleanr_email = re.compile('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')        
    rmve_bracket = re.compile("\(.*\)")
    rmve_bracket2 = re.compile("\[.*\]" )  
    cleantext = re.sub(cleanr_image, '', content)
    cleantext = re.sub(cleanr_tag, '', cleantext)
    cleantext = re.sub(cleanr_email, '', cleantext)
    cleantext = re.sub(rmve_bracket, '', cleantext)
    cleantext = re.sub(rmve_bracket2, '', cleantext)

    return cleantext.strip()

def clean_text(inputString):
    text_rmv = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', inputString)
    return text_rmv.strip()

def scrapNaverNewsKeyword(key, article_num, headers, sort='1', length=350):
    articles = []
    links = [] 
    page_num = 0
    while True:
        url = 'https://search.naver.com/search.naver?where=news'
        page = f'{page_num}1'
        resp = requests.get(url, params={'sm':'tab_jum', 'query':key, 'sort':sort, 'start':page}) 
        news_search = BeautifulSoup(resp.text, 'html.parser') 
        url_list = [d['href'] for d in news_search.find_all('a', attrs={'class':'info'}) if d.text=='네이버뉴스']
        for url in url_list:    
            news = requests.get(url,headers=headers) #그 뉴스링크에 다시 접근
            news_html = BeautifulSoup(news.text,"html.parser") #html로 변환
            newstype = news.url.split('.')[0].split('//')[-1]

            if newstype == 'sports':
                title = news_html.find('h4', {'class':'title'}).text
                content = news_html.find_all('div', {'id':'newsEndContents'})  ##스포츠 일때는 sid가 없어서 1순위 확인
                content = str(content)
                content = content.split('<p class="source">') 
                text = content[0]            
            elif newstype == 'entertain':
                title = news_html.find('h2', {'class':'end_tit'}).text
                text = ' '.join([paragraph.text for paragraph in news_html.find_all('div', {'id':'articeBody'})]) 
            else:
                title = news_html.find('h2', {'class':'media_end_head_headline'}).text
                text = ' '.join([paragraph.text for paragraph in news_html.find_all('div', {'class':'go_trans _article_content'})]) 

            cleaned_text = cleanArticle(text)
            if len(cleaned_text) > length:
                articles.append((title.strip(), cleaned_text))
                links.append(url)
            if len(articles) == article_num:
                break
        if len(articles) == article_num:
            break
        page_num+=1  
    return articles, links

def saveArticles(articles, path):
    for title, content in articles:
        f = open(os.path.join(path, clean_text(title) + '.txt'), 'w', encoding='utf8')
        f.write(content)
        f.close()

def set_chrome_driver(headers):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("user-agent="+headers["user-agent"])
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    return driver

def check_txt_logo(txt, in_=True):
  txt = txt.upper()
  if in_:
    return '로고' in  txt or 'LOGO' in  txt or 'CI' in  txt or '휘장' in txt
  else:
    return '로고' not in txt and 'LOGO' not in  txt and 'CI' not in  txt and '휘장' not in txt


def scrapNamuImg(key, path, headers,namuKeyword_kind='person'):
    driver = set_chrome_driver(headers)

    url = 'https://namu.wiki/w/'+key
    driver.get(url=url)
    html = driver.page_source
    driver.close()
    soup = BeautifulSoup(html, 'lxml')

    if namuKeyword_kind == 'person':
        imglink = [il['src'] for il in soup.find_all('img', attrs={'class':'dVTtICxy'}) if not il.find_parent('dd') and check_txt_logo(il['alt'], in_=False) ]
        for i, link in enumerate(imglink):
            res=requests.get("https:"+link,headers=headers)
            if 'svg' not in res.text and 'video' not in res.text:
                urlopen_img = Image.open(BytesIO(res.content))
                # counts = np.unique(np.array(urlopen_img.split()[-1]), return_counts=True)[1]
                # ratio = counts[0]/np.sum(counts)
                if urlopen_img.size[1]*urlopen_img.size[0] > 100000  :
                    print(res.url)
                    if path:
                        urlopen_img.save(path,'png')
                    break
    else :
        key_ = soup.find('title').text.replace(' - 나무위키','').upper()
        imglink = [il['src'] for il in soup.find_all('img', attrs={'class':'dVTtICxy'}) if not il.find_parent('dd') and (key_ in  il['alt']) and check_txt_logo(il['alt']) ]
        if len(imglink) < 1:
            imglink = [il['src'] for il in soup.find_all('img', attrs={'class':'dVTtICxy'}) if not il.find_parent('dd') and check_txt_logo(il['alt'])]
        for i, link in enumerate(imglink):
            res=requests.get("https:"+link,headers=headers)
            try:
                urlopen_img = Image.open(BytesIO(cairosvg.svg2png(res.content)))
                print(res.url)
                if path:
                    urlopen_img.save(path,'png')
                break
            except:
                urlopen_img = Image.open(BytesIO(res.content))
                print(res.url)
                if path:
                    urlopen_img.save(path,'png')
                break

def save_article_img(url, headers, save_path, height=300):
  try:
    res = requests.get(url,headers=headers) #그 뉴스링크에 다시 접근
    soup = BeautifulSoup(res.text,"html.parser") 
    newstype = res.url.split('.')[0].split('//')[-1]
    if newstype == 'sports' :
      img_url = soup.find('span', attrs = {'class':'end_photo_org'}).img['src']

    else:
      try:
        img_url = soup.find('img', attrs = {'id':'img1'})['data-src']
      except:
        img_url = soup.find('img', attrs = {'id':'img1'})['src']
    img_res = requests.get(img_url,headers=headers)
    tmp_img = Image.open(BytesIO(img_res.content))
    tmp_img = np.array(tmp_img)
    aspect_ratio = float(height) / tmp_img.shape[0]
    dsize = (int(tmp_img.shape[1] * aspect_ratio), height)

    resized = cv2.resize(tmp_img, dsize, interpolation=cv2.INTER_AREA)

    y,x,h,w = (0,0,resized.shape[0], resized.shape[1])
    if resized.shape[1] > 500:
        mid_x = w//2
        offset_x = 250
        img_re = resized[0:resized.shape[0], mid_x-offset_x:mid_x+offset_x]
    else:
        # 그림 주변에 검은색으로 칠하기
        w_x = (500-(w-x))/2  # w_x = (300 - 그림)을 뺀 나머지 영역 크기 [ 그림나머지/2 [그림] 그림나머지/2 ]
        h_y = (300-(h-y))/2

        if(w_x < 0):         # 크기가 -면 0으로 지정.
            w_x = 0
        elif(h_y < 0):
            h_y = 0

        M = np.float32([[1,0,w_x], [0,1,h_y]])  #(2*3 이차원 행렬)
        img_re = cv2.warpAffine(resized, M, (500, 300))
    img_re = cv2.cvtColor(img_re, cv2.COLOR_BGR2RGB)
    cv2.imwrite(save_path,img_re)
    return img_re
  except:
    background = np.zeros((500, 300, 3))
    cv2.imwrite(save_path,background)
    return background



