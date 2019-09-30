# coding=utf-8

import sys
import json
import base64


# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 百度云控制台获取到ak，sk以及
# EasyDL官网获取到URL

# ak
API_KEY = 'Wiz6X3riOjoy3DpQPdW8fO7l'

# sk
SECRET_KEY = 'mU1npXUNnk4IDGozEobnceewTHAkICPT'

# url
EASYDL_OBJECT_DETECT_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/luosiluomushu"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()

"""
    调用远程服务
"""
def request(url, data):
    req = Request(url, json.dumps(data))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)


if __name__ == '__main__':

    # 获取access token
    token = fetch_token()

    # 拼接url
    url = EASYDL_OBJECT_DETECT_URL + "?access_token=" + token

    filename = "test_image.jpg"

    file_content = read_file(filename)

    # 请求接口
    response = request(url, 
        {
            'image': base64.b64encode(file_content),
            'threshold': 0.6
        })

    result_json = json.loads(response)

    result = result_json["results"]
    if len(result) == 0:
        print("图片中未识别到丝螺母")
    else:
        for obj in result:
            loc = obj["location"]
            print("物体类型：" + str(obj["name"]))
            print("置信度：" + str(obj["score"]))
            print("物体位置坐标：")
            print("    左：" + str(loc["left"]) +  " 上：" + str(loc["top"]) + " 长：" + str(loc["width"]) + " 高：" + str(loc["height"]))
            print("")






