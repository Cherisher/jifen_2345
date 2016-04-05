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
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2'
         }
    req = urllib2.Request(url, headers=send_headers)
    
    req.add_data(data)
    response = urllib2.urlopen(req).read()
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
        'Accept-Encoding': 'gzip, deflate',
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

def set2345Cookie(url_str):     
    global cookie    
    send_headers = {       
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2',
        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'DNT': '1',
        'Referer': 'http://jifen.2345.com/'}
    
    req = urllib2.Request(url_str, headers=send_headers)
    
    cookie = cookielib.CookieJar()
    handler=urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler, HttpRedirect_Handler)
    
    response = opener.open(req)
    print response.read()
    
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value

        
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
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2'
     }
    req = urllib2.Request(url, headers=send_headers)

    req.add_data(data)
    response = urllib2.urlopen(req).read()
    checkLoginResponse(response)
    
    
if __name__ == '__main__':
    forward = 'http://jifen.2345.com'
    url = "/jifenLogin.php"
    url =forward + url
    
    username = "xxxxxxx" # 用户名
    password = 'xxxxxx' # 密码
 
    if checkNeedVirCode(url, username) == True and checkTime(url) == True:
        print 'Do Login'
        doLogin(forward, url, username, password)
