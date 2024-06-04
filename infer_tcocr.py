from PIL import Image
import json
import requests
import utility as UTL
from matplotlib.ticker import MultipleLocator  
  
def load_image(file_path):  
    """加载图片并返回图像对象"""  
    return Image.open(file_path)  
 

def load_json_result(file_path):
    #加载返回结果文件
    with open(file_path,'r',encoding="utf-8") as file:
        data = json.load(file)
        return data

def ocr_system(input_img_path,
               api_address,
               service_id,
               token,
               out_img_path
    ):
    """
    predict tc-ocr system 
    """
    # Token授权
    headers = {
        "Authorization": "{}".format(token),
        "Content-Type": "application/json"
    }

    # JSON请求体
    request_body = {
        "key1": "value1",
        "key2": "value2"
    }

    # 发送GET请求
    response = requests.get(api_address, headers=headers, json=request_body)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析JSON响应
        data = response.json()
        print("API调用成功，响应数据：", json.dumps(data, indent=4))
    else:
        print("API调用失败，状态码：", response.status_code)
        print("错误信息：", response.text)

