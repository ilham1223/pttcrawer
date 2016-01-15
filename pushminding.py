
# coding: utf-8

# In[1]:

from minding import htmlmind, GetWordFreq
from craw import GetHTML, Get18HTML
import craw as cw
import re
from time import sleep
from datetime import datetime
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
requests.packages.urllib3.disable_warnings()
get_ipython().magic(u'matplotlib inline')


# In[4]:

#獲取C_Chat板上某篇文章中最常出現的詞彙
def example1():
    url = "https://www.ptt.cc/bbs/C_Chat/M.1452827989.A.48C.html"
    webhtml = GetHTML(url)
    webhtml = webhtml.decode('utf8')
    data = htmlmind(webhtml, 1, 3)
    for i in range(1, 10):
        print data[-i][0], data[-i][1]


# In[8]:

#獲取非18x版面上的關鍵字累計
def TitleAdd(BoardNamem, Start, End, Keyword):
    board_waiting_list = cw.GetBoardURL(BoardNamem, Start, End)
    data = []
    ww = Keyword
    freq = 0
    tt = datetime.today()
    TIME1 = tt
    TIME2 = tt
    counter = 0
    for boardurl in board_waiting_list:
        board_html = GetHTML(boardurl)
        post_waiting_list = cw.GetPostURL(board_html)
        print boardurl
        freq += GetWordFreq(board_html, ww)
        while TIME1 == tt or TIME2 == tt:
            i = 0
            j = 1
            counter += 1
            try:
                TIME1 = cw.GetPostTime(GetHTML(post_waiting_list[i]))
            except:
                print "GET NO TIME1", post_waiting_list[i]
                i += 1
            try:
                TIME2 = cw.GetPostTime(GetHTML(post_waiting_list[-j]))
            except:
                print "GET NO TIME2", post_waiting_list[-j]
                j += 1
            if counter>5:
                break
        data.append([TIME1, TIME2, freq])
        return data


# In[7]:

#獲取內文（包含推文）的關鍵字累計
#獲取版面上的關鍵字累計
def PushAdd(BoardName, Start, End, Keyword):
    board_waiting_list = cw.GetBoardURL(BoardName, Start, End)
    data = []
    ww = Keyword
    freq = 0
    counter = 0
    for boardurl in board_waiting_list:
        board_html = GetHTML(boardurl)
        post_waiting_list = cw.GetPostURL(board_html)
        print board_html
        for posturl in post_waiting_list:
            sleep(0.5)
            posthtml = GetHTML(posturl)
            TIME = cw.GetPostTime(posthtml)
            freq += GetWordFreq(posthtml, ww)
            data.append([TIME, freq, posturl])
    return data


# In[12]:

#獲取18x版面上的關鍵字累計
def xTitleAdd(BoardName, Start, End, KeyWord):
    board_waiting_list = cw.GetBoardURL(BoardName, Start, End)
    data = []
    ww = KeyWord
    freq = 0
    tt = datetime.today()
    TIME1 = tt
    TIME2 = tt
    counter = 0
    for boardurl in board_waiting_list:
        board_html = Get18HTML(boardurl)
        post_waiting_list = cw.GetPostURL(board_html)
        print boardurl
        freq += GetWordFreq(board_html, ww)
        while TIME1 == tt or TIME2 == tt:
            i = 0
            j = 1
            counter += 1
            try:
                TIME1 = cw.GetPostTime(Get18HTML(post_waiting_list[i]))
            except:
                print "GET NO TIME1", post_waiting_list[i]
                i += 1
            try:
                TIME2 = cw.GetPostTime(Get18HTML(post_waiting_list[-j]))
            except:
                print "GET NO TIME2", post_waiting_list[-j]
                j += 1
            if counter>5:
                break
        data.append([TIME1, TIME2, freq])
        return data


# In[19]:

#獲取18x版面內文（包含推文）的關鍵字累計
def xPushAdd(BoardName, Start, End, Key):
    board_waiting_list = cw.GetBoardURL(BoardName, Start, End)
    data = []
    ww = Key
    freq = 0
    counter = 0
    for boardurl in board_waiting_list:
        board_html = Get18HTML(boardurl)
        post_waiting_list = cw.GetPostURL(board_html)
        print boardurl
        for posturl in post_waiting_list:
            sleep(0.5)
            posthtml = Get18HTML(posturl)
            try:
                TIME = cw.GetPostTime(posthtml)
                freq += GetWordFreq(posthtml, ww)
                data.append([TIME, freq, posturl])
            except:
                print "GET NO TIME ", posturl
                print posthtml
    return data


# In[26]:

#繪製時間-關鍵字累積量圖
def example2():
    data = xPushAdd('Gossiping', 10440, 10460, u'黃安')
    adata = np.array(data)
    dates = matplotlib.dates.date2num(adata[:, 0])
    plt.plot_date(dates, adata[:, 1])


# In[ ]:

example2()


# In[ ]:



