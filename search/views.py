import csv
import os
from django.http import HttpResponse
from django.shortcuts import render

from django.views import generic

#クラスベースのビューを作るため
from django.views import View

#スクレイピングのコードをインポート
from . import scraping 

import time

import pandas as pd

#Viewを継承してGET文、POST文の関数を作る
class SearchView(View):
    def get(self, request, *args, **kwargs):
        if "search_word" in request.GET:
            if request.GET["search_word"] != "":
                start_date = request.GET["start_date"]
                end_date = request.GET["end_date"]
                search_limit = request.GET["search_limit"]
                start_time  = time.time()
                word = request.GET["search_word"]
                
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment;  filename="result.csv"'
                writer = csv.writer(response)
                tweetsList    = scraping.search_twitter(word, start_date, end_date, search_limit)
                for tweets in tweetsList:
                    writer.writerow(tweets)
                return response

        return render(request,"search/base.html")

    def post(self, request, *args, **kwargs):
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;  filename="result.csv"'
        writer = csv.writer(response)

        for tweets in self.__list:
            writer.writerow(tweets)

        return response

index   = SearchView.as_view()