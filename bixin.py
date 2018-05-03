# -*- coding: UTF-8 -*-
__author__ = 'WILL_V'

import urllib.request
import urllib.parse
import json
import os
import time
import random
from urllib.request import urlretrieve
from time import time as timec


def bixin():
    idstart = int(input('请输入开始的id号：')) - 1
    idend = int(input('请输入结束的id号：')) + 1
    i = 0
    opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    ip = str(random.randint(1, 210)) + '.' + str(random.randint(1, 210)) + '.' + str(
        random.randint(1, 210)) + '.' + str(random.randint(1, 210))
    opener.addheaders = [
        ('User-Agent',
         'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'),
        ('X-Forwarded-For', ip),
        ('Host', '118.31.40.206:8888'),
        ('Connection', 'close'),
        ('X-Requested-With', 'XMLHttpRequest'),
        ('Referer', '118.31.40.206:8888')
    ]
    urllib.request.install_opener(opener)
    for i in range(idstart, idend):
        i = i + 1
        url = geturl(i)
        if (url):
            print('[+]正在爬取id=' + str(i) + '的数据')
            if (getpic(url) != 'no data'):
                print('\t[-]正在获取图片')
                all = getpic(url)
                print('\t[-]正在下载')
                time.sleep(3)
                download(i, all)
            else:
                print("\t\033[0;33m%s\033[0m" % '[x]未获取到数据')
        if (i % 5 == 0):
            # print('爬了5套，暂停10s，防止403')
            # time.sleep(10)
            pass


def geturl(i):
    url = 'http://118.31.40.206:8888/api/moment/list?len=200&userid=' + str(i)
    return url


def getpic(url):
    response = json.loads(urllib.request.urlopen(url).read().decode())
    # print(response)
    if response['Sucess']:
        if response['Data'] != []:
            all = {}
            for item in response['Data']:
                content = item['content']
                imgs = item['imgs']
                content = content.replace('\n', '')
                content = content.replace('\t', '')
                content = content.replace('\r', '')
                content = content.replace('\\', '')
                content = content.replace('|', '')
                content = content.replace('/', '')
                content = content.replace('?', '')
                content = content.replace(':', '')
                content = content.replace('*', '')
                content = content.replace('"', '')
                content = content.replace('<', '')
                content = content.replace('>', '')
                content = content.replace('...', '')
                content = content.replace(' ', '')
                if (item['content'] == ''):
                    content = '无conten-' + str(int(timec()))
                all[content] = imgs
            return all
        else:
            # print(url+" no data")
            return "no data"
    else:
        print("\033[0;31m%s\033[0m" % (url + " FAIL"))
        return "no data"


def download(id, all):
    folder = os.getcwd() + '\\download\\' + str(id)
    print('\t\t[!]共' + str(len(all)) + '个文件夹')
    print('\t\t开始下载')
    i = 0
    if not os.path.exists(folder):
        os.makedirs(folder)
    for item in all:
        itemfolder = folder + '\\' + item
        if True:  # not os.path.exists(itemfolder):
            if not os.path.exists(itemfolder):
                os.makedirs(itemfolder)
            for img in all[item]:
                path = itemfolder + img[img.rfind('/'):]
                if os.path.exists(path):
                    continue
                i = i + 1
                if (i % 10 == 0):
                    pass
                    # time.sleep(20)
                imgpath = path.replace('/', '\\')
                try:
                    urlretrieve(img, imgpath)
                except:
                    continue
        else:
            print('\t\t' + itemfolder + '已存在，跳过')
    print('\t\t下载结束')


if __name__ == '__main__':
    bixin()
