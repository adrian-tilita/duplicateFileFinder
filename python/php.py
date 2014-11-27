# Necessary Libs
import os
import math
import time
import hashlib

########################################################
# Content
#-------------------------------------------------------
#
# scandir( path )
# file_get_contents( file, [Int(chunk_size) = 64] )
# file_put_contents( file, content )
# microtime( [Boolean(get_as_float) = False] )
# filesize ( file )
########################################################
# Custom methods
#-------------------------------------------------------
# combineFileWithPath(path,file) - returns os.path.join
# getExtension(file)
########################################################


########################################################
# @scandir( path )
#-------------------------------------------------------
# directory - dir name
########################################################
def scandir( path ):
	try:
		files = os.listdir( path )
	except IOError as e:
		#print( e )
		return False
	else:
		return files
# END OF FUNCTION
########################################################
# @is_dir( path )
#-------------------------------------------------------
# directory - dir name
########################################################
def is_dir( path ):
	return os.path.isdir(path)
# END OF FUNCTION


########################################################
# @file_get_contents( file, chunk_size )
#-------------------------------------------------------
# file - file name
# chunk_size - optional, default 64 - chunks size
########################################################
def file_get_contents(file, chunk = 64):
	try:
		file_open = os.open(file, 'r')
	except IOError as e:
		return False
	else:
		content = ''
		while True:
			try:
				# Read in chunks to avoid problems
				temp = file_open.read(chunk)
			except UnicodeDecodeError:
				temp = ''
				pass
			else:
				# Break loop if nothing else to read
				if not temp:
					break
				content = content + temp
		# close file
		file_open.close()
		return content
# END OF FUNCTION

########################################################
# @file_put_contents( file, content )
#-------------------------------------------------------
# file - file name
# content - content to put in file
########################################################
def file_put_contents(file, content):
	try:
		file_open = open(file, 'w')
	except IOError as e:
		return False
	else:
		file_open.write(content)
		file_open.close()
		return True
# END OF FUNCTION

########################################################
# @microtime( file, content )
#-------------------------------------------------------
# get_as_float - default False
########################################################
def microtime(get_as_float = False):
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())
# END OF FUNCTION


########################################################
# @filesize( file )
#-------------------------------------------------------
# return size in bytes
########################################################
def filesize(file):
	try:
		size = os.path.getsize(file)
	except Exception:
		return 0
	else:
		return size
# END OF FUNCTION

########################################################
# @combineFileWithPath( path, file )
#-------------------------------------------------------
# returns os.path.join
########################################################
def combineFileWithPath(path, file):
	return os.path.join(path,file)
# END OF FUNCTION


########################################################
# @getExtension( file )
#-------------------------------------------------------
# returns extension
########################################################
def getExtension(file):
	file, ext = os.path.splitext( file )
	ext = ext.lower()
	return ext[1:]
# END OF FUNCTION