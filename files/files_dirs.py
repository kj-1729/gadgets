# -*- coding: utf-8 -*-

import sys
import os
import datetime
import re

class list_files:
	def __init__(self, root_dir, max_depth):
		self.root_dir = root_dir	
		self.max_depth = max_depth
		if self.max_depth < 0:
			self.path_depth = 15
		else:
			self.path_depth = self.max_depth
		
		self.seqno = 0
		self.path = []
		
	def process(self):
		self.print_header()

		data = {'parent_seqno': '',
			'file_name': 'ROOT',
			'file_dir': 'DIR',
			'dir': '',
			'fullpath': self.root_dir,
			'depth': 0,
			'file_size': '',
			'fname_suffix': '',
			'last_modified': ''
		}
		self.print_data(data)
		
		data = {'parent_seqno': 0,
			'depth': 0,
			'dir': self.root_dir,
		}

		self.do_process(data)
		
	def do_process(self, data):
		if data['depth'] > self.max_depth and self.max_depth >= 0:
			sys.stderr.write('Skip: '+data['dir']+'\n')
			return
			
		file_list = os.listdir(data['dir'])
		for file_name in file_list:
			if file_name == 'Thumbs.db':
				continue
			
			data['file_name'] = file_name
			data['fullpath'] = os.path.join(data['dir'], file_name)
			data['last_modified'] = datetime.datetime.fromtimestamp(os.stat(data['fullpath']).st_mtime).strftime("%Y/%m/%d %H:%M:%S")

			self.seqno += 1

			if os.path.isfile(data['fullpath']):
				data['file_size'] = os.stat(data['fullpath']).st_size

				m = re.search('^.*\.([^\.]+)*$', file_name)
				if m is not None:
					data['fname_suffix'] = m.group(1)
				else:
					data['fname_suffix'] = ''
				data['file_dir'] = 'FILE'

				self.path.append(file_name)
				self.print_data(data)
				self.path.pop()

			elif os.path.isdir(data['fullpath']):
				data['file_size'] = ""
				data['fname_suffix'] = ""
				data['file_dir'] = 'DIR'
				self.print_data(data)

				self.path.append(file_name)
				
				next_data = {'parent_seqno': self.seqno,
					'depth': data['depth'] + 1,
					'dir': data['fullpath'],
				}
				self.do_process(next_data)
				self.path.pop()

	def print_header(self):
		print('SEQNO\tPARENT_SEQNO\tDIR/FILE\tDEPTH\tFILE_TYPE\tFILE_NAME\tDIRNAME\tFULL_PATH\tSIZE\tLAST_MODIFIED', end='')
		for idx in range(self.path_depth):
			print('\t', end='')
			print(f'PATH_{idx+1}', end='')
		print("")

	def print_data(self, data):
		print(str(self.seqno), data['parent_seqno'], data['file_dir'], data['depth'], data['fname_suffix'], data['file_name'], data['dir'], data['fullpath'], data['file_size'], data['last_modified'], sep='\t', end='')
		for loop in range(self.path_depth):
			print('\t', end='')
			if loop < len(self.path):
				print(self.path[loop], end='')
		print('')


	
def main():
	if len(sys.argv) < 2:
		sys.stderr.write('Usage: python $0 root_dir [max_depth]\n')
		sys.exit(1)
	
	root_dir = sys.argv[1]
	
	if len(sys.argv) >= 3:
		max_depth = int(sys.argv[2])
	else:
		max_depth = -1

	print(f'ROOT_DIR\t{root_dir}')
	print(f'MAX_DEPTH\t{max_depth}')
	
	hd = list_files(root_dir, max_depth)
	hd.process()

if __name__ == '__main__':
	main()
