from PIL import Image
import os
import cv2
import json
import requests
import utility as utl
from matplotlib.ticker import MultipleLocator  
  
def is_image_file(filename):
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def get_image_path(dir,file_names):  
    image_paths = []
    if not file_names:
        for root, dirs, files in os.walk(dir):
            for file in files:
                if is_image_file(file):
                    img_path = os.path.join(root, file)
                    image_paths.append(img_path)
    else:
        for file_name in file_names:
            file_path = dir + file_name
            if is_image_file(file_path):
                image_paths.append(file_path)
    return image_paths  
 

def load_json(file_path):
    #加载返回结果文件
    with open(file_path,'r',encoding="utf-8") as file:
        data = json.load(file)
        return data

def ocr_system(input_img_path,
               api_address,
               token,
               out_img_path=None
    ):
    """
    predict tc-ocr system 
    """
    # 拼接Headers：Token授权等
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    # 拼接JSON请求体
    request_data = {} #请求体  
    
    data_arr = [] 
    img_base64 = utl.image_to_base64(input_img_path)
    data_arr.append(img_base64)
    
    request_data = {"image" : img_base64,"options": {
    "use_rotate": "false"
  }}
    request_body = json.dumps(request_data)     # 将 request_data 转换为 JSON 字符串
    
    #api_address = url + "?serviceId="+service_id

    # 设置超时时间（单位：秒）
    timeout = 10
    # 发送请求
    response = requests.post(api_address, headers=headers, json=request_data, timeout=timeout)

    if response.status_code == 200:    # 检查响应状态码
        content = response.json()
        print("API调用成功，响应数据：", json.dumps(content, indent=4))
    else:
        print("API调用失败，状态码：", response.status_code)
        print("错误信息：", response.text)
        return

    #3、解析JSON中的box和文本
    if('data' in content):
        data_list = content.get('data', [])
        text_list = data_list
    if('text' in data_list):
        text_list = data_list.get('text')
    if( not text_list):
        print("API调用失败，错误信息：", response.text)
        return
    boxes ,scores ,txts = [],[],[]

    for item in text_list:
        box = item.get('box')
        box = [tuple(iBox) for iBox in box]
        boxes.append(box)  
        confidence = item.get('confidence')
        scores.append(confidence)
        words = item.get('words')
        txts.append(words)
        #print(f"Box: {box}, Confidence: {confidence}, Words: {words}")

    image = Image.open(input_img_path)
    draw_img = utl.draw_ocr_box_txt(image,boxes,txts,scores)

    if(not out_img_path):
        out_img_path = './img_result/image_infer.png'
    bsucess = cv2.imwrite(out_img_path, draw_img[:, :, ::-1])

    return out_img_path

#从json中获取接口API和Token
def get_address_and_token(parsed_json):
    data = {}
    if "api" in parsed_json:
        api_url = parsed_json['api']
    if "serviceId" in parsed_json:
        service_ids = parsed_json['serviceId']
    if "token" in parsed_json:
        tokens = parsed_json['token']

    zip_result = zip(service_ids, tokens)
    for ser_id, token in zip_result:
        data[api_url + f"?serviceId={ser_id}"] = token
      
    return data

