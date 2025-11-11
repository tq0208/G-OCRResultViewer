import json
import os
import requests
from PIL import Image
import cv2
import utility as utl
import numpy as np
from io import BytesIO

def download_image(image_url):
    """
    从URL下载图片
    """
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        print(f"下载图片失败: {e}")
        return None

def parse_ocr_json(json_path):
    """
    解析OCR JSON文件，提取图片URL和layout数据
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 解析JSON结构: {"output":{"pages":[{"image":"url","layout":[...]}]}}
    pages = data.get('output', {}).get('pages', [])
    
    results = []
    for page in pages:
        image_url = page.get('image', '')
        layout_items = page.get('layout', [])
        
        boxes, scores, txts = [], [], []
        
        for item in layout_items:
            bbox = item.get('bbox', [])
            content = item.get('content', '')
            score = item.get('score', 0.0)
            
            # 转换bbox格式: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]] -> [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
            if len(bbox) == 4:
                box = [tuple(point) for point in bbox]
                boxes.append(box)
                scores.append(score)
                txts.append(content)
        
        results.append({
            'image_url': image_url,
            'boxes': boxes,
            'scores': scores,
            'txts': txts
        })
    
    return results

def visualize_ocr_result(json_path, output_dir='./img_result'):
    """
    解析OCR JSON结果并生成可视化图片
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 解析JSON文件
    print(f"正在解析JSON文件: {json_path}")
    ocr_results = parse_ocr_json(json_path)
    
    if not ocr_results:
        print("未找到有效的OCR结果")
        return
    
    # 处理每一页
    for idx, result in enumerate(ocr_results):
        image_url = result['image_url']
        boxes = result['boxes']
        scores = result['scores']
        txts = result['txts']
        
        print(f"\n处理第 {idx + 1} 页...")
        print(f"图片URL: {image_url}")
        print(f"检测到 {len(boxes)} 个OCR结果")
        
        # 下载图片
        print("正在下载图片...")
        image = download_image(image_url)
        if image is None:
            print(f"跳过第 {idx + 1} 页（图片下载失败）")
            continue
        
        # 使用可视化函数绘制OCR结果
        print("正在生成可视化图片...")
        draw_img = utl.draw_ocr_box_txt(
            image,
            boxes,
            txts,
            scores,
            drop_score=0.0,
            font_path="./fonts/simfang.ttf"
        )
        
        # 生成输出文件名
        json_filename = os.path.splitext(os.path.basename(json_path))[0]
        output_filename = f"{json_filename}_page{idx + 1}_visualized.png"
        output_path = os.path.join(output_dir, output_filename)
        
        # 保存图片（使用cv2.imencode支持中文路径）
        success, encoded_img = cv2.imencode('.png', draw_img[:, :, ::-1])
        if success:
            with open(output_path, 'wb') as f:
                f.write(encoded_img.tobytes())
            print(f"可视化图片已保存: {output_path}")
        else:
            print(f"保存图片失败: {output_path}")

if __name__ == "__main__":
    # 解析ppOCR-v5-output.json并生成可视化图片
    json_path = "./output/ppOCR-v5-output.json"
    visualize_ocr_result(json_path)
