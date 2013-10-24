# -*- coding: utf-8 -*-
import werobot, urllib2, urllib, simplejson, socket,cookielib

robot = werobot.WeRoBot(token='zhourongyu')

@robot.location
def handler(message):
    return "I don't care~"

@robot.subscribe
def subscribe(message):
    return 'Hello My Friend!'

@robot.text
def doText(message):
	msg = message.content
	if(msg[0:3] == "sn:"):
		sn = msg[3:]
		url = "http://sn.appvv.com/tools/newSn.htm"
		#可以加入参数  [无参数，使用get，以下这种方式，使用post] 
		params = {'sn': sn, 'key': '05D0437977124766B7AF884C0EF3BA6E'}
		#可以加入请求头信息，以便识别 
		i_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0", 
		         "Content-type":"application/x-www-form-urlencoded","Accept": "text/plain"} 
		#use post,have some params post to server,if not support ,will throw exception 
		#req = urllib2.Request(url, data=urllib.urlencode(params), headers=i_headers) 
		# setup cookie handler
		cookie_jar = cookielib.LWPCookieJar()
		cookie = urllib2.HTTPCookieProcessor(cookie_jar)
		opener = urllib2.build_opener(cookie) # we are not going to use proxy now

		req = urllib2.Request(url, urllib.urlencode(params), i_headers)
        #创建request后，还可以进行其他添加,若是key重复，后者生效 
        #request.add_header('Accept','application/json') 
        #可以指定提交方式 
        #request.get_method = lambda: 'PUT' 
		try: 
			res = opener.open(req)
			html = res.read()
		except urllib2.HTTPError, e: 
			print"Error Code:", e.code 
			return '查询失败,请联系作者'
		except urllib2.URLError, e: 
			print"Error Reason:", e.reason
			return '查询失败,请联系作者'
		res = simplejson.loads(html)
		dump_str = simplejson.dumps(res, ensure_ascii=False, encoding='utf-8')
		ddata = simplejson.loads(dump_str)
		info = ddata['data']['exName']+","+ddata['data']['code']+","+ddata['data']['modelNumber']+","+ddata['data']['Activated']+","+ddata['data']['creatData']
		print info
		return info
	else:
		return '格式不对哟~ 正确格式"sn:xxxxx"'
robot.run()