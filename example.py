
# coding: utf-8

'''
此檔案為一些關於craw.py以及minding.py的使用範例
'''

from minding import htmlmind, GetWordFreq
from craw import GetHTML, Get18HTML, GetPush
import craw as cw
from time import sleep
from datetime import datetime
import requests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter
requests.packages.urllib3.disable_warnings()


# In[4]:

# 獲取C_Chat板上某篇文章中最常出現的詞彙
def example1():
    url = "https://www.ptt.cc/bbs/C_Chat/M.1452827989.A.48C.html"
    webhtml = GetHTML(url)
    webhtml = webhtml.decode('utf8')
    data = htmlmind(webhtml, 1, 3)
    for i in range(1, 10):
        print data[-i][0], data[-i][1]


# In[8]:

# 獲取非18x版面上的關鍵字累計
def TitleAdd(BoardNamem, Start, End, Keyword):
    board_waiting_list = cw.GetBoardURL(BoardNamem, Start, End)
    data = []
    ww = Keyword
    freq = 0
    counter = 0
    for boardurl in board_waiting_list:
        tt = datetime.today()
        TIME1 = tt
        TIME2 = tt
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
            if counter > 5:
                break
        data.append([TIME1, TIME2, freq])
        return data


# 獲取內文（包含推文）的關鍵字累計
# 獲取版面上的關鍵字累計
def PushAdd(BoardName, Start, End, Keyword):
    board_waiting_list = cw.GetBoardURL(BoardName, Start, End)
    data = []
    ww = Keyword
    freq = 0
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

# 獲取18x版面上的關鍵字累計
def xTitleAdd(BoardName, Start, End, KeyWord):
    board_waiting_list = cw.GetBoardURL(BoardName, Start, End)
    data = []
    ww = KeyWord
    freq = 0
    for boardurl in board_waiting_list:
        board_html = Get18HTML(boardurl)
        post_waiting_list = cw.GetPostURL(board_html)
        print boardurl
        tt = datetime.today()
        TIME1 = tt
        TIME2 = tt
        sleep(1)
        freq += GetWordFreq(board_html, ww)
        while TIME1 == tt or TIME2 == tt:
            i = 0
            j = 1
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
        data.append([TIME1, TIME2, freq])
    return data


# In[19]:

# 獲取18x版面內文（包含推文）的關鍵字累計
def xPushAdd(BoardName, Start, End, Key):
    board_waiting_list = cw.GetBoardURL(BoardName, Start, End)
    data = []
    ww = Key
    freq = 0
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

# 繪製時間-關鍵字累積量圖
def example2():
    data = xPushAdd('Gossiping', 10440, 10450, u'黃安')
    adata = np.array(data)
    dates = matplotlib.dates.date2num(adata[:, 0])
    plt.plot_date(dates, adata[:, 1], '--.')
    plt.show()

# 計算八卦版系列文出現次數


def example3():
    key = u'被刪除'
    hour = HourLocator()
    data = xTitleAdd(u'Gossiping', 10644, 10710, key)
    adata = np.array(data)
    dates = matplotlib.dates.date2num(adata[:, 0])
    datefmt = DateFormatter('%H:%M')
    fig, ax = plt.subplots()
    ax.plot_date(dates, adata[:, 2], '.')
    ax.xaxis.set_major_locator(hour)
    ax.xaxis.set_major_formatter(datefmt)
    ax.autoscale_view()
    ax.fmt_xdata = DateFormatter('%H:%M')
    fig.autofmt_xdate()
    ax.set_xlabel(u'時間')
    ax.set_ylabel(u'累計發文數')
    plt.show()
    print data[-1][2]
# In[ ]:

# 繪製推文時間累計圖


def example4():
    html = Get18HTML("https://www.ptt.cc/bbs/Gossiping/M.1453350815.A.725.html")
    pushlist = GetPush(html)
    data = []
    counter = 0
    hour = HourLocator()
    for i in pushlist:
        counter += 1
        data.append([i.time, counter])
    adata = np.array(data)
    dates = matplotlib.dates.date2num(adata[:, 0])
    datefmt = DateFormatter('%H:%M')
    fig, ax = plt.subplots()
    ax.plot_date(dates, adata[:, 1], '.')
    ax.xaxis.set_major_locator(hour)
    ax.xaxis.set_major_formatter(datefmt)
    ax.autoscale_view()
    ax.fmt_xdata = DateFormatter('%H:%M')
    fig.autofmt_xdate()
    ax.set_xlabel(u'時間')
    ax.set_ylabel(u'累計推文數')
    plt.show()


def main():
    example4()


if __name__ == "__main__":
    main()
# In[ ]:
