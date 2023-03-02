# -*- coding: utf-8 -*-

import sys
import os
import io
import datetime
import re
							  
write = sys.stdout.write

class list_files:
	def __init__(self, base_dir, max_depth):
		self.base_dir = base_dir	
		self.max_depth = max_depth
		self.file_name_list = {}
		self.seqno = 0
		self.path = []
		
	def process(self):
		write('SEQNO\tPARENT_SEQNO\tDIR/FILE\tDEPTH\tEXTENTION\tFILE_NAME\tDIRNAME\tFULL_PATH\tSIZE\tLAST_MODIFIED')
		for idx in range(15):
			write("\t")
			write("PATH_"+str(idx+1))
		write("\n")

		self.do_list_files(self.base_dir, '', 0, 0)
		
	def do_list_files(self, this_dir, path, this_depth, parent_seqno):
		if this_depth > self.max_depth and self.max_depth >= 0:
			sys.stderr.write('Skip: '+this_dir+'\n')
			return
			
		file_list = os.listdir(this_dir)
		for this_file in file_list:
			if this_file == 'Thumbs.db':
				continue
				
			this_file_fullpath = this_dir + '\\' + this_file
			this_path = path + '\\' + this_file
			
			last_modified = datetime.datetime.fromtimestamp(os.stat(this_file_fullpath).st_mtime).strftime("%Y/%m/%d %H:%M:%S")

			self.seqno += 1
				

			if os.path.isfile(this_file_fullpath):
				#this_file_normed = re.sub('[\d/]+', 'X', this_file)
				#if this_file_normed not in self.file_name_list.keys():
				#	dummy = []
				#	self.file_name_list[this_file_normed] = dummy
				#self.file_name_list[this_file_normed].append([this_file_fullpath, last_modified])
				
				file_size = os.stat(this_file_fullpath).st_size

				m = re.search('^.*\.([^\.]+)*$', this_file)
				if m is not None:
					fname_suffix = m.group(1)
				else:
					fname_suffix = ''

				###### OUTPUT ######
				write(str(self.seqno)) #file_no_str)
				write('\t')
				write(str(parent_seqno))
				write('\t')
				write('FILE')
				write('\t')
				write(str(this_depth))
				write('\t')
				write(fname_suffix)
				write('\t')
				write(this_file)
				write('\t')
				write(this_dir)
				write('\t')
				write(this_file_fullpath)
				write('\t')
				write(str(file_size))
				write('\t')
				write(last_modified)
				for this_path in self.path:
					write("\t")
					write(this_path)
				write("\t")
				write(this_file)
				write('\n')

			elif os.path.isdir(this_file_fullpath):
				file_size = ""
				fname_suffix = ""

				###### OUTPUT ######
				write(str(self.seqno)) #file_no_str)
				write('\t')
				write(str(parent_seqno))
				write('\t')
				write('DIR')
				write('\t')
				write(str(this_depth))
				write('\t')
				write(fname_suffix)
				write('\t')
				write(this_file)
				write('\t')
				write(this_dir)
				write('\t')
				write(this_file_fullpath)
				write('\t')
				write(str(file_size))
				write('\t')
				write(last_modified)
				for this_path in self.path:
					write("\t")
					write(this_path)
				write("\t")
				write(this_file)
				write('\n')

				self.path.append(this_file)
				self.do_list_files(this_file_fullpath, this_path, this_depth+1, self.seqno)
				self.path.pop()
	
def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python $0 base_dir max_depth\n')
		sys.exit(1)
	
	base_dir = sys.argv[1]
	max_depth = int(sys.argv[2])
	
	hd = list_files(base_dir, max_depth)
	hd.process()

if __name__ == '__main__':
	main()


		
