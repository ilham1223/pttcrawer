
# coding: utf-8

# In[1]:
"""
簡單的文字探勘，在文檔案中找出現次數最多的字詞
"""


import re
import numpy as np
import codecs


# In[8]:

def postminding(mystr, min_len, max_len):
    N = len(mystr)
    mydict = dict()
    for char_len in range(min_len, max_len):
        for locate in range(N):
            if char_len+locate < N:
                keyword = mystr[locate:locate+char_len+1]
                mydict[keyword] = [0, keyword]

    for char_len in range(min_len, max_len):
        for locate in range(N):
            if char_len+locate < N:
                keyword = mystr[locate:locate+char_len+1]
                mydict[keyword][0] += 1

    data = np.array(mydict.values())
    data = sorted(data, key=lambda x : x[0])
    return data

# In[9]:

def main():
    p=re.compile(r'[\w^[ :./\t\n\r\f\v推]+')

    f = codecs.open("test.dat","r","utf-8")
    mystr = f.read().strip('\n')
    mystr = re.sub(p, '', mystr)

    print mystr
    data = postminding(mystr, 1, 3)
    if data is not []:
        for i in range(1, 11):
            print data[-i][1], "\t", data[-i][0]
    f.close()


if __name__ == "__main__":
    main()
# In[ ]:



