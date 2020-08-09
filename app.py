from flask import Flask, render_template, request, session, redirect
import csv
import requests
from bs4 import BeautifulSoup as bs
import bs4
from openpyxl import Workbook
from itertools import chain
from openpyxl import load_workbook
from wordcloud import WordCloud
import re
from konlpy.tag import Okt
import pandas as pd
from functools import wraps
import pymongo
from pymongo import MongoClient

from datetime import date, timedelta
import naver_reviews
import daum_reviews
import error_dicts
from collections import Counter




okt = Okt()

app = Flask(__name__)
app.secret_key = b"7\xe39,\x8eE\xff\xe5\x9b\x95\xc6,\xfcX'b"



#database
cluster = MongoClient("mongodb+srv://sangbeen:12341234@boilerplate.cw0as.gcp.mongodb.net/user_login_system?retryWrites=true&w=majority")
db = cluster["user_login_system"]
collection = db["user"]


#Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap 

# Route
from user import routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('test.html')


def find_dict_mismatch(one_line , dict_list):   #국어사전
    cnt = 0
    for one_word in one_line:
        if one_word not in dict_list:
            cnt += 1
            print(one_word)
    return cnt

def find_dict_match(one_line , dict_list):  #특수문자 사전
    cnt = 0
    for one_word in one_line:
        if one_word in dict_list:
            cnt += 1
            print(one_word)
    return cnt

'''
def find_dict_match(one_line, dict_list):
    cnt = 0
    f = open("dict.txt", 'rt', encoding='UTF8') 
    special_dict = []
    while True:
        error_word = f.readline()
        error_word = error_word.strip()

        if not error_word: break
        special_dict.append(error_word)
        

        cnt = cnt + one_line.count(error_word)
        #print(error_word)
    f.close()
    return cnt
'''
def get_article_contents(news_link):
    contents=[]
    res = requests.get(news_link)
    soup = bs(res.text, 'lxml')
    body = soup.find('div', class_="_article_body_contents")
    for content in body:
        if type(content) is bs4.element.NavigableString and len(content)>50:
             contents.append(content.strip())
    return contents


def preprocess_string(string_list):
    noun_list = []
    for line in string_list:
        line = re.sub('\s', " ", line)  #텍스트파일 전처리.
        nouns = okt.nouns(line)
        noun_list.append(nouns)

    return noun_list

'''

@app.route('/post', methods=['POST'])
def post():
    value = request.form['test']
    data=[]
    section_ids = ["100", "101", "102"]
    for section_id in section_ids:
        url = value
        url = url.replace(str(100), "%s") % section_id
        res = requests.get(url)
        soup = bs(res.text, "lxml")
        lis=soup.find_all('li', class_= "ranking_item", limit=3)
        for li in lis:
            news_link = "https://news.naver.com" + li.a.attrs.get('href')
            #####[뉴스 내용 가져오기 함수 추가]
            s = get_article_contents(news_link)
            data.append(s)

#이중 리스트 하나로 만들기
    data=list(chain.from_iterable(data))

#엑셀 생성
    wb = Workbook()
    ws = wb.create_sheet("뉴스",0)
    row=2
    ws.cell(1,1,"뉴스")

#엑셀에 입력
    for i in data:
        ws.cell(row,1,i)
        row+=1
    wb.save('output.xlsx')

    wb = load_workbook('output.xlsx', read_only = True)
    data1 = wb.active
    script=[]
    for row in data1.iter_rows():
        for cell in row:
            var1=cell.value
            script.append(var1)

    line_cnt = 0
    error_cnt = 0

    noun_list = preprocess_string(script)
    
    #-------
    
    excel_data_df = pd.read_excel('korean_dict.xlsx', sheet_name='NIADic')
    korean_dict_list = excel_data_df['term'].tolist()
    

    f = open("dict.txt", 'rt', encoding='UTF8') 
    special_dict = []
    while True:
        error_word = f.readline()
        error_word = error_word.strip()

        if not error_word: break
        special_dict.append(error_word)
    #-------
    

    for one_line in noun_list:
        line_cnt += 1
        error_cnt += find_dict_mismatch(one_line, korean_dict_list)
        error_cnt += find_dict_match(one_line, special_dict)

    error_pcnt = str(error_cnt / len(noun_list) * 100)
    #print(error_cnt)
    #print(line_cnt)
    return "품질 오류 : " + error_pcnt + "% 입니다."

'''
#@app.route('/user/signup', methods=['POST'])

@app.route('/post', methods=['POST'])
def crawl():
    url_3= request.form['test']
    #url_3="https://news.naver.com/main/read.nhn?mode=LSD&sid1=001&oid=023&aid=0003547854"
    print(url_3)
    if "naver" in url_3:
        naver_reviews.capture_replys_naver(url_3, excel_name="comments")
    else:
        daum_reviews.capture_replys_daum(url_3, excel_name="comments")

    # 엑셀 리스트로 읽어들이기
    wb = load_workbook("comments.xlsx", read_only=True)
    data1 = wb.active
    script = []
    for row in data1:
        for cell in row:
            var1 = cell.value
            script.append(var1)
    script[0] = "comments"

    # 전체 오류단어 리스트 생성
    errorfre_list = []
    for one_line in script:
        i = error_dicts.find_dict(one_line)[1]
        errorfre_list.append(i)
    errorfre_list = list(chain.from_iterable(errorfre_list))

    # 오류단어 단어 dict형태로 분류
    pred = Counter(errorfre_list).most_common()
    err_dict = dict(pred)
    data_key=list(err_dict.keys())
    data_value=list(err_dict.values())



    #도넛 차트 변수
    ra_1 = len(errorfre_list)
    cnt_1 = 0
    for i in script:
        cnt_1 +=1
    ratio= [cnt_1/(cnt_1 + ra_1), ra_1/(ra_1 + cnt_1)]



    return render_template("result.html" ,ratio=ratio, data=data_key, data1=data_value)
