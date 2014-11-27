import php
import md5sum
import pprint
import operator
import sys
import xml.etree.ElementTree as ET

start = php.microtime(True)

class getDuplicates:

	ext  = False	# (Array)Extensions
	path = False	# (String)Path
	files= []

	# setPath( path )
	def setPath(self, path):
		self.path = path
	# end method

	# setExt( ext )
	def setExt(self, ext):
		self.ext = []
		for item in ext:
			self.ext.append( item.lower() )
	# end method
	
	# getFiles( path )
	def getFiles(self, path = False):
		# Identifying if is the first instance of this method
		original = False
		if not path:
			original = True
			path = self.path

		items = []
		files = php.scandir(path)
		if files:
			for file in files:
				filename = php.combineFileWithPath(path,file)
				# If the current file is a directory
				if php.is_dir(filename):
					dir_files = self.getFiles(filename)
					for dir_file in dir_files:
						items.append(dir_file)
				# If the current file is actually a file
				else:
					# If we verify the extension
					if self.ext:
						# get file extension
						file_ext = php.getExtension(filename)
						is_type  = False
						for ext in self.ext:
							if file_ext == ext:
								is_type = True
								break
						if not is_type:
							continue
					items.append(filename)
		if original:
			self.files = items
			self.filterFiles()
			return
		else:
			return items
	# END OF FUNCTION

	# filerFiles()
	def filterFiles(self):
		files = {}
		group = {}
		#pprint.pprint(self.files)
		for file in self.files:
			hash = md5sum.printsum( file )
			files[file] = hash

		# Filter by Hash
		hash_count = {}
		last_hash = ''
		# Order files by hash
		sorted_files = {}
		sorted_files = sorted(files.items(), key=operator.itemgetter(1))

		# Group Duplicates
		for file in sorted_files:
			if last_hash != file[1]:
				last_hash = file[1]
				hash_count[last_hash] = 1
			else:
				hash_count[file[1]] += 1
		# Group Files
		keys = {}
		for hash in hash_count:
			if hash_count[hash] > 1:
				for file in files:
					if files[file] == hash:
						if files[file] not in group:
							keys[files[file]]  = 0
							group[files[file]] = {}
						group[files[file]][ keys[files[file]] ] = file
						keys[files[file]] += 1
		# end of group files

		self.files = group

	# Write Result To XML
	def writeXml(self, filename = 'duplicate_files.xml'):
		group_files = self.files
		# Generate The XML File
		xml_list = ET.Element('list')
		for group in group_files:
			xml_group = ET.SubElement(xml_list, "group")
			group_item = group_files[group]
			for file in group_item:
				size = {}
				size["filesize"] = str( php.filesize(group_item[file]) )
				xml_file = ET.SubElement(xml_group, "file", size)
				xml_file.text = group_item[file]
		xml_file = ET.tostring(xml_list, "utf-8", "xml")
		php.file_put_contents(filename, xml_file.decode("utf-8"))
# END OF CLASS


# Get And Set Arguments
key  = 0
path = False
ext  = False
xml  = 'duplicates.xml'

for arg in sys.argv:
	if key == 1:
		path = arg
	if key == 2:
		ext = arg.split(",")
	if key == 3:
		xml = arg
	key += 1
# end of getArgument

if path == 'help' or path == '?' or not path:
	print('==============================================================')
	print('Usage:')
	print('     main.py [path] *[ext] *[xml_filename]')
	print('* - optional')
	print('')
	print('Example: main.py C:\\ jpg,png duplicate_files.xml')
	print('==============================================================')
	exit(0)

scan = getDuplicates()
scan.setPath(path)
if ext:
	scan.setExt(ext)
scan.getFiles()
scan.writeXml(xml)

end = php.microtime(True) - start
end = "{:.2f}".format(end)
print('Finished in ' + end + ' seconds.')