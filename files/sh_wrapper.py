# -*- coding: utf-8 -*-

import sys
import os
import shutil

def process1(this_func):
	# input:
	# 0: seqno
	# 1: dir/file name
	for line in sys.stdin:
		data = line[:-1].split('\t')
		this_func(data[1])

def process2(this_func):
	# input:
	# 0: seqno
	# 1: dir/file name (from)
	# 2: dir/file name (to)
	for line in sys.stdin:
		data = line[:-1].split('\t')
		this_func(data[1], data[2])

	
def main():
	command_dict = {
		'move': shutil.move,
		'copy': shutil.copy,
		'mkdir': os.makedirs
	}

	if len(sys.argv) < 2:
		sys.stderr.write('Usage: cat list python $0 command\n')
		sys.exit(1)
	
	this_command = sys.argv[1]
	

	header = sys.stdin.readline()
	if not this_command in command_dict:
		sys.stderr.write(f'ERROR: commad ({this_command}) not registered\n')
		sys.exit(1)

	this_func = command_dict[this_command]
	
	if this_command in ('copy', 'move'):
		process2(this_func)
	else:
		process1(this_func)
	
if __name__ == '__main__':
	main()

