#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by BIGMAO
# Date：2016-10-16
# Time: 20:32
import urllib2,cookielib, urllib
from bs4 import BeautifulSoup
from random import Random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Chsi:
    def __init__(self):
        self.main_url = 'https://account.chsi.com.cn/passport/login'
        self.cookie   = cookielib.CookieJar()
        self.handler  = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(HttpRedirect_Handler(),self.handler)
        urllib2.install_opener(self.opener)
    def craw(self, username, password):
        self.username = username
        self.password = password
        print self.login()
    def login(self):
        request = urllib2.Request(self.main_url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
        request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Encoding','deflate, sdch, br')
        request.add_header('Accept-Language','zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4')
        request.add_header('Cache-Control','no-cache')
        request.add_header('Connection','keep-alive')
        # request.add_header('Host','account.chsi.com.cn')
        request.add_header('Pragma','no-cache')
        request.add_header('Referer','https://account.chsi.com.cn/passport/logout')
        request.add_header('Upgrade-Insecure-Requests','1')
        self.headers = request.headers
        response = self.opener.open(self.main_url)
        lt = None
        if response.code == 200:
            data = BeautifulSoup(response.read().decode('utf-8'), 'html.parser', from_encoding='utf-8')
            node = data.find('input', attrs={'name':'lt'})
            lt =  node['value']

        if lt is not None:
            form_data = {
                'username':self.username,
                'password':self.password,
                'lt':lt,
                '_eventId':'submit',
                'submit':'登  录'
            }
            content = ''
            next_url = None
            try:
                request = urllib2.Request(self.main_url)
                request.headers = self.headers
                request.add_header('Referer', self.main_url)
                request.add_data(urllib.urlencode(form_data))
                response = urllib2.urlopen(request)
                print response.code
            except urllib2.HTTPError, e:
                if e.code == 302 or e.code == 301:
                    next_url = e.headers['Location']
                else:
                    return False
            while next_url is not None:
                try:
                    request = urllib2.Request(next_url)
                    request.headers = self.headers
                    request.add_header('Referer', self.main_url)
                    content = urllib2.urlopen(request)
                    next_url = None
                except urllib2.HTTPError, e:
                    print e.headers['Location']
                    next_url = e.headers['Location']
            content = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
            _url_node = content.find('a', attrs={"title":"学信档案"})
            next_url = _url_node['href']
            while next_url is not None:
                try:
                    request = urllib2.Request(next_url)
                    request.headers = self.headers
                    content = urllib2.urlopen(request)
                    next_url = None
                except urllib2.HTTPError, e:
                    print e.headers['Location']
                    next_url = e.headers['Location']
            if content.code == 200:
                random_str = get_random_str()
                self.craw_xj(random_str)
                # self.craw_xl(random_str)

    def craw_xj(self, random):
        try:
            request = urllib2.Request('http://my.chsi.com.cn/archive/xjarchive.action?trnd=' + random)
            request.headers = self.headers
            response = urllib2.urlopen(request)
            content = response.read()
            content = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
            table = content.find('table', attrs={})
            # 取姓名
            self.data = []
            name = table.find('td').get_text()
            self.data.append({"name":name})
            # 取性别
            sex = table.find_all('tr')
            print sex


        except urllib2.HTTPError, e:
            print e.reason







def get_random_str():
    chars = '0123456789'
    str = ''
    random = Random()
    for i in range(32):
        str += chars[random.randint(0,9)]
    return str

class HttpRedirect_Handler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        pass


