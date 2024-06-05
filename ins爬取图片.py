import requests
import os
import numpy as np
os.environ['NO_PROXY']='scontent-xsp1-1.cdninstagram.com,scontent-tpe1-1.cdninstagram.com,scontent-sin6-2.cdninstagram.com,amazon.cn,www.lofter.com,twitter.com,pbs.twimg.com,instagram.com'
#可以request的网站环境

lists = np.loadtxt('E:/爬虫图片库/ins图片url.csv', skiprows=1, usecols=1, dtype=str, delimiter=',', unpack=False, encoding='utf-8')
#图片url的地址路径！！！
'''
https://wx2.sinaimg.cn/mw690/008AHX631y1hi13x53h7wj30b46o4kj1.jpg
'''


url = "https://wx2.sinaimg.cn/mw690/008AHX631y1hi13x53h7wj30b46o4kj1.jpg"
root="D:/"
path= root + "16." +url.split('.')[-1]
i = 0 #起始图片索引,每次需手动设置！！！

headers = {'user-agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
      'Connection': 'close'}

root = "E:/爬虫图片库/insm/"
#图片存的路径！！！

proxies = {
        'http': '127.0.0.1:7890',
        'https': '127.0.0.1:7890'
    }
#代理ip设置！！！

for url in lists:
    if(url=='None'):
        continue
    path = root+str(i)+'.jpg'
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(path):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)  # 超时设置为10秒
        except:
            for i in range(10):  # 循环去请求网站
                response = requests.get(url, headers=headers, proxies=proxies, timeout=20)
                if response.status_code == 200:
                    break
        with open(path, 'wb') as f:
            f.write(response.content)
            f.close()
            print(str(i)+"文件保存成功")
        response.close()
    else:
        print(str(i)+"文件已存在")
    i += 1