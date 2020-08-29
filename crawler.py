from flask import Flask, render_template, request, session, redirect
from datetime import date, timedelta
import naver_reviews
import daum_reviews
from dictionary import Dictionary
from collections import Counter
from openpyxl import load_workbook
from itertools import chain
import pandas as pd
#from app import app


class Crawler:
    def crawl(self):
        url_3= request.form['url_input']
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


        #(추가) 한글사전 추가
        '''excel_data_df = pd.read_excel('korean_dict.xlsx', sheet_name='NIADic')
        korean_dict_list = excel_data_df['term'].tolist()
        dictionary = Dictionary(korean_dict_list)
        print('[한글 사전 준비 완료]')'''


        #(추가) 전처리. 불용어 거르고 명사화
        #noun_list = []
        #noun_list = dictionary.preprocess_string(script)

        dictionary = Dictionary()


        
        # 전체 오류단어 리스트 생성
        errorfre_list = []
        for one_line in script:
            i = dictionary.find_dict(one_line)[1]
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
