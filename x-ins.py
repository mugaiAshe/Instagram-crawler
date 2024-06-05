import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import urllib
import re
import numpy as np

driver = webdriver.Edge()

def Save_Data():

    csv_path = 'E:/爬虫图片库/dqins图片url.csv'
    #存url的地址路径，需自创csv文件！！！

    Data_List = []

    #word_path = "E:/爬虫图片库/dqgjc.csv"
    lists = ['pistol', 'rifle', 'defenseknives', 'shotshow', 'shotgun',
             'tanto', 'clippoint', 'war', 'bowie', 'dagger', 'blade', 'nessmuk', 'scurve', 'spanto',
             'spearpoint', 'talon', 'wharncliffe', 'kukri', 'straightbacks', 'ak',
              '刀','Switchblade']
    #lists = np.loadtxt(word_path, skiprows=1, usecols=1, dtype=str, delimiter=',', unpack=False, encoding='ansi')

    url = 'https://www.instagram.com/'
    driver.get(url)
    time.sleep(6)
    zhangh = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    zhangh.send_keys("")# 键入用户名！！！
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys("")# 键入密码！！！
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
    time.sleep(80)

    index = 0  # 关键词下标！！！
    while (index < len(lists)):
        word = lists[index]
        print(word)

        if (index % 2 == 0):
            Data_List_New = []
            for data in Data_List:
                if data not in Data_List_New:
                    Data_List_New.append(data)

            print('共爬取了 {} 条数据。'.format(len(Data_List_New)))
            df_Sheet = pd.DataFrame(Data_List_New, columns=['img_url', 'user', 'url_to', 'time'])
            print('Get data successfully!!!')

            df = pd.read_csv(csv_path, encoding='utf8', usecols=['img_url', 'user', 'url_to', 'time'])
            file = [df, df_Sheet]
            new_df = pd.concat(file, axis=0)
            final_df = new_df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=True)
            final_df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)

            final_df.to_csv(csv_path)

        index += 1
        if (word == ''):
            print('word empty!')
            continue
        word = urllib.parse.quote(word)
        word_url = 'https://www.instagram.com/explore/tags/' + word + '/'
        driver.get(word_url)

        try:
            page = 0
            for y in range(300):  # 设置爬取量！！！
                time.sleep(5)
                js = 'window.scrollBy(0,1000)'
                driver.execute_script(js)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')

                emptydiv = soup.find_all('span', {
                    "class": "x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x133cpev x1s688f x5n08af x2b8uid x4zkp8e x41vudc x10wh9bi x1wdrske x8viiok x18hxmgj"})
                if (emptydiv != []):
                    print('tag empty!')
                    break

                # pbemptydiv = soup.find_all('p', {
                #     "class": "_aao2"})
                # if (pbemptydiv != []):
                #     print('tag pbempty!')
                #     break
                #
                # noneemptydiv = soup.find_all('div', {
                #     "class": "_aady _aaq6"})
                # if (noneemptydiv != []):
                #     print('tag none empty!')
                #     break

                divimg = soup.find_all('img', {'class': 'x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3'})
                if (divimg == []):
                    print('divimg none')
                    continue

                for div in divimg:
                    if (div == None):
                        print('single div none')
                        break

                    alt = div.get('alt')
                    if (alt == None):
                        print('anonymous!')
                        continue

                    data = []
                    imgurl = div.get('src')
                    if (imgurl == None):
                        print('imgurl none!')
                        continue
                    print(str(imgurl))
                    data.append(str(imgurl))

                    ustr = re.findall(r'by .+? on', alt)
                    if (ustr == []):
                        print('ustr empty, no time!')
                        continue
                    usr = ustr[0].replace('by ', '')
                    usr = usr.replace(' on', '')
                    print(usr)
                    data.append(usr)

                    a = div.find_parent('a')
                    if (a == None):
                        print('a wrong!')
                        continue
                    urlto = a.get('href')
                    if (urlto == None):
                        print('url_to wrong!')
                        continue
                    totalurl = 'https://www.instagram.com' + urlto
                    print(totalurl)
                    data.append(totalurl)

                    tstr = re.findall(r'\w+? \d{2}, \d{4}', alt)
                    if (tstr == []):
                        print('tstr empty!')
                        continue
                    tim = tstr[0].replace(' on ', '')

                    datein = tim
                    datein = datein.replace(',', '')
                    d = datein.split(' ')
                    date_dic = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05',
                                'June': '06', 'July': '07', 'August': '08', 'September': '09',
                                'October': '10', 'November': '11', 'December': '12'}
                    tim = d[2] + date_dic[d[0]] + d[1]
                    print(tim)
                    data.append(tim)

                    Data_List.append(data)
                page += 1
                print('Fetching data on page {}！！！'.format(page))
                time.sleep(5)

        except Exception as e:
            print(e)
            print('wrong try')
        print('第 {} 个词的URL信息已获取完毕。'.format(index))


    driver.close()

    Data_List_New = []
    for data in Data_List:
        if data not in Data_List_New:
            Data_List_New.append(data)

    print('共爬取了 {} 条数据。'.format(len(Data_List_New)))
    df_Sheet = pd.DataFrame(Data_List_New, columns=['img_url', 'user', 'url_to', 'time'])
    print('Get data successfully!!!')

    df = pd.read_csv(csv_path, encoding='utf8', usecols=['img_url', 'user', 'url_to', 'time'])
    file = [df, df_Sheet]
    new_df = pd.concat(file, axis=0)
    final_df = new_df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=True)
    final_df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)

    final_df.to_csv(csv_path)

if __name__ == '__main__':
    Save_Data()