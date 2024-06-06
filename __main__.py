import os
import infer_tcocr
from PIL import Image
import logging

def gen_out_img_path(out_dir,file_path,service_id):
     # 获取原始文件扩展名
    extension = os.path.splitext(file_path)[1]
    filename = os.path.basename(file_path)
    filename = filename.split('.')[0]
    #将service_id插入扩展名前，得到新的输出图片名称
    new_file_name = f"{out_dir}/{filename}({service_id}){extension}"
    
    # 打印新的文件名
    print(new_file_name)
    return new_file_name

def main():  
    "通过配置文件，读取系统服务，与Tocken信息；识别的图片文件，输出识别结果等信息"
    parsed_json = infer_tcocr.load_json('./config/main.json')
    imageDir =  parsed_json['imageDir']
    image_names = parsed_json['images'] 
    outImgDir = parsed_json['outImgDir']

    api_addrs = infer_tcocr.get_address_and_token(parsed_json)  #获得所有的服务和token

    image_paths = infer_tcocr.get_image_path(imageDir,image_names) #获取所有待识别的img

    logger = logging.getLogger(f'{outImgDir}/ocr_debug.log')

    for api_address,token in api_addrs.items():
        for img_file in image_paths:
            service_id = api_address.split('=')[1]
            out_img_file = gen_out_img_path(outImgDir,img_file,service_id)
            out_image = infer_tcocr.ocr_system(img_file,api_address,token,out_img_file)
            if(out_image!=None and os.path.exists(out_image)):
                image_result = Image.open(out_image)
                #image_result.show()
            else:
                logger.error(f"serviceid = {service_id}    img = {img_file}  result_img not generate!")


if __name__ == "__main__":  
    main()

##