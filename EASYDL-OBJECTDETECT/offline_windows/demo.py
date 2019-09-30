# coding=utf-8
import requests

with open('../test_image.jpg', 'rb') as f:
    img = f.read()

result = requests.post('http://127.0.0.1:24401/', params={'threshold': 0.1},
                                                  data=img).json()

results = result["results"]

if len(results) == 0:
    print("图片中未识别到螺丝螺母")
else:
    for obj in results:
 
        print("物体类型：" + str(obj["label"]))
        print("置信度：" + str(obj["confidence"]))
        print("物体位置坐标：")
        print("    左：" + str(obj["x1"]) +  " 上：" + str(obj["y1"]) + " 右：" + str(obj["x2"]) + " 下：" + str(obj["y2"]))
        print("")