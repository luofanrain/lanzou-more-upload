import os

rootPath = r"D:/转移/15TB电子书2022年更新"

def renameFile(filePath,name):
  files = os.listdir(filePath)
  for file in files:
    fileName = f"{filePath}/{file}"
    prepName = file if name == "" else f"{name}-{file}"
    if os.path.isdir(fileName):
      renameFile(fileName,prepName)
    else:
      targetFileName = f"{filePath}/{prepName}"
      try:
        # 防止二次运行，重复命名
        if prepName in fileName:
            continue
        os.rename(fileName,targetFileName)
      except Exception:
        pass

if __name__ == "__main__":
  renameFile(rootPath,"")