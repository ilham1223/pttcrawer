
# coding: utf-8

# In[1]:

import re
import urllib2
from datetime import datetime
from time import sleep
from matplotlib.pyplot import plot, show, xlabel, ylabel
from Interpolation import *
import numpy as np


# In[2]:
#取得貼文時間
def GetPostTime(htmlstr):
    Post_regex = re.compile(r'</span><span class="article-meta-value">(.{1,100})</span></div>')
    article_meta_info = Post_regex.findall(htmlstr)
    Stime = article_meta_info[3]
    date_object = datetime.strptime(Stime, '%a %b %d %H:%M:%S %Y')
    return date_object


# In[3]:
#取得貼文的網址
def GetPostURL(boardhtml):
    Post_regex = re.compile(r'<a href="(.{1,200}\.html)">')
    urls = Post_regex.findall(boardhtml)
    for i in range(len(urls)):
        urls[i] = "https://www.ptt.cc/"+urls[i]
    return urls


# In[4]:
#取得看板的網址
def GetBoardURL(BoardName, Start, End):
    head = "https://www.ptt.cc/bbs/"+BoardName+"/index"
    retlist = []
    for i in range(Start, End):
        URL = head+str(i)+".html"
        retlist.append(URL)
    return retlist


# In[5]:
#取得該網址的HTML碼
def GetHTML(URL):
    content = urllib2.urlopen(URL).read()
    return content


# In[48]:
#向前的微分
def differ(func, x, dx):
    return float(func(x+dx)-func(x))/dx


# In[9]:


def TimeAnal(BoardName, start, end):
    board_waiting_list = GetBoardURL(BoardName, start, end)
    PostTime = []
    for boardurl in board_waiting_list:
        board_html = GetHTML(boardurl)
        post_waiting_list = GetPostURL(board_html)
        print boardurl
        for posturl in post_waiting_list:
            sleep(0.1)
            post_html = GetHTML(posturl)
            try:
                TIME = GetPostTime(post_html)
                PostTime.append(TIME)
            except:
                print "GET NO TIME "+posturl

    inttime = []
    y = []
    counter = 0
    for T in PostTime:
        counter += 1
        inttime.append((T-PostTime[0]).total_seconds())
        y.append(counter)

    xy = []
    for i in range(len(PostTime)):
        xy.append([inttime[i]/60./60., y[i]])
    axy = np.array(xy)
    x_max = max(axy[:, 0])
    N = len(xy)

    A = Interpolator(axy, Linear, 10000, [0, x_max+1])
    XY = []
    factor = float(x_max/N*5)
    for i in range(int(0*factor), int(x_max*factor)):
        x1 = i/float(factor)
        y1 = A.f(x1)
        dy = differ(A.f, x1, 1/float(factor))
        XY.append([x1, y1, dy])
    aXY = np.array(XY)

    plot(aXY[:, 0], aXY[:, 2], 'o--')
    show()


def main():
    TimeAnal("C_Chat", 4650, 4670)


if __name__ == "__main__":
    main()
