#!/bin/env python
# -*- coding: utf8 -*-
"""
Auth: Candoit
Date: 2016-04-05
"""
import urllib
import urllib2
import cookielib
import time
import random
import hashlib


class HttpRedirect_Handler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

def checkNeedVirCode(url, username):
    data="cmd=isNeedCaptcha&showWay=ajax&username=" + username

    send_headers = {
        'Host': 'jifen.2345.com',
        'Connection': 'keep-alive',
        'Content-Length': len(data),
        'Accept': '*/*',
        'Origin': 'http://jifen.2345.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Referer': 'http://jifen.2345.com/',
        'Accept-Encoding': 'xzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2'
         }
    req = urllib2.Request(url, headers=send_headers)

    req.add_data(data)
    response = urllib2.urlopen(req).read()
    print response
    if int(response) == 0:
        print "noNeedCaptcha"
        return True
    else:
        print "NeedCaptcha"
        return False

def checkTime(url):
    currtime = int(time.time())
    data = "cmd=vdate&currtime=" + str(currtime)
    send_headers = {
        'Host': 'jifen.2345.com',
        'Connection': 'keep-alive',
        'Content-Length': len(data),
        'Accept': '*/*',
        'Origin': 'http://jifen.2345.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Referer': 'http://jifen.2345.com/',
        'Accept-Encoding': 'xzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2'
     }
    req = urllib2.Request(url, headers=send_headers)

    req.add_data(data)
    response = urllib2.urlopen(req).read()
    if response == 'time_err':
        print 'time error'
        return False
    else:
        print 'time success'
        return True


def doSignature(opener):
    url = 'http://jifen.2345.com/jifen/every_day_signature_new.php'
    data = "sign_token="

    currtime = time.time()
    midnight = currtime - (currtime % 86400) + time.timezone # 当天零点的时间
    code = str(int(midnight)) + uid[::-1] # uid 反转

    """
    code 算法：
    当天零点的时间 + uid字符串反转
    """
    m2 = hashlib.md5()
    m2.update(uid+ code)
    data += m2.hexdigest()

    req = urllib2.Request(url)
    tmp = ""
    for item in cookie:
        tmp += item.name+ "=" + item.value+"; "

    print 'Cookie:',tmp
    req.add_header('Cookie', tmp)
    req.add_header('Connection', 'keep-alive')
    req.add_header('Accept-Encoding', 'xzip, deflate, sdch')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2')
    req.add_header('DNT', '1')
    req.add_header('Referer', 'http://jifen.2345.com/index.php')
    req.add_header('Origin', 'http://jifen.2345.com')
    req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    req.add_header('Accept', '*/*')
    req.add_header('Content-Length', len(data))

    req.add_data(data)
    print 'doSignature'
    response = urllib2.urlopen(req);

    print response.read()


def set2345Cookie(url_str):
    """
        HTTP/1.1 302 Found
        Date: Thu, 07 Apr 2016 02:24:54 GMT
        Server: Apache
        P3P: CP='NOI ADM DEV PSAi COM NAV OUR OTRo STP IND DEM'
        Set-Cookie: I=i%3D23741766%26u%3D24311802%26n%3D%25B0%25B5%25D3%25B0%25D6%25AE%25D3%25E3%26t%3D1459995894.51632200%26s%3D71ffe08c34ccef8afca5655a8f8b091b%26v%3D1.0%26ismobile%3D0; expires=Thu, 07-Apr-2016 04:24:54 GMT; path=/; domain=.2345.cn; httponly
        Set-Cookie: uid=24311802; expires=Thu, 07-Apr-2016 04:24:54 GMT; path=/; domain=.2345.cn
        Location: http://jifen.2345.com
        Cache-Control: max-age=0
        Expires: Thu, 07 Apr 2016 02:24:54 GMT
        Vary: Accept-Encoding
        Content-Length: 0
        Connection: close
        Content-Type: text/html; charset=gbk
    """
    send_headers = {
        'Connection': 'keep-alive',
        'Accept-Encoding': 'xzip, deflate, sdch',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2',
        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'DNT': '1',
        'Referer': 'http://jifen.2345.com/'}

    req = urllib2.Request(url_str, headers=send_headers)

    opener = urllib2.build_opener(HttpRedirect_Handler)

    response = opener.open(req)

    data = response.read()

    doSignature(opener)

def checkLoginResponse(response):
    errmsg ={1: '验证码输入错误，请重新输入',
           4:  '2345帐号不存在或密码错误!',
           7:'请输入验证码 :)',
           8:'登录有误，错误代码1004，请联系客服 :)',
           9:'登陆异常, 请稍后再试 :)',
           10:'2345帐号异常'}

    redata = response.strip("[]").split(',')[0:4]
    op = int(redata[0])
    if op == 6:
        url_str = redata[1].replace('\/', '/').strip("\"")

        if url_str.find('bbs.2345.cn/api/passport.php?action=login&cookieTime') >= 0:
            print 'setCookie'
            set2345Cookie(url_str)
        else:
            print url_str
    elif op == 2 or op == 3 or op == 5:
        url_str = redata[1].replace('\/', '/').strip("\"")
        print url_str

    else:
        print errmsg[op]

def doLogin(forward, url, username, password):
    vTime ="7776000"
    weakpass="0"
    remember = '0'
    imgCodeStr=''

    """
    ·# 验证码处理
     if(checkCookie('lnc') == 1) {
     	   imgCodeStr = "&pImgCode=" + $("#pImgCode").val() + "";
        }
    """
    global cookie
    global uid

    cookie = cookielib.CookieJar()
    handler=urllib2.HTTPCookieProcessor(cookie)

    m2 = hashlib.md5()
    m2.update(password)
    md5passwd = m2.hexdigest()

    data = "cmd=login&username=" + username + "&password=" + md5passwd + "&remember=" + remember + "&forward=" + forward + "&showWay=ajax"+imgCodeStr+"&weakpass="+weakpass+"&t=" + str(random.random())
    send_headers = {
        'Host': 'jifen.2345.com',
        'Connection': 'keep-alive',
        'Content-Length': len(data),
        'Accept': '*/*',
        'Origin': 'http://jifen.2345.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Referer': 'http://jifen.2345.com/',
        'Accept-Encoding': 'xzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2'
     }
    req = urllib2.Request(url, headers=send_headers)
    req.add_data(data)

    opener = urllib2.build_opener(handler)

    response = opener.open(req).read()


    #print cookie
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value
        if item.name == 'uid':
            uid = item.value

    print "uid:", uid

    checkLoginResponse(response)


if __name__ == '__main__':
    forward = 'http://jifen.2345.com'
    url = "/jifenLogin.php"
    url =forward + url

    username = "" # 用户名
    password = "" # 密码

    if len(username) == 0 or len(password) == 0:
        print "!!!Please input you username and password!!!"
        sys.exit(1)

    if checkNeedVirCode(url, username) == True and checkTime(url) == True:
        print 'Do Login'
        doLogin(forward, url, username, password)
    else:
        sys.exit(1)
