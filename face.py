# -*- coding: utf-8 -*-

import httplib
import urllib
import json
import base64
import urllib2
import requests

def api(photourl):
    headers = {'Content-Type': 'application/json','Ocp-Apim-Subscription-Key': 'Microsoft Face API Key',}
    
    params = {'returnFaceId': 'true','returnFaceLandmarks': 'false','returnFaceAttributes': 'age,gender',}
    
    body = {"url":photourl,}
    try:
        r = requests.post('https://api.projectoxford.ai/face/v1.0/detect?',params = params,data = json.dumps(body),headers = headers)
        con = r.json()
        age = con[0]['faceAttributes']['age']
        age = str(age)
        sex = con[0]['faceAttributes']['gender']
        if sex == u'female':
            sex = u'女'
        else:
            sex = u'男'
        datas = [sex,age]
        return datas
    except Exception as e:
        return [u'错误',u'错误']
