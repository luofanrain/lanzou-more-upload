import os
import math

from PyPDF2 import PdfFileReader, PdfFileWriter


def dealWithLargeFile(filePath):
  ext = filePath[-4:].lower()
  if  ".pdf" != ext:
    return
  fsize = os.path.getsize(filePath)
  count = math.ceil(fsize/float(1000 * 1024)/100)
  if count == 1:
    return
  count = count + 1
  fileBlob = open(filePath, 'rb')
  try:
    pdfReader = PdfFileReader(fileBlob)
    errorStatus = pdfReader.errorDeal
    numPages = pdfReader.getNumPages()
  except Exception:
    return
  pagesize = math.ceil(numPages/count)
  pdfFileWriter = None
  if not errorStatus:
    for page in range(0, numPages):
      curSection = math.floor(page/pagesize)
      if page == curSection * pagesize:
        pdfFileWriter = PdfFileWriter()
      curPage = pdfReader.getPage(page)
      pdfFileWriter.addPage(curPage)
      if page == (curSection + 1) * pagesize - 1 or page == numPages - 1:
        curFileName = filePath[:-4]
        curFileName = f"{curFileName}-{curSection + 1}.pdf"
        print(curFileName)
        try:
          pdfFileWriter.write(open(curFileName, 'wb'))
        except Exception as Err:
          print(Err)
        pdfFileWriter = None
  fileBlob.close()
  os.remove(filePath)

def dealWithFile(filePath):
  files = os.listdir(filePath)
  for file in files:
    fileName = f"{filePath}/{file}"
    if os.path.isdir(fileName):
      dealWithFile(fileName)
    else:
      print(fileName)
      dealWithLargeFile(fileName)

    