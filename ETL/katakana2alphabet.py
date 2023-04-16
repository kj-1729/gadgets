# -*- encoding: cp932 -*-

import sys
import re

write = sys.stdout.write


class kana_alpha_transf:
	def __init__(self):
		self.kana_map_1 = {u'�' : 'A',  u'�' : 'I',  u'�' : 'U',  u'�' : 'E',  u'�' : 'O', 
		 u'�' : 'KA',  u'�' : 'KI',  u'�' : 'KU',  u'�' : 'KE',  u'�' : 'KO', 
		 u'�' : 'SA',  u'�' : 'SHI',  u'�' : 'SU',  u'�' : 'SE',  u'�' : 'SO', 
		 u'�' : 'TA',  u'�' : 'CHI',  u'�' : 'TSU',  u'�' : 'TE',  u'�' : 'TO', 
		 u'�' : 'NA',  u'�' : 'NI',  u'�' : 'NU',  u'�' : 'NE',  u'�' : 'NO', 
		 u'�' : 'HA',  u'�' : 'HI',  u'�' : 'FU',  u'�' : 'HE',  u'�' : 'HO', 
		 u'�' : 'MA',  u'�' : 'MI',  u'�' : 'MU',  u'�' : 'ME',  u'�' : 'MO', 
		 u'�' : 'YA',   u'�' : 'YU',   u'�' : 'YO', 
		 u'�' : 'RA',  u'�' : 'RI',  u'�' : 'RU',  u'�' : 'RE',  u'�' : 'RO', 
		 u'�' : 'WA',     u'�' : 'WO', 
		 u'�' : 'N', u'�' : '', u'-' : '', u'�' : ' '}

		self.kana_map_2 = {u'��' : 'VU', u'��' : 'GA',  u'��' : 'GI',  u'��' : 'GU',  u'��' : 'GE',  u'��' : 'GO', 
		 u'��' : 'ZA',  u'��' : 'JI',  u'��' : 'ZU',  u'��' : 'ZE',  u'��' : 'ZO', 
		 u'��' : 'DA',  u'��' : 'DI',  u'��' : 'DU',  u'��' : 'DE',  u'��' : 'DO', 
		 u'��' : 'BA',  u'��' : 'BI',  u'��' : 'BU',  u'��' : 'BE',  u'��' : 'BO', 
		 u'��' : 'PA',  u'��' : 'PI',  u'��' : 'PU',  u'��' : 'PE',  u'��' : 'PO'}


		self.kana_map_3 = {u'��' : 'WA', u'��' : 'WI', u'��' : 'WE', u'��' : 'WO',
		 u'��' : 'KYA',  u'��' : 'KYU',  u'��' : 'KYO', 
		 u'��' : 'SYA',  u'��' : 'SYU',  u'��' : 'SHE',  u'��' : 'SYO', 
		 u'��' : 'TYA',  u'��' : 'TYU',  u'��' : 'CHE', u'��' : 'TYO', 
		 u'è' : 'TYI', u'ĩ' : 'TYU',
		 u'Ƭ' : 'NYA',  u'ƭ' : 'NYU',  u'Ʈ' : 'NYO', 
		 u'ˬ' : 'HYA',  u'˭' : 'HYU',  u'ˮ' : 'HYO', 
		 u'̧' : 'FA',  u'̨' : 'FI',  u'̪' : 'FE',  u'̫' : 'FO', 
		 u'Ь' : 'MYA',  u'Э' : 'MYU',  u'Ю' : 'MYO', 
		 u'ج' : 'RYA',  u'ح' : 'RYU',  u'خ' : 'RYO'}

		self.kana_map_4 = {u'�ާ' : 'VA', u'�ި': 'VI', u'�ު' : 'VE', u'�ޫ' : 'VO',
		 u'�ެ' : 'GYA',  u'�ޭ' : 'GYU',  u'�ޮ' : 'GYO', 
		 u'�ު' : 'GYE',
		 u'�ެ' : 'JA',  u'�ޭ' : 'JU',  u'�ު' : 'JE', u'�ޮ' : 'JO', 
		 u'�ެ' : 'DYA',  u'�ޭ' : 'DYU',  u'�ޮ' : 'DYO',
		 u'�ި' : 'DYI', u'�ޭ' : 'DYU',  u'�ީ' : 'DU',
		 u'�ެ' : 'BYA',  u'�ޭ' : 'BYU',  u'�ޮ' : 'BYO', 
		 u'�߬' : 'PYA',  u'�߭' : 'PYU',  u'�߮' : 'PYO'}

		self.multiple_str = {u'�' : 1, u'�' : 1,  u'�' : 1,  u'�' : 1,  u'�' : 1,  u'�' : 1,  u'�' : 1,  u'�' : 1,  u'�' : 1,  u'�' : 1}
		self.small_tsu = u'�'
		
		#self.error_str = '[ERROR]'
		self.error_str = ''

	def kana2alpha(self, str):
		self.alpha_str = ''
		self.orig_str = ''
		str_len = len(str)
		
		self.flg_small_tsu = 'N'
		loop_st = 0
		while loop_st < str_len:
			if str[loop_st] == ' ':
			### blank
				self.alpha_str += ' '
				self.orig_str += '|' + str[loop_st]
				loop_st += 1
			else:
				m = re.search('[A-Za-z0-9\'\.\-\(\)]', str[loop_st])
				if m is not None:
				### alphabet
					self.alpha_str += str[loop_st]
					self.orig_str += '|' + str[loop_st]
					loop_st += 1
				else:
					if loop_st + 1 >= str_len:
					### 1 character (end of str)
						chr = self.get_alpha(1, str[loop_st])
						self.alpha_str = self.alpha_str + chr
						self.orig_str += '|' + str[loop_st]
						loop_st += 1
					elif str[loop_st] == self.small_tsu:
						self.flg_small_tsu = 'Y'
						loop_st += 1
					else:
						loop_ed = loop_st+1
						if self.multiple_str.has_key(str[loop_ed]):
						### 2 or more characters
							loop_ed += 1
							if loop_ed >= str_len:
							### 2 characters (end of str)
								chr = self.get_alpha(2, str[loop_st:loop_ed])
								self.orig_str += '|' + str[loop_st:loop_ed]
								self.alpha_str = self.alpha_str + chr
								loop_st += 2
							elif self.multiple_str.has_key(str[loop_ed]):
							### 3 characters
								loop_ed += 1
								chr = self.get_alpha(3, str[loop_st:loop_ed])
								self.orig_str += '|' + str[loop_st:loop_ed]
								self.alpha_str = self.alpha_str + chr
								loop_st += 3
							else:
							### 2 characters
								chr = self.get_alpha(2, str[loop_st:loop_ed])
								self.orig_str += '|' + str[loop_st:loop_ed]
								self.alpha_str = self.alpha_str + chr
								loop_st += 2
						else:
						### 1 character
							chr = self.get_alpha(1, str[loop_st])
							self.orig_str += '|' + str[loop_st]
							self.alpha_str = self.alpha_str + chr
							loop_st += 1
		#write("ORIG: "+self.orig_str.encode('cp932')+"\n")
		return self.pretty_alpha_str(self.alpha_str)
		
		
	def get_alpha(self, len_str, str):
		if len_str == 1:
			if self.kana_map_1.has_key(str):
				this_chr = self.kana_map_1[str]
			else:
				return self.error_str
		elif len_str == 2:
			if self.kana_map_2.has_key(str):
				this_chr = self.kana_map_2[str]
			elif self.kana_map_3.has_key(str):
				this_chr = self.kana_map_3[str]
			else:
				return self.error_str
		elif len_str == 3:
			if self.kana_map_4.has_key(str):
				this_chr = self.kana_map_4[str]
			else:
				return self.error_str
		else:
			return self.error_str

		if self.flg_small_tsu == 'Y':
			self.flg_small_tsu = 'N'
			if len(this_chr) > 0:
				return this_chr[0] + this_chr
			else:
				return this_chr
		else:
			return this_chr

	def pretty_alpha_str(self, str):
		pretty_str = re.sub('OU', 'O', str)
		pretty_str = re.sub('UU', 'U', pretty_str)
		pretty_str = re.sub('OO', 'O', pretty_str)

		return pretty_str
		
	def flip_name(self, str):
		m = re.search('^([^\s]*) (.*)$', str)
		if m is not None:
			flipped_str = m.group(2) + ' ' + m.group(1)
		else:
			flipped_str = str
		
		return flipped_str
		
	def get_orig_str(self):
		return self.orig_str
		
def pretty_claimant_name(str):
	m = re.search('^TY[0-9]* (.*)$', str)
	if m is not None:
		return m.group(1)
	else:
		m = re.search('^EQ[0-9]* (.*)$', str)
		if m is not None:
			return m.group(1)
		else:
			m = re.search('^LP[0-9]* (.*)$', str)
			if m is not None:
				return m.group(1)
			else:
				return str

def main():
	header = sys.stdin.readline()
	hd = kana_alpha_transf()
	idx_claimant_name = 12
	
	outdelim = "\t"
	cnt = 0
	for line in sys.stdin:
		line_u = unicode(line, 'cp932')
		data = line_u[:-1].split('\t')
		
		claimant_name = pretty_claimant_name(data[idx_claimant_name])
		#print "-------------------------------------"
		alpha_str = hd.kana2alpha(claimant_name)
		cnt += 1
		
		write(data[0])
		write(outdelim)
		#write(data[1])
		#write(outdelim)
		#write(data[idx_claimant_name].encode('cp932'))
		#write(outdelim)
		#write((hd.get_orig_str()).encode('cp932'))
		#write(outdelim)
		write(alpha_str)
		write(outdelim)
		write(hd.flip_name(alpha_str))
		write("\n")
		

if __name__ == '__main__':
	main()

