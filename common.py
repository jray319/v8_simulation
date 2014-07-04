import sys
import glob

def getReportAttribute(filePath, attrName, isMax=False):
  f = open(filePath,"r")
  if f==0:
    return 0

  while True:
    l = f.readline()
    if l.find(attrName) != -1:
      if isMax:
        cols = l.split(":")
        l = cols[1]
      cols = l.split("=")
      value = cols[1]
      f.close
      if '.' in value:
        return float(value)
      else:
        return int(value)
    if len(l)==0:
      break
  f.close
  return 0

def getReportHistAttribute(filePath, attrName):
  hist = {}
  hist["total"] = 0
  hist["avg"] = 0
  hist["max"] = 0

  f = open(filePath,"r")
  if f==0:
    return hist

  while True:
    l = f.readline()
    cols = l.split("=")
    if len(cols) == 2:
      key = cols[0]
      value = cols[1]
      if l.find(attrName+"_Samples") != -1:
        hist["total"] = int(value)
      elif l.find(attrName+"_Avg") != -1:
        hist["avg"] = 0
      elif l.find(attrName+"_MaxKey") != -1:
        hist["max"] = int(value)
      elif l.find(attrName+"(") != -1:
        index = key.split("(").pop().replace(")", "")
        #print index + " = " + value
        hist[index] = int(value)
    if len(l)==0:
      break
  f.close
  return hist

def getAttribute(reportPath, attrType, isMax=False):
  return getReportAttribute(reportPath, attrType, isMax)

def getHistAttribute(reportPath, attrType):
  return getReportHistAttribute(reportPath, attrType)

def writeTexHeader(file, continued=False):
  file.write("\\begin{figure}[htb]\n")
  if continued:
    file.write("\\ContinuedFloat\n")
  file.write("\\begin{center}\n")

def writeTexBody(file, figureName, tag, width=1):
  file.write("\\begin{minipage}{%f\\columnwidth}\n" % (width))
  file.write("  \\includegraphics[width=\\columnwidth]{%s}\n" % (figureName))
  if tag != "":
    file.write("  \\subcaption{%s}\n" % (tag))
  file.write("\\end{minipage}\n")

def writeTexFooter(file, caption, label):
  file.write("\\begin{minipage}{\\columnwidth}\n")
  file.write("  \\caption{\\protect %s}.  \\label{fig:%s}\n" % (caption, label))
  file.write("\\end{minipage}\n")
  file.write("\\end{center}\n")
  file.write("\\end{figure}\n")
