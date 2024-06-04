#main.py
import cv2
import infer_tcocr
import argparse 
import utility as utl
import numpy as np

def main():  
#0、传入识别图片及结果集文本
# 创建一个 ArgumentParser 对象  
    parser = argparse.ArgumentParser(description='Process some integers.')  
  
    # 添加参数  
    #parser.add_argument('--image', type=str, required=True, help='input image file')  
    #parser.add_argument('--result', type=str, required=True, help='input result file') 
    #parser.add_argument('--output', type=str, required=True, help='An output file')  
  
    # 解析参数  
    #args = parser.parse_args()  

    #1、添加图片，传入解析的图片，返回图片结果 
    image_path = 'E:\工作\架构文档\\2024\产业园区业务\AI相关\AIRequest\自测结果\衬里管\衬里管-材料表1原图.png'   # 替换为你的图片路径  
    image = infer_tcocr.load_image(image_path)

    # 获取图像的尺寸（以像素为单位）  
    width, height = image.width,image.height;  
    print('Width (pixels):', width)  
    print('Height (pixels):', height) 

    #2、解析OCR识别结果，返回文字及其box所在位置列表
    json_path = 'E:\工作\架构文档\\2024\产业园区业务\AI相关\AIRequest\自测结果\衬里管\衬里管-材料表1_自建服务.json'
    content = infer_tcocr.load_json_result(json_path)

    #3、解析JSON中的box和文本
    data_list = content.get('data', [])
    boxes ,scores ,txts = [],[],[]
    for item in data_list:
        box = item.get('box')
        box = [tuple(iBox) for iBox in box]
        boxes.append(box)  
        confidence = item.get('confidence')
        scores.append(confidence)
        words = item.get('words')
        txts.append(words)
        print(f"Box: {box}, Confidence: {confidence}, Words: {words}")

    draw_img = utl.draw_ocr_box_txt(image,boxes,txts,scores)
    bsucess = cv2.imwrite('./img_result/image_infer.png', draw_img[:, :, ::-1])

if __name__ == "__main__":  
    main()

##