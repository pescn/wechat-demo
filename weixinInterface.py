# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import requests
import os
import urllib2
import json
from lxml import etree
import cookielib
import re
import random
import kuaidi
import fanyi
import talk_api
import face
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        
        token="Wechat Token" 
        
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        userid = fromUser[0:15]
        if msgType == 'image':
            picurl = xml.find('PicUrl').text
            datas = face.api(picurl)
            try:
                result = '图中人物性别为' + str(datas[0]) + '\n' + '年龄为' + str(datas[1])
            except:
                return self.render.reply_text(fromUser, toUser, int(time.time()),  "1")
            try:
                return self.render.reply_text(fromUser, toUser, int(time.time()), result)
            except:
                return self.render.reply_text(fromUser, toUser, int(time.time()), "2")
        elif msgType == 'voice':
            content = xml.find('Recognition').text
            try:
                if type(content).__name__ == "unicode":
                    content = content.encode('UTF-8')
                content = str(content)
                msg = talk_api.talk(content, userid)
                return self.render.reply_text(fromUser,toUser,int(time.time()), msg)
            except:
                return self.render.reply_text(fromUser,toUser,int(time.time()), content + '这货还不够聪明，换句话聊天吧')
        elif msgType == 'text':
            content = xml.find("Content").text  # 获得用户所输入的内容
            if content[0:2] == u"翻译":
                word = content[2:]                 
                if type(word).__name__ == "unicode":
                    word = word.encode('UTF-8')
                word = str(word)
                Nword = fanyi.youdao(word)
                return self.render.reply_text(fromUser,toUser,int(time.time()), Nword)
            elif content[0:2] == u'反馈':
                return self.render.reply_text(fromUser,toUser,int(time.time()), '我们已经收到您的反馈，谢谢您的支持')
				
            elif content[0:2] == u'互动':
                return self.render.reply_text(fromUser,toUser,int(time.time()), '你的留言已加入互动版块，我们将在筛选后投放到大屏上,谢谢你的参与')
            else:
                try:
                    if type(content).__name__ == "unicode":
                        content = content.encode('UTF-8')
                    content = str(content)
                    msg = talk_api.talk(content, userid)
                    return self.render.reply_text(fromUser,toUser,int(time.time()), msg)
                except:
                    return self.render.reply_text(fromUser,toUser,int(time.time()), '这货还不够聪明，换句话聊天吧')
        else:
            return self.render.reply_text(fromUser,toUser,int(time.time()),'暂不支持除文字、语言和图片以外的其他信息哦')
