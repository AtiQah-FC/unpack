import os
import sys
import fnmatch
import shutil
import stat

rootdir = "."

def removeFile(filename):
	os.chmod(filename, stat.S_IWUSR)
	os.remove(filename)
	print("remove "+filename)
	
def formatPath(folder, filename):
	path = os.path.join(folder, filename)
	path= path.replace('\\', '/');
	return path
	
def formatDestPath(path):
	path= path.replace('\\', '/');
	oldSize= len(path)
	path= path.replace('/CD1', '');
	path= path.replace('/CD2', '');
	path= path.replace('/CD3', '');
	pathChanged= False
	if (oldSize != len(path)):
		pathChanged= True
	return path, pathChanged

def checkFile(filename):
	if fnmatch.fnmatch(filename, '*part1.rar') or fnmatch.fnmatch(filename, '*part01.rar'):
		return "RarFirst"
	elif fnmatch.fnmatch(filename, '*part[0123456789].rar') or fnmatch.fnmatch(filename, '*part[0123456789][0123456789].rar'):
		return "RarOther"
	elif fnmatch.fnmatch(filename, '*.rar'):
		return "RarFirst"
	elif fnmatch.fnmatch(filename, '*.r[0123456789][0123456789]'):
		return "RarOther"
	elif fnmatch.fnmatch(filename, '*.sfv') or fnmatch.fnmatch(filename, '*Sample[.-]*'):
		return "Junk"
	return ""

for folder, subs, files in os.walk(rootdir):
	
	outFolder=""
	
	if fnmatch.fnmatch(folder,"*Sample"):
		for filename in files:
			path= formatPath(folder, filename)
			print("sampledir: "+path)
			removeFile(path)
		os.rmdir(folder)
		continue
		
	if fnmatch.fnmatch(folder,"*Subs") or fnmatch.fnmatch(folder,"*Sub"):
		for filename in files:
			path= formatPath(folder, filename)
			fileType= checkFile(path)
			if fileType=="Junk":
				removeFile(path)
		continue

	delFiles= []
	pathChanged= False
	unpackErrorCode= False
	
	for filename in files:
		path= formatPath(folder, filename)
		fileType= checkFile(path)
		#print("file: "+path+" "+str(fileType))
	
		if fileType!="":
			delFiles.append(path)
		
		if fileType=="RarFirst": #we need to call the unrar only for the first file of the rar lists
			outFolder, pathChanged= formatDestPath(folder)
			unpackErrorCode= os.system('unrar -y x "'+path+'" "'+outFolder+'"')
			#print("Extracting: "+path+" to "+outFolder)

	if unpackErrorCode==0: #we only deleting something when the unrar finished correctly
		for delFile in delFiles:
			removeFile(delFile)
	
		if (pathChanged):
			os.rmdir(folder)
			#print("Removing dir: "+folder+" "+outFolder)