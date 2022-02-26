# 批量上传蓝奏云
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random
import os
import re
import math
from dealWithLargeFile import dealWithFile 
from removeFile import removeFile 
from dealWithOtherFile import dealWithOtherFile 
from compress import dealWithCompress 

Session = requests.session()
# cookie 和phpdisk_info 填到此处即可
Cookie = {
    "phpdisk_info":"",
    "ylogin":""
}
Config = {
    "urls": {
        "upload":"http://up.woozooo.com/fileup.php", # 上传接口
        "folder":"https://up.woozooo.com/doupload.php" # 文件夹接口
    },
    "rootPath":"E:/转移/PPT(1)", # 本地目录
    "rootFolderId":"4877118",  # 目标文件纠结啊
    "request":{
        "headers":{
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Cookie":f"phpdisk_info={Cookie['phpdisk_info']};ylogin={Cookie['ylogin']}"
        }
    },
    "maxUploadSize": 100 * 1024 * 1024, # 目前最大支持100M(非会员)，会员自行更改，超过指定大小，会自动过来
    "ext":["pdf","mobi","azw3","txt","epub","pptx","ppt","docx","doc","xlsx","xls","exe","apk","zip","rar","ttf","exe"] # 自定义支持格式，非支持格式将会打包zip后上传，
}
# task 
# 1 上传文件
# 2 创建文件夹
# 5 获取文件
# 47 获取目录

uploadLog = {
    "complete":0,
    "fail":0
}
def dealWithFolder(filePath=Config["rootPath"],parentId=Config["rootFolderId"]):
    files = os.listdir(filePath)
    # print(files)
    folders = getFolderDetail()
    for file in files:
        fileName = f"{filePath}/{file}"
        if os.path.isdir(fileName):
            file = re.sub("[^\u4e00-\u9fa5\w]","",file)
            folderId = parentId
            
            if parentId == Config["rootFolderId"]:
                targetFiles = os.listdir(fileName)
                if len(targetFiles) == 0:
                    continue
                try:
                    folderId = folders[file]
                except Exception:
                    result = createFolder(parentId,file)
                    folderId = result["text"]
                # folderId = folders[file]
            dealWithFolder(fileName,folderId)
            # dealWithFolder(fileName,parentId)
        else:
            ext =  fileName.split(".")[-1].lower()
            fileSize = os.path.getsize(fileName)
            count = math.ceil(fileSize/float(1024 * 1024)/100)
            if not ext in Config["ext"] or count > 1:
                uploadLog["fail"] += 1
                continue
            uploadLog["complete"] += 1
            uploadFile(fileName,file,parentId)



def uploadFile(filePath,fileName,folderId):
    uploadHeaders = {
        "Accept": "* / *",
        "Accept - Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Origin": "https://up.woozooo.com",
        "Referer": "https://up.woozooo.com/mydisk.php?item=files&action=index",
        "User-Agent": Config["request"]["headers"]["User-Agent"],
        "Cookie": Config["request"]["headers"]["Cookie"]
    }
    curFileBlob = open(filePath, "rb")
    uploadData = MultipartEncoder(
        fields = {
            "task": "1",
            "folder_id": folderId,
            "id": "WU_FILE_0",
            "name": fileName,
            "type": "application/octet-stream",
            # "lastModifiedDate": "Thu Jun 27 2019 12:11:16 GMT 0800 (中国标准时间)",
            # "size": "185",
            "upload_file": (fileName, curFileBlob, "application/octet-stream")
        },
        boundary="-----------------------------" + str(random.randint(1e28, 1e29 - 1))
    )
    uploadHeaders["Content-Type"] = uploadData.content_type
    result = Session.post(url = Config["urls"]["upload"], data=uploadData, headers=uploadHeaders).json()
    curFileBlob.close()
    if result["zt"] == 1:
        os.remove(filePath)
        print(f"【{fileName}】上传成功")
    else:
        print(f"【{fileName}】上传失败")
        print(result)

def createFolder(targetId,folderName):
    data = {
        "task": "2",
        "parent_id": targetId,
        "folder_name": folderName,
        "folder_description": ""
    }
    headers = Config["request"]["headers"]
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    result = Session.post(url=Config["urls"]["folder"], data=data, headers=headers).json()
    print(f"创建文件夹成功【{folderName}，{result['zt']}")
    return result


def getFolderDetail():

    data = {
        "task": "47",
        "folder_id": Config["rootFolderId"]
    }
    result = Session.post(url=Config["urls"]["folder"], data=data, headers=Config["request"]["headers"]).json()
    folders = {}
    for item in result["text"]:
        folders[item["name"]] = item["fol_id"]
    return folders

def dealWithAll():
    global Session
    Session = requests.session()
    try:
        dealWithFolder()
    except Exception as Err:
        print(Err)
        dealWithAll()

if __name__ == "__main__":
    # 删除长期更新等非必要数据
    currentPath = Config["rootPath"]
    removeFile(currentPath)
    # 图片转pdf
    dealWithOtherFile(currentPath,Config["ext"])
    # 拆分大文件
    dealWithFile(currentPath)
    # 压缩pdf后再进行拆分
    
    dealWithCompress(currentPath,False)
    # 二次拆分，防止部分图片太大，导致超过100M
    dealWithFile(currentPath)
    # 开始批量处理
    dealWithAll()
    
    # 压缩上传失败的PDF
    dealWithCompress(currentPath,True)
    # 拆分
    dealWithFile(currentPath)
    # 二次处理
    dealWithAll()

    print(uploadLog)
