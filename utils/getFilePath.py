
from email import contentmanager
from fileinput import filename
from tools import getHeaders
import requests

headers = getHeaders()
Session = requests.session()
Config = {
    "rootFolderId":"4838469",
    "headers":headers,
    "urls": {
        "folder":"https://up.woozooo.com/doupload.php" # 文件夹接口
    },
    "fileName":"三体"
}
def getFolders(folderId):
    data = {
        "task": "47",
        "folder_id": str(folderId)
    }
    result = Session.post(url=Config["urls"]["folder"], data=data, headers=Config["headers"]).json()
    folders = []
    for item in result["text"]:
        folders.append({
            "name":item["name"],
            "id":item["fol_id"]
        })
    return folders
    
def getFiles(folderId,fileName):
    fileList = []
    for index in range(0,10000):
        data = {
            "task": "5",
            "folder_id": str(folderId),
            "pg":index+1
        }
        result = Session.post(url=Config["urls"]["folder"], data=data, headers=Config["headers"]).json()
        files = list(filter(lambda x:Config["fileName"] in x['name_all'],result["text"]))
        if Config["fileName"]:
            files = list(map(lambda x:{"id":x["id"],"name":x["name_all"]},files))
            fileList.extend(files)
            if len(fileList) > 0:
                break
        else:
            fileList.extend(files)
        if len(result["text"]) == 0:
            break
    return fileList
def gennerateDownloadLink(files):
    fileList = []
    for item in files:
        if isinstance(item,dict):
            data = {
                "task": "22",
                "file_id": item["id"]
            }
            result = Session.post(url=Config["urls"]["folder"], data=data, headers=Config["headers"]).json()
            fileInfo = result["info"]
            print(fileInfo)
            downloadLink = f"文件名：{item['name']},=================下载链接：{fileInfo['is_newd']}/{fileInfo['f_id']}"
            fileList.append(downloadLink)
    return fileList

def getFilePath(id,fileName=""):
    folders = getFolders(id)
    print(f"正在查找文件夹======={fileName}")
    try:
        files = getFiles(id,fileName)
    except Exception:
        print(f"{fileName}查找错误")
    for item in folders:
        prepName = f"{fileName}==={item['name']}"
        files.extend(getFilePath(item["id"],prepName))
        if Config["fileName"] and len(files) > 0:
            break
    return files
    

if __name__ == "__main__":
    files = getFilePath(Config["rootFolderId"])
    if Config["fileName"]:
        files = gennerateDownloadLink(files)
    file = open("output.txt","w",encoding="utf-8")
    content = "\n".join(files)
    print(content)
    file.write(content)
    file.close()