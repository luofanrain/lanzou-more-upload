import os
import re

from PyPDF2 import PdfFileReader, PdfFileWriter

rootPath = "C:/Users/luofanrain/Desktop/test"
def mergeFile(fileName,filePath):
  [targetFileName,files] = getFileList(fileName,filePath)
  pdfFileWriter = PdfFileWriter()
  fileManager = []
  try:
    for file in  files:
      fileBlob = open(file, 'rb')
      pdfReader = PdfFileReader(fileBlob)
      numPages = pdfReader.getNumPages()
      for page in range(0, numPages):
        curPage = pdfReader.getPage(page)
        pdfFileWriter.addPage(curPage) 
      fileManager.append(fileBlob)
      # fileBlob.close()
    pdfFileWriter.write(open(targetFileName, 'wb'))
    pdfFileWriter = None
  except Exception as Error:
    print(Error)
    return

  for index in range(0,len(files)):
    fileManager[index].close()
    os.remove(files[index])

def getFileList(fileName,filePath):
  fileData = re.split("[-]",fileName)
  index = len(fileData) - 1
  while index > 0:
    if re.search("\d+(.pdf)?",fileData[index]):
      fileData.pop()
      index -= 1
    else:
      break

  targetFileName = "-".join(fileData)
  files = []

  for file in os.listdir(filePath):
    curFileName = f"{filePath}/{file}"
    if re.search(f"^{targetFileName}-",curFileName):
      files.append(curFileName)
  targetFileName = targetFileName if re.search("\.pdf$",targetFileName) else f"{targetFileName}.pdf"
  return [targetFileName,files]
  

def dealWithFile(filePath):
  
  for file in os.listdir(filePath):
    fileName = f"{filePath}/{file}"
    if not os.path.exists(fileName):
      continue
    mergeFile(fileName,filePath)
    

if __name__ == "__main__":
  dealWithFile(rootPath)
      

    