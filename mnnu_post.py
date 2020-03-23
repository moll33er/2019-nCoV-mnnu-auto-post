# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 11:26:39 2020

@author: Administrator
"""
import random
import string
import os,sys
from urllib.parse import quote, unquote, urlencode
from bs4 import BeautifulSoup

import urllib.request as urllib2
import http.cookiejar as cookielib
import time
from apscheduler.schedulers.blocking import BlockingScheduler
'''
----------------------------------------------------------
修改学号和密码即可
#txtUid： 学号   txtPwd： 密码
linux 系统后台执行命令
nohup python -u mnnu_post.py > out.log 2>&1 &
----------------------------------------------------------
'''
payload = {'ReSubmiteFlag':'f5f10e73-c238-4381-a9d7-6b92c7932162',
           'StuLoginMode':'1','txtUid':'*********','txtPwd':'******',
           'codeInput':'jifd'}#验证码
payloads = {}
html_t=''
########################################################

#s = requests.Session()
url = 'http://dxg.mnnu.edu.cn/SPCP/Web/'
headers ={
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
#'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#'Referer': 'http://dxg.mnnu.edu.cn/SPCP/Web/Report/Index',
#'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,en-GB;q=0.7,en;q=0.6'
        }
headers_1 ={
#'Connection': 'keep-alive',
#'Content-Length': '2848',
#'Cache-Control': 'max-age=0',
#'Origin': 'http://dxg.mnnu.edu.cn',
#'Upgrade-Insecure-Requests': '1',
#'Content-Type': 'application/x-www-form-urlencoded',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
#'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#'Referer': 'http://dxg.mnnu.edu.cn/SPCP/Web/Report/Index',
#'Accept-Encoding': 'gzip, deflate',
#'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,en-GB;q=0.7,en;q=0.6'
        }

def get_pzdata(soup):
    PZData = '['
    PZData_1 = {}
    #单选框数据组装
    radioCount = soup.find('input',{'name':'radioCount'}).get('value')
    radioCount = int(radioCount)
    for i in range(1,radioCount+1):
        PZData_1['OptionName'] = soup.find('input',
                {'name':'radio_'+str(i),'checked':'checked'}).get('data-optionname')
        PZData_1['SelectId'] = soup.find('input',
                {'name':'radio_'+str(i),'checked':'checked'}).get('value')
        PZData_1['TitleId'] = soup.find('input',
                {'name':'radio_'+str(i),'checked':'checked'}).parent.get('data-tid')
        PZData_1['OptionType'] = '0'
        if i >1:
            PZData = PZData + ","
        PZData = PZData + (str(PZData_1)).replace("\'","\"").replace(" ","")
    #多选框数据组装    
    checkboxCount = soup.find('input',{'name':'checkboxCount'}).get('value')
    checkboxCount = int(checkboxCount) 
    for i in range(1,checkboxCount+1):
        PZData_1['OptionName'] = soup.find('input',
                {'name':'checkbox_'+str(i),'checked':'checked'}).get('data-optionname')
        PZData_1['SelectId'] = soup.find('input',
                {'name':'checkbox_'+str(i),'checked':'checked'}).get('value')
        PZData_1['TitleId'] = soup.find('input',
                {'name':'checkbox_'+str(i),'checked':'checked'}).parent.get('data-tid')
        PZData_1['OptionType'] = '1'
        PZData = PZData + ","+ (str(PZData_1)).replace("\'","\"").replace(" ","")
    #填空题 text_
    if int(soup.find('input',{'name':'blackCount'}).get('value')) > 0:
        print("blackCount出现新的选项！！！！\n请更新程序！！！")
        sys.exit(0)
    PZData = PZData + "]"
    #print(PZData)
    return PZData

def html_soup(soup):
    global payloads
    #soup = BeautifulSoup(htmlhandle, 'html.parser')
    
    
    print('---请确认个人信息：（有错误去网页端修改）---\n')
    StudentId = soup.select('input#StudentId')[0].get('value')
    Name = soup.select('input#Name')[0].get('value')
    MoveTel = soup.find('input',{'name':'MoveTel'}).get('value')
                       
    Province = soup.find('select',{'name':'Province'}).select('option[selected]')[0].get('value')                   
    City = soup.find('select',{'name':'City'}).get('data-defaultvalue')                   
    County = soup.find('select',{'name':'County'}).get('data-defaultvalue')                   
    ComeWhere = soup.find('input',{'name':'ComeWhere'}).get('value')                  
    
    FaProvince = soup.find('select',{'name':'FaProvince'}).select('option[selected]')[0].get('value')
    FaCity = (soup.find('select',{'name':'FaCity'}).get('data-defaultvalue'))
    FaCounty = (soup.find('select',{'name':'FaCounty'}).get('data-defaultvalue'))
    FaComeWhere = (soup.find('input',{'name':'FaComeWhere'}).get('value'))
    
    Sex = (soup.find('input',{'name':'Sex'}).get('value'))
    IdCard = (soup.find('input',{'name':'IdCard'}).get('value'))
    SpeType = (soup.find('input',{'name':'SpeType'}).get('value'))
    CollegeNo = (soup.find('input',{'name':'CollegeNo'}).get('value'))
    
    SpeGrade = (soup.find('input',{'name':'SpeGrade'}).get('value'))
    SpecialtyName = (soup.find('input',{'name':'SpecialtyName'}).get('value'))
    ClassName = (soup.find('input',{'name':'ClassName'}).get('value'))
    
    ProvinceName = (soup.find('input',{'name':'ProvinceName'}).get('value'))
    CityName = (soup.find('input',{'name':'CityName'}).get('value'))
    CountyName = (soup.find('input',{'name':'CountyName'}).get('value'))
    FaProvinceName = (soup.find('input',{'name':'FaProvinceName'}).get('value'))
    FaCityName = (soup.find('input',{'name':'FaCityName'}).get('value'))
    FaCountyName = (soup.find('input',{'name':'FaCountyName'}).get('value'))
    
    radioCount = soup.find('input',{'name':'radioCount'}).get('value')
    checkboxCount = soup.find('input',{'name':'checkboxCount'}).get('value')
    blackCount = soup.find('input',{'name':'blackCount'}).get('value')
    ReSubmiteFlag = soup.find('input',{'name':'ReSubmiteFlag'}).get('value')
    
    col=''
    if SpeType =='B':
        col='本科'
    elif SpeType =='Z':
        col='专科'
    elif SpeType =='Y':
        col='预科'
    elif SpeType =='S':
        col='硕士'
    elif SpeType =='D':
        col='博士'
    elif SpeType =='H':
        col='专升本'
    else:
        col='错误'  
    PZData = get_pzdata(soup)    
        
    print(StudentId + ' '+
            Name + ' '+
            MoveTel + '\n'+ 
            '当前所在地址：\n'+ProvinceName  + ' '+
            CityName  + ' '+
            CountyName  + ' '+ComeWhere+ '\n'+'家庭住址：\n'+
            FaProvinceName  + ' '+
            FaCityName  + ' '+
            FaCountyName + ' '+FaComeWhere+ '\n'+Sex  + '\n'+
            IdCard  + '\n'+
            
            col  + ' '+SpeGrade  + ' '+
            SpecialtyName  + ' '+
            ClassName  + '\n'
            )
    print('默认选择：\n是否发烧咳嗽（可多选）：无以上症状\n是否确诊新型肺炎：否，身体健康\n'+
          '是否疑似感染：否，不是疑似感染者\n往返或途径湖北、浙江温州以及其它省内外疫情重点地区情况？：无以上情况'+
          '与湖北、浙江温州以及省外疫情重点地区的人员接触情况？：无以上情况\n'+
          '由漳州居住地外返回漳州情况？：无以上情况\n')
    payloads={'StudentId':StudentId,
              'Name':Name,
              'MoveTel':MoveTel,
              'Province':Province,
              'City':City,
              'County':County,
              'ComeWhere':ComeWhere,
              'FaProvince':FaProvince,
              'FaCity':FaCity,
              'FaCounty':FaCounty,
              'FaComeWhere':FaComeWhere,
              #'checkbox_1':'a6a88a53-39cf-41cf-81ea-053e3643e3c4',
              #'text_1':'',
              'Other':'',
              'GetAreaUrl':'%2FSPCP%2FWeb%2FReport%2FGetArea',
              'Sex':Sex,
              'IdCard':IdCard,
              'SpeType':SpeType,
              'CollegeNo':CollegeNo,
              'SpeGrade':SpeGrade,
              'SpecialtyName':SpecialtyName,
              'ClassName':ClassName,
              'ProvinceName':ProvinceName,
              'CityName':CityName,
              'CountyName':CountyName,
              'FaProvinceName':FaProvinceName,
              'FaCityName':FaCityName,
              'FaCountyName':FaCountyName,
              'radioCount':radioCount,
              'checkboxCount':checkboxCount,
              'blackCount':blackCount,
              
              'PZData':PZData,
              
              'ReSubmiteFlag':ReSubmiteFlag
              }
    #单选框数据组装
    radioCount = soup.find('input',{'name':'radioCount'}).get('value')
    radioCount = int(radioCount)
    for i in range(1,radioCount+1):
        payloads['radio_'+str(i)] = soup.find('input',
                {'name':'radio_'+str(i),'checked':'checked'}).get('value')
    #多选框数据组装    
    checkboxCount = soup.find('input',{'name':'checkboxCount'}).get('value')
    checkboxCount = int(checkboxCount) 
    for i in range(1,checkboxCount+1):
        payloads['checkbox_'+str(i)] = soup.find('input',
                {'name':'checkbox_'+str(i),'checked':'checked'}).get('value')
'''
print(StudentId + '\n'+
        Name + '\n'+
        MoveTel + '\n'+
                           
        Province  + '\n'+                
        City  + '\n'+            
        County  + '\n'+               
        ComeWhere  + '\n'+          
        
        FaProvince  + '\n'+
        FaCity  + '\n'+
        FaCounty  + '\n'+
        FaComeWhere  + '\n'+
        
        Sex  + '\n'+
        IdCard  + '\n'+
        SpeType  + '\n'+
        CollegeNo  + '\n'+
        
        SpeGrade  + '\n'+
        SpecialtyName  + '\n'+
        ClassName  + '\n'+
        
        ProvinceName  + '\n'+
        CityName  + '\n'+
        CountyName  + '\n'+
        FaProvinceName  + '\n'+
        FaCityName  + '\n'+
        FaCountyName  
)
'''
'''                   
print(soup.select('input#StudentId')[0].get('value'))
print(soup.select('input#Name')[0].get('value'))
print(soup.find('input',{'name':'MoveTel'}).get('value'))

print(soup.find('select',{'name':'Province'}).select('option[selected]')[0].get('value'))
print(soup.find('select',{'name':'City'}).get('data-defaultvalue'))
print(soup.find('select',{'name':'County'}).get('data-defaultvalue'))
print(soup.find('input',{'name':'ComeWhere'}).get('value'))

print(soup.find('select',{'name':'FaProvince'}).select('option[selected]')[0].get('value'))
print(soup.find('select',{'name':'FaCity'}).get('data-defaultvalue'))
print(soup.find('select',{'name':'FaCounty'}).get('data-defaultvalue'))
print(soup.find('input',{'name':'FaComeWhere'}).get('value'))

print(soup.find('input',{'name':'checkbox_1','checked':'checked'}).get('value'))

print(soup.find('input',{'name':'text_1'}).get('value'))
print(soup.find('input',{'name':'radio_1','checked':'checked'}).get('value'))
print(soup.find('input',{'name':'text_2'}).get('value'))
print(soup.find('input',{'name':'radio_2','checked':'checked'}).get('value'))
print(soup.find('input',{'name':'radio_3','checked':'checked'}).get('value'))
print(soup.find('input',{'name':'radio_4','checked':'checked'}).get('value'))
print(soup.find('input',{'name':'radio_5','checked':'checked'}).get('value'))
print(soup.find('textarea',{'name':'Other'}).text)

print(soup.find('input',{'name':'GetAreaUrl'}).get('value'))'
print(soup.find('input',{'name':'Sex'}).get('value'))
print(soup.find('input',{'name':'IdCard'}).get('value'))
print(soup.find('input',{'name':'SpeType'}).get('value'))
print(soup.find('input',{'name':'CollegeNo'}).get('value'))

print(soup.find('input',{'name':'SpeGrade'}).get('value'))
print(soup.find('input',{'name':'SpecialtyName'}).get('value'))
print(soup.find('input',{'name':'ClassName'}).get('value'))

print(soup.find('input',{'name':'ProvinceName'}).get('value'))
print(soup.find('input',{'name':'CityName'}).get('value'))
print(soup.find('input',{'name':'CountyName'}).get('value'))
print(soup.find('input',{'name':'FaProvinceName'}).get('value'))
print(soup.find('input',{'name':'FaCityName'}).get('value'))
print(soup.find('input',{'name':'FaCountyName'}).get('value'))


# 5  1  2
print(soup.find('input',{'name':'radioCount'}).get('value'))
print(soup.find('input',{'name':'checkboxCount'}).get('value'))
print(soup.find('input',{'name':'blackCount'}).get('value'))
'''

#查找提示信息
def findtext(str):
    try:
        be = str.index('layer.alert(\'')
        try:
            text_0 = str[be:].index('(\'')
            text_1 = str[be:].index('\',')
            return str[be+text_0+2:be+text_1]
        except:
            return 0
    except:
        return 0
    
def findfile(start, name):
    for files in os.listdir(start):
        if name == files:
            return 1
            #full_path = os.path.join(start, relpath, name)
            #print(os.path.normpath(os.path.abspath(full_path)))    
#获取cookie
def get_cookies(cookie,opener):
    cookie.clear()#清除原有cookie
    handler=urllib2.HTTPCookieProcessor(cookie)
    #通过handler来构建opener
    opener = urllib2.build_opener(handler)
    #此处的open方法同urllib2的urlopen方法，也可以传入request
    response = opener.open(url,urlencode(payload).encode("utf-8"))
    #登陆以获取新的cookie
    #
    r = response.read().decode("utf-8")
    #保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)
    return r,opener
  
    
#删除保存的cookie文件
def del_cookie():
    if os.path.exists("cookie.db"):
        os.remove("cookie.db")
    else:
        print("The file does not exist")
#解析需要的post数据
def post_mnnu():
    global html_t
    #设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'cookie.db'
    #获取运行目录
    path = os.getcwd()
    file_ok = findfile(path,filename)#查找cookie
#    proxy = '127.0.0.1:85'
    #proxy_handler = urllib.request.ProxyHandler({
    #    'http': proxy,
    #})
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    if file_ok == 1:
        print('检测到登陆记录')
        #载入cookie
        cookie.load(filename, ignore_discard=True, ignore_expires=True)
        r = ''
    
        
    handler=urllib2.HTTPCookieProcessor(cookie)
    #通过handler来构建opener
    opener = urllib2.build_opener(handler)
    #此处的open方法同urllib2的urlopen方法，也可以传入request
    #opener.add_handler = headers
    
    if file_ok == None:
        r , opener = get_cookies(cookie,opener)
        #response = opener.open(url,urlencode(payload).encode("utf-8"))
        #r = response.read().decode("utf-8")
        #保存cookie到文件
        #cookie.save(ignore_discard=True, ignore_expires=True)
    
    #print(r)
    #for item in cookie:
    #    print ('Name = '+item.name)
    #    print ('Value = '+item.value)
    #r = s.post(url,data=payload,headers=headers)
    #r = r.text 
    #添加头部 这里只添加了浏览器标示
    header_list = []
    for key, value in headers.items():
        header_list.append((key, value))
    opener.addheaders = header_list
    #打开提交页面
    r = opener.open('http://dxg.mnnu.edu.cn/SPCP/Web/Report/Index').read().decode("utf-8")
    soup = BeautifulSoup(r, 'html.parser')
    #查找提示元素
    load_ok = str(soup.find('script',{'type':'text/javascript'}))
    time_out = 0
    while load_ok.find("open") != -1:#open关键字为未登陆或者cookie失效
        time_out += 1
        del_cookie()#删除原有的cookie
        r , opener = get_cookies(cookie,opener)#获取新的cookie
        print("登陆失败!!!第",time_out,"次重新登陆中...")
        #重新打开提交页面
        r = opener.open('http://dxg.mnnu.edu.cn/SPCP/Web/Report/Index').read().decode("utf-8")
        soup = BeautifulSoup(r, 'html.parser')
        load_ok = str(soup.find('script',{'type':'text/javascript'}))
        
        #print(soup.find('input',{'name':'Sex'}))
        if(time_out > 15):#超时退出
            print("登陆失败，已退出！\n请检查账号密码和网络设置！！")
            sys.exit(0)
    #print("重新登陆成功！")#
        
    print('登陆成功')
    
    
    #查找提交页面必备元素，存在即为登陆成功
    if soup.find('input',{'name':'Sex'}) != None:
        #解析psot信息 payloads
        html_soup(soup)
        #print(urlencode(payloads).encode("utf-8"))
        #加载headers 
        for key, value in headers_1.items():
            header_list.append((key, value))
        opener.addheaders = header_list
        #print(opener.addheaders)
        #post   
        r = opener.open('http://dxg.mnnu.edu.cn/SPCP/Web/Report/Index',
                        urlencode(payloads).
                        encode("utf-8")).read().decode("utf-8")
       # buf = BytesIO(r)
       # f = gzip.GzipFile(fileobj=buf)
       # r = f.read().decode("utf-8")
        #r = s.post(url+'Report/Index',data=payloads,headers=headers).text
        #print(r)
        if findtext(r)==0:
            print('未知错误')
        else:
            print(findtext(r))
    elif(load_ok.find("layer.alert") != -1):
        print('当前采集日期已登记！')
        
    else:
        print(r)
        print("未知错误")

def tst():
    day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    times = time.strftime('%H:%M:%S',time.localtime(time.time()))

    print(day,times)
    #以日期命名文件
    f = open("./"+day+".txt",'a')
    post_mnnu()
    #保存网站信息以便更新
    f.write(html_t)
    f.close()
        


if __name__ == "__main__": 
    #仅执行一次 标志
    only_0 = True
    print('-------闽南师范大学学生健康情况填报自动填表系统--------------\n',
          '-------当前默认为健康状态，如有异常请手动上报---------------')
    #获取随机4位验证码 当前网址在js端检查验证码，不添加也能登陆成功
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 4))

    payload['codeInput'] = salt
    #挂后台 任务调度
    scheduler = BlockingScheduler()
    scheduler.add_job(tst, 'cron', hour=6,minute=30)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
'''    
    #挂后台
    while True:
        #获取时间
        day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        times = time.strftime('%H:%M:%S',time.localtime(time.time()))
        times_1 = time.strftime('%H:%M',time.localtime(time.time()))
        #时间到！    or 1
        if (times_1 == '01:34' )or(times_1 == '01:35' )  :
            if only_0:
                print(day,times)
                #以日期命名文件
                f = open("./"+day+".txt",'a')
                post_mnnu()
                #保存网站信息以便更新
                f.write(html_t)
                f.close()
            only_0 = False
            
            
        else:
            only_0 = True
        time.sleep(100000000)
'''        
'''    
    
    
    path = 'C:/Users/Administrator/Desktop/2020-03-22.txt'
    htmlfile = open(path, 'r',encoding='UTF-8')
    soup = BeautifulSoup(htmlfile.read(), 'html.parser')
    txt = soup.find_all('input')
    print(get_pzdata(soup))
    html_soup(soup)
    print("payloads:",urlencode(payloads).
                            encode("utf-8"))
#    for x in txt:
#        print(x.get('name'),x.get('value'),x.get('data-optionname'))

    #txt = soup.find_all('select')
   # for x in txt:
'''       
    












