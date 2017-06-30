#!/usr/bin/python
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
import json
import hashlib
import sys

Encoding='gzip, deflate'
loginCookie=''
phpsessid=''
uid='24311802'

def DoLogin():
    global loginCookie
    global phpsessid
    global uid
    
    url = 'https://passport.2345.com/clientapi/login.php'
    #password md5
    data='captcha_code=&password=11111111111111111111111111111111111&username=111111111111111111111'

    cookie = cookielib.CookieJar()
    handler=urllib2.HTTPCookieProcessor(cookie)


    req = urllib2.Request(url)
    req.add_header('Host', 'passport.2345.com')
    req.add_header('Accept', '*/*')
    req.add_header('Accept-Encoding', 'xzip, default')
    req.add_header('Content-Length', len(data))
    req.add_header('Content-Type','application/x-www-form-urlencoded')
    req.add_header('Accept-Language', 'zh-Hans;q=1, en-US;q=0.9')
    req.add_header('Cookie', 'name_ie=%2526263%2524433%2520043%2540060; uid='+uid)
    req.add_header('Connection', 'keep-alive')
    req.add_header('User-Agent', 'union/1.0 (iPhone; iOS 9.3.2; Scale/2.00)')
    req.add_data(data)

    opener = urllib2.build_opener(handler)

    response = opener.open(req).read()
    #print cookie


    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value
        if item.name == 'uid':
            uid = item.value
        elif item.name == 'PHPSESSID':
            phpsessid = item.value
    s = json.loads(response)
    loginCookie =  s['data']['I']

def AppIOSv3():
    global loginCookie
    global phpsessid
    global uid
    global Encoding
    #url = 'http://jifen.2345.com/appiosv2/sign/index'
    url = 'http://jifen.2345.com/appv3/index/index?channel=1&ioschannel=appstore&iosversion=2.0'
    cookiestr = 'I='+ loginCookie +'; os=iosnew; requestFromApp=1; appversionuid=300' #+uid + ';PHPSESSID=' + phpsessid

    print cookiestr
    
    cookie = cookielib.CookieJar()
    handler=urllib2.HTTPCookieProcessor(cookie)


    req = urllib2.Request(url)
    req.add_header('Host', 'jifen.2345.com')
    req.add_header('Accept', '*/*')
    req.add_header('Accept-Encoding', Encoding)    
    req.add_header('Cookie',cookiestr)
    req.add_header('token', '660ce50559c21986422a8e36a334e671')
    req.add_header('Connection', 'keep-alive')
    req.add_header('User-Agent', 'unionPersonal/2.0 (iPhone; iOS 9.3.3; Scale/2.00)')    

    opener = urllib2.build_opener(handler)
    
    response = opener.open(req).read()
    #print response

def doSign(host, req):
    global loginCookie
    global phpsessid
    global uid
    global Encoding
    url = 'http://'+host+'/jifen/every_day_signature_new.php'
    
    
    cookiestr = 'I='+ loginCookie +'; PHPSESSID=' + phpsessid +'; appversion=300; os=iosnew; path=/; requestFromApp=1; uid='+uid+'; name_ie=%2526263%2524433%2520043%2540060; uid='+uid
    POST_data = "?sign_token="
    if host == 'jifen.2345.com' or host == 'shouji.2345.com':
         currtime = time.time()
         midnight = currtime - (currtime % 86400) + time.timezone # 当天零点的时间
         code = str(int(midnight)) + uid[::-1] # uid 反转
         """
code 算法：
当天零点的时间 + uid字符串反转
"""
         m2 = hashlib.md5()
         m2.update(uid+ code)
         POST_data += m2.hexdigest()
    
    POST_data += "&channel=1"    

    req = urllib2.Request(url+POST_data)    
    req.add_header('Host', host)    
    req.add_header('Accept-Language', 'zh-cn')
    req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G34')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    req.add_header('Accept', '*/*')
    req.add_header('Referer', 'http://'+host+'/appv3/sign/index')
    req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Cookie', cookiestr)
    req.add_header('Origin', 'http://'+ host)
    #req.add_header('Content-Length', len(POST_data))
    req.add_header('Accept-Encoding', Encoding)
    
    #req.add_data(POST_data)
    
    print 'doSignature'
    response = urllib2.urlopen(req);

    print response.read()
    
def doSignV3(host):
    global loginCookie
    global phpsessid
    global uid
    global Encoding

    url = 'http://'+ host +'/appv3/sign/index'

    cookiestr = 'I='+ loginCookie +';os=iosnew;requestFromApp=1;appversion=300;uid='+ uid +';path=/;PHPSESSID=;'+phpsessid
    
    req = urllib2.Request(url)

    req.add_header('Host', host)
    req.add_header('Accept-Encoding', Encoding)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Cookie', cookiestr)
    req.add_header('token', '660ce50559c21986422a8e36a334e671')
    req.add_header('Accept-Language', 'zh-cn')
    req.add_header('Connection', 'keep-alive')
    req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G34')

    print 'doSignV3'
    response = urllib2.urlopen(req);
    #print response.read()

    doSign(host, req)

    
def CheckAPPVersion():
    global Encoding
    url = 'http://jifen.2345.com/appv3/api/bankaddress?v=20160215'
    req = urllib2.Request(url)
    
    req.add_header('Host', 'jifen.2345.com')    
    req.add_header('Connection', 'Keep-Alive')    
    req.add_header('Accept-Encoding', Encoding)    
    
    response = urllib2.urlopen(req);

    data = json.loads(response.read())
    if data['status'] == '200':
        return 1
   
    return 0 


if not CheckAPPVersion():
    print "Error version"
    sys.exit(0)
    
print 'Version is OK'
DoLogin()
AppIOSv3()

#doSignV3('shouji.2345.com')
doSignV3('jifen.2345.com')

sys.exit(0)
