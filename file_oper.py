import os

def getFiles(path):
	g_fileList = []
	if os.path.exists(path):
		files = os.listdir(path)
		for f in files :
			subpath=os.path.join(path,f)
			if os.path.isfile(subpath):
				g_fileList.append(subpath)
			else:
				sub_file = getFiles(subpath)
				g_fileList.extend(sub_file)
	return g_fileList
def filterExname (fileList, arrExtnames):
	filterList = []
	for strFile in fileList:
		strLowFileName = strFile.lower() # 转小写先
		for strExtName in arrExtnames :
			if strLowFileName.endswith(strExtName) :
				filterList.append(strFile)
	return filterList

def get_extension_file(dir, arrExtName):
    All_files = getFiles(dir)
    ret_file = filterExname(All_files,arrExtName)
    return ret_file