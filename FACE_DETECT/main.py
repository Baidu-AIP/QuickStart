# coding=utf-8

import sys
import json
import base64


# make it work in both python2 both python3
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

# skip https auth
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'oWx5qAVA89FRPbjhbbGrKYX7'

SECRET_KEY = 'WPsbvyKP9ZDKATbZyM05sROUt2OGiskk'


FACE_DETECT = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    get token
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
    read file
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
    call remote http server
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
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

    # get access token
    token = fetch_token()

    # concat url
    url = FACE_DETECT + "?access_token=" + token

    file_content = read_file('./faces.jpg')
    response = request(url, urlencode(
    {
        'image': base64.b64encode(file_content),
        'image_type': 'BASE64',
        'face_field': 'gender,age',
        'max_face_num': 10
    }))

    data = json.loads(response)
    num = 65;

    if data["error_code"] == 0:
        face_num = data["result"]["face_num"]
        if face_num == 0:
            # could not find face
            print("no face in the picture")
        else:
            # get face list
            face_list = data["result"]["face_list"]
            for face in face_list:
                # male face
                if face["gender"]["type"] == "male":
                    gender = "男"
                # female face
                if face["gender"]["type"] == "female":
                    gender = "女"

                print("顾客" + chr(num))
                print("   性别: " + gender + " 年龄: " + str(face["age"]))
                num = num + 1

    else:
        # print error response
        print(response)


