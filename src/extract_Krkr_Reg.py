import re
import sys
import os
import struct
from common import *

from extract_TXT import ParseVar, searchLine, initParseVar
from extract_TXT import replaceOnceImp as replaceOnceImpTXT

def initExtra():
	endStr = ExVar.endStr
	ctrlStr = ExVar.ctrlStr
	sepStr = ExVar.sepStr
	if not endStr:
		endStr = 'np'
	if not ctrlStr:
		ctrlStr = '^[A-Za-z]'
	if not sepStr:
		sepStr = '[^\\[\\]]+'
	return endStr, ctrlStr, sepStr

# ---------------- Group: Krkr 1 -------------------
def parseImp(content, listCtrl, dealOnce):
	endStr, ctrlStr, sepStr = initExtra()
	var = ParseVar(listCtrl, dealOnce)
	initParseVar(var)
	lastCtrl = None
	for contentIndex in range(len(content)):
		if contentIndex < ExVar.startline: continue 
		var.lineData = content[contentIndex][:-1] #忽略换行
		# 每行
		var.contentIndex = contentIndex
		ctrls = searchLine(var)
		if ctrls == None or len(ctrls) > 0:
			#要求段落结束后一定有skip
			if lastCtrl and 'unfinish' in lastCtrl:
				del lastCtrl['unfinish'] 
			lastCtrl = None
			continue
		#print(var.lineData)
		#搜索
		iter = re.finditer(sepStr, var.lineData)
		for r in iter:
			text = r.group()
			if text == endStr:
				if lastCtrl and 'unfinish' in lastCtrl:
					del lastCtrl['unfinish'] 
				lastCtrl = None
				continue
			if re.search(ctrlStr, text):
				continue
			start = r.start()
			end = r.end()
			lastCtrl = {'pos':[contentIndex, start, end]}
			lastCtrl['unfinish'] = True
			if dealOnce(text, contentIndex):
				listCtrl.append(lastCtrl)

# -----------------------------------
def replaceOnceImp(content, lCtrl, lTrans):
	return replaceOnceImpTXT(content, lCtrl, lTrans)
