
# coding: utf-8

# In[1]:

import re
import urllib2
from datetime import datetime
from time import sleep
from matplotlib.pyplot import plot, show, xlabel, ylabel, legend
from Interpolation import *
import numpy as np
import requests
requests.packages.urllib3.disable_warnings()
# In[2]:
#取得貼文時間
def GetPostTime(htmlstr):
    Post_regex = re.compile(r'</span><span class="article-meta-value">(.{1,100})</span></div>')
    article_meta_info = Post_regex.findall(htmlstr)
    Stime = article_meta_info[3]
    date_object = datetime.strptime(Stime, '%a %b %d %H:%M:%S %Y')
    return date_object


def GetPostInfo(htmlstr):
    Post_regex = re.compile(r'</span><span class="article-meta-value">(.{1,100})</span></div>')
    article_meta_info = Post_regex.findall(htmlstr)
    Stime = article_meta_info[3]
    date_object = datetime.strptime(Stime, '%a %b %d %H:%M:%S %Y')
    info = article_meta_info
    info[-1] = date_object
    return info


class Post:
    def __init__(self, htmlstr):
        Post_regex = re.compile(r'</span><span class="article-meta-value">(.{1,100})</span></div>')
        article_meta_info = Post_regex.findall(htmlstr)
        Stime = article_meta_info[3]
        date_object = datetime.strptime(Stime, '%a %b %d %H:%M:%S %Y')
        info = article_meta_info
        info[-1] = date_object
        self.info = info
        self.content = htmlstr
        self.pushlist = GetPush(htmlstr)


class pushinfo:
    def __init__(self, olist, year):
        self.status = olist[0]
        self.name = olist[1]
        self.content = olist[2]
        self.time = datetime.strptime(olist[3]+year, '%m/%d %H:%M%Y')
        self.point = self.p(olist[0])

    def p(self, x):
        return {
            u'推':1,
            u'噓':-1,
            u'→':0,
        }[x]

#此處編碼待修正
    def __repr__(self):
        return self.status+" "+self.name+" "+self.content+" "+str(self.time)

    def __str__(self):
        return "%s %s %s %s"%(self.status, self.name,
                              self.content, self.time)

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


def Get18HTML(URL):
    payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
    res = rs.get(URL, verify=False)
    return res.text

# In[48]:
#向前的微分
def differ(func, x, dx):
    return float(func(x+dx)-func(x))/dx


# In[9]:

def GetPush(webhtml):
    pushre = re.compile(u'push-tag">(.+) </span>.+push-userid">(.+)</span>.+push-content">: (.+)</span>.+"push-ipdatetime"> (.+)')
    mylist = re.findall(pushre, webhtml)
    postdate = GetPostTime(webhtml)
    year = str(postdate.year)
    pushlist = []
    for i in mylist:
        push = pushinfo(i, year)
        pushlist.append(push)
    return pushlist

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

    plot(aXY[:, 0], aXY[:, 2]*16, 'o--', label=u'增加速率')
    plot(aXY[:, 0], aXY[:, 1], '*--', label=u'文章量')
    legend()
    show()



def main():
#    TimeAnal("C_Chat", 4630, 4670)
    html = GetHTML("https://www.ptt.cc/bbs/C_Chat/M.1452691553.A.187.html")
    GetPush(html)


if __name__ == "__main__":
    main()
