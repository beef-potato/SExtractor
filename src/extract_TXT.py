import re
import sys
import os
import struct
from common import *
from helper_text import generateBytes

OldEncodeName = 'cp932' #仅用于TXT模式截断
NewEncodeName = 'gbk' #仅用于TXT模式截断

class ParseVar():
	contentIndex = 0
	lineData = None
	searchStart = 0
	searchEnd = -1
	listIndex = 0 #准备弃用
	listCtrl = None
	dealOnce = None
	regList = []
	nameList = []
	OldEncodeName = None
	ignoreDecodeError = False
	postSkip = None
	checkJIS = None

	def __init__(self, listCtrl=None, dealOnce=None):
		self.listCtrl = listCtrl
		self.dealOnce = dealOnce

# -----------------------------------
def GetPos(var:ParseVar, searchData:str, r:re.Match[str], i):
	start = r.start(i)
	end = r.end(i)
	if var.OldEncodeName and ExVar.pureText:
		#bin的纯文本模式
		#从字符位置转为字节位置
		lengthPre = len(searchData[0:start].encode(var.OldEncodeName))
		lengthText = len(searchData[start:end].encode(var.OldEncodeName))
		start = lengthPre
		end = lengthPre + lengthText
	start += var.searchStart
	end += var.searchStart
	return start, end
# -----------------------------------
def searchLine(var:ParseVar):
	if var.searchStart > 0:
		searchData = var.lineData[var.searchStart:var.searchEnd]
	else:
		searchData = var.lineData
	if var.OldEncodeName and ExVar.pureText:
		#bin的纯文本模式
		searchData = searchData.decode(var.OldEncodeName)
	ctrls = []
	for regItem in var.regList:
		regType = regItem[1]
		value = regItem[0]
		if regType == 'skip':
			# 跳过
			if re.search(value, searchData): #已匹配则停止
				return None #skip则返回None
		else:
			# 搜索
			tmpDic = {}
			matched = False
			iter = re.finditer(value, searchData) 
			for r in iter:
				#print(r.groups())
				for i in range(1, len(r.groups())+1):
					if r.group(i) == None: continue
					start, end = GetPos(var, searchData, r, i)
					if var.OldEncodeName: # bin
						try:
							if var.checkJIS != None:
								ret = checkJIS(var.lineData[start:end], var.checkJIS)
								if not ret:
									continue
							text = var.lineData[start:end].decode(var.OldEncodeName)
						except Exception as ex:
							if var.ignoreDecodeError:
								continue
							else:
								raise
					else: # txt
						text = var.lineData[start:end]
					#匹配后跳过
					if var.postSkip:
						if re.search(var.postSkip, text):
							#print('postSkip', text)
							continue
					#0行数，1起始字符下标（包含），2结束字符下标（不包含）
					ctrl = {'pos':[var.contentIndex, start, end]}
					tmpDic[start] = [text, ctrl]
					#检查命名
					key = None
					for name, index in r.re.groupindex.items():
						if i == index: key = name
					if text in var.nameList: #强制检查名字
						ctrl['isName'] = True #名字标记
					elif not key:
						pass
					elif key.startswith('name'):
						ctrl['isName'] = True #名字标记
					elif key.startswith('unf'):
						ctrl['unfinish'] = True
					matched = True
			if matched :
				#按文本中顺序处理
				for key in sorted(tmpDic.keys()):
					value = tmpDic[key]
					if var.dealOnce(value[0], var.contentIndex):
						var.listCtrl.append(value[1])
						ctrls.append(value[1])
				break #已匹配则停止
	return ctrls

def GetRegList(items, OldEncodeName):
	lst = []
	for key, value in items:
		if OldEncodeName and ExVar.pureText == False:
			value = value.encode(OldEncodeName)
		if re.search('skip', key):
			lst.append([value, 'skip'])
		elif re.search('search', key):
			lst.append([value, 'search'])
	return lst

def dealLastCtrl(lastCtrl, ctrls, contentIndex=-1):
	if ctrls == None or len(ctrls) == 0 or 'isName' in ctrls[-1]: #skip匹配或name匹配或存在未匹配内容
		if lastCtrl and 'unfinish' in lastCtrl:
			del lastCtrl['unfinish'] #段落结束
		lastCtrl = None
	elif 'unfinish' in ctrls[-1]:
		lastCtrl = ctrls[-1]
	else:
		lastCtrl = None
	return lastCtrl

def initParseVar(var:ParseVar, regDic=None):
	if regDic == None:
		regDic = ExVar.regDic
	var.nameList = ExVar.nameList
	var.regList = GetRegList(regDic.items(), var.OldEncodeName)
	var.ignoreDecodeError = ExVar.ignoreDecodeError
	var.postSkip = ExVar.postSkip
	var.checkJIS = ExVar.checkJIS
	if var.checkJIS and var.OldEncodeName:
		var.checkJIS = var.checkJIS.encode(var.OldEncodeName)

# ---------------- Group: TXT -------------------
def parseImp(content, listCtrl, dealOnce):
	checkLast = ExVar.structure.startswith('para')
	var = ParseVar(listCtrl, dealOnce)
	initParseVar(var)
	lastCtrl = None
	for contentIndex in range(len(content)):
		if contentIndex < ExVar.startline: continue 
		var.lineData = content[contentIndex][:-1] #不检查末尾换行
		#print('>>> Line ' + str(contentIndex), ': ', var.lineData)
		var.contentIndex = contentIndex
		ctrls = searchLine(var)
		if checkLast:
			lastCtrl = dealLastCtrl(lastCtrl, ctrls, contentIndex)
	#文末处理
	if lastCtrl and 'unfinish' in lastCtrl:
		del lastCtrl['unfinish'] #段落结束

# -----------------------------------
def replaceOnceImp(content, lCtrl, lTrans):
	num = len(lCtrl)
	for i in range(num):
		# 位置
		ctrl = lCtrl[i]
		posData = ctrl['pos']
		contentIndex = posData[0]
		start = posData[1]
		end = posData[2]
		trans = lTrans[i]
		if ExVar.cutoff:
			origData = content[contentIndex][start:end].encode(OldEncodeName)
			transData = generateBytes(trans, len(origData), NewEncodeName)
			if transData == None:
				return False
			trans = transData.decode(NewEncodeName)
		#写入new
		strNew = content[contentIndex][:start] + trans + content[contentIndex][end:]
		#print(strNew)
		content[contentIndex] = strNew
	return True
