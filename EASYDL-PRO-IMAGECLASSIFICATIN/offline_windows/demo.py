# coding=utf-8
import requests

with open('./test.jpg', 'rb') as f:
    img = f.read()

result = requests.post('http://127.0.0.1:24401/', params={'threshold': 0.1},
                                                  data=img).json()

results = result["results"]

if len(results) == 0:
    print("图片中未识别到结果")
else:
    for obj in results:
        print(obj)
