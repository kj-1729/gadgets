#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime
import time
import random

write = sys.stdout.write

class mecab:
	def __init__(self):
		self.mecab = "C:\\Program Files (x86)\\MeCab\\bin\\mecab.exe"
		#self.mecabrc = "-r E:\\NLP\\MeCab\\mecabrc"

		self.mecab_option = ""; #"-N2"
		
		target_form = {}
		target_form[u'助詞'] = -1
		target_form[u'助動詞'] =-1
		target_form[u'連体詞'] = -1
		target_form[u'接頭詞'] = -1
		target_form[u'記号'] =-1
		target_form[u'副詞'] =-1
		target_form[u'接続詞'] =-1
		target_form[u'名詞'] = 0
		target_form[u'固有名詞'] =0
		target_form[u'数'] =-1
		target_form[u'接尾'] =-1
		target_form[u'非自立'] =-1
		target_form[u'動詞'] = 0

		self.target_form = target_form

		now = datetime.datetime.now()
		unixtime = int(time.mktime(now.timetuple()))
		rd = int(1000000000*random.random())
		self.suffix = str(unixtime) + '_' + str(rd)
		self.tmp_fname = "mecab-tmp" + self.suffix + ".txt"

	def parse(self, sentence):
		#os.system(cmd)
		self.sentence = sentence
		
		fp = open(self.tmp_fname, 'w')
		fp.write(self.sentence)
		fp.close()
		
		#self.cmd = "echo "+self.sentence+" | \""+self.mecab+"\" "+self.mecab_option+" "+self.mecabrc+" "
		self.cmd = "type "+self.tmp_fname+" | \""+self.mecab+"\""


		pp = os.popen(self.cmd, 'r')
		parse_result = []
		for line in pp:
			#print "============================="
			#print line
			if re.match('^EOS', line):
				continue
			data = line[:-1].split('\t')
			if len(data) < 2:
				self.result = None
				return None
			result = data[1].split(',')
			result.insert(0, data[0])
			parse_result.append(result)
		self.result = parse_result

	def is_target_form(self, term, idx):
		form_u = term[idx] #unicode(term[idx], 'cp932')
		if self.target_form.has_key(form_u) == False:
			return 1
		else:
			flg = self.target_form[form_u]
			if flg == 0:
				return self.is_target_form(term, idx+1)
			else:
				return flg

	def get_result(self):
		return self.result

	def print_result(self):
		cnt = 0
		write("------- in mecab.print_result -----------")
		for res in self.result:
			write(str(cnt) + ":" + res[0] + ":")
			for res1 in res:
				write(res1+"|")
			write("\n")
			cnt += 1
		write("-----------------")

	def rm(self):
		os.remove(self.tmp_fname)
		
def main():
	if len(sys.argv) > 2:
		idx_id = int(sys.argv[1])
		idx_txt = int(sys.argv[2])
	else:
		sys.stderr.write("Usage: cat datafile | python mecab.py idx_id idx_txt > output\n")
		sys.exit(1)
		

	mecab_field_name = ['KEYWORD', 'HINSHI', 'HINSHI_1','HINSHI_2', 'HINSHI_3', 'KATSUYO_KATA', 'KATSUYO_KEI', 'GENKEI', 'YOMI', 'HATSUON']
	handler = mecab()
	header = sys.stdin.readline()
	field_name = header[:-1].split('\t')
	num_fields = len(field_name)
	for loop1 in range(num_fields):
		if loop1 > 0:
			write('\t')
		if loop1 == idx_txt:
			for loop2 in range(8):
				if loop2 > 0:
					write('\t')
				write(mecab_field_name[loop2])
		else:
			write(field_name[loop1]) #.encode('cp932'))
	write('\n')
		
	#idx_txt = 17
	loop=0
	prev_id = '-1'
	for line in sys.stdin:
		data = line[:-1].split('\t')
		#num_fields = len(data)
		
		if data[idx_id] != prev_id:
			prev_id = data[idx_id]
			
		#sentence_u = unicode(data[idx_txt], 'utf_8')		
		#handler.parse(sentence_u.encode('cp932'))
		#print data[idx_txt]
		
		txt = data[idx_txt] #.encode('cp932')
		handler.parse(txt)
		result = handler.get_result()
		
		'''
		for i in range(num_fields):
			write(data[i])
			write('\t')
		write("\n")
		write("-----------------------------\n")
		'''
		
		for res in result:
			for loop in range(num_fields):
				if loop > 0:
					write('\t')
				if loop == idx_txt:
					for loop2 in range(8):
						if loop2 > 0:
							write('\t')
						write(res[loop2])
				else:
					write(data[loop]) #.encode('cp932'))
			write('\n')
		loop += 1

	handler.rm()
	

if __name__ == "__main__":
	main()
