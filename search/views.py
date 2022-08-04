import os
from django.shortcuts import render

from django.views import generic
# from .models import UploadFile

# Create your views here.

# class UploadList(generic.ListView):
#     model = UploadFile

#クラスベースのビューを作るため
from django.views import View

#スクレイピングのコードをインポート
from . import scraping 

import time

import pandas as pd

#拒否したいURLのリスト
DENY_URL_LIST   = []

DENY_TITLE_LIST = []


#Viewを継承してGET文、POST文の関数を作る
class SearchView(View):

    def get(self, request, *args, **kwargs):
        if "search_word" in request.GET:
            print(request)
            if request.GET["search_word"] != "":
                start_date = request.GET["start_date"]
                end_date = request.GET["end_date"]
                # if request.GET["search_limit"] == "":
                #     search_limit = 100
                # else:
                #     search_limit = request.GET["search_limit"]
                start_time  = time.time()

                word = request.GET["search_word"]

                #検索結果を表示
                # tweets_list    = scraping.search_google(word, start_date, end_date, search_limit)
                tweets_list    = scraping.search_google(word, start_date, end_date)

                #テンプレートで扱いやすいように整形
                data        = []
                tweets_list_length    = len(tweets_list)

                #ここで特定URL、タイトルのサイトを除外する。
                for i in range(tweets_list_length):
                    allow_flag = True

                    for deny in DENY_URL_LIST:
                        if deny in tweets_list[i]:
                            allow_flag   = False
                            break
                        
                    if allow_flag:
                        for deny in DENY_TITLE_LIST:
                            if deny in tweets_list[i]:
                                allow_flag   = False
                                break

                    if allow_flag:
                        # data.append( { "url":link_list[i] , "title":title_list[i] } )
                        data = tweets_list

    
                end_time    = int(time.time() - start_time)

                context = { "search_word"   : word,
                            "start_date"   : start_date,
                            "end_date"   : end_date,
                            # "search_limit"   : search_limit,
                            "data"          : data,
                            "time"          : end_time
                            }
        
                tweets_df2 = pd.DataFrame(tweets_list, columns=['日付', 'アカウント名', 'Twitter Id', 'Text', 'TweetURL' ])
                # 先頭から余計な記号(#,@)を削除
                tweets_df2.to_csv('./csv/result.csv',index=False)
                # print(os.getcwd())
                return render(request,"search/results.html",context)

        return render(request,"search/base.html")

    def post(self, request, *args, **kwargs):

        pass

index   = SearchView.as_view()

