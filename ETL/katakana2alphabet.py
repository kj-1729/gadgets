# -*- encoding: cp932 -*-

import sys
import re

write = sys.stdout.write


class kana_alpha_transf:
	def __init__(self):
		self.kana_map_1 = {u'ｱ' : 'A',  u'ｲ' : 'I',  u'ｳ' : 'U',  u'ｴ' : 'E',  u'ｵ' : 'O', 
		 u'ｶ' : 'KA',  u'ｷ' : 'KI',  u'ｸ' : 'KU',  u'ｹ' : 'KE',  u'ｺ' : 'KO', 
		 u'ｻ' : 'SA',  u'ｼ' : 'SHI',  u'ｽ' : 'SU',  u'ｾ' : 'SE',  u'ｿ' : 'SO', 
		 u'ﾀ' : 'TA',  u'ﾁ' : 'CHI',  u'ﾂ' : 'TSU',  u'ﾃ' : 'TE',  u'ﾄ' : 'TO', 
		 u'ﾅ' : 'NA',  u'ﾆ' : 'NI',  u'ﾇ' : 'NU',  u'ﾈ' : 'NE',  u'ﾉ' : 'NO', 
		 u'ﾊ' : 'HA',  u'ﾋ' : 'HI',  u'ﾌ' : 'FU',  u'ﾍ' : 'HE',  u'ﾎ' : 'HO', 
		 u'ﾏ' : 'MA',  u'ﾐ' : 'MI',  u'ﾑ' : 'MU',  u'ﾒ' : 'ME',  u'ﾓ' : 'MO', 
		 u'ﾔ' : 'YA',   u'ﾕ' : 'YU',   u'ﾖ' : 'YO', 
		 u'ﾗ' : 'RA',  u'ﾘ' : 'RI',  u'ﾙ' : 'RU',  u'ﾚ' : 'RE',  u'ﾛ' : 'RO', 
		 u'ﾜ' : 'WA',     u'ｦ' : 'WO', 
		 u'ﾝ' : 'N', u'ｰ' : '', u'-' : '', u'･' : ' '}

		self.kana_map_2 = {u'ｳﾞ' : 'VU', u'ｶﾞ' : 'GA',  u'ｷﾞ' : 'GI',  u'ｸﾞ' : 'GU',  u'ｹﾞ' : 'GE',  u'ｺﾞ' : 'GO', 
		 u'ｻﾞ' : 'ZA',  u'ｼﾞ' : 'JI',  u'ｽﾞ' : 'ZU',  u'ｾﾞ' : 'ZE',  u'ｿﾞ' : 'ZO', 
		 u'ﾀﾞ' : 'DA',  u'ﾁﾞ' : 'DI',  u'ﾂﾞ' : 'DU',  u'ﾃﾞ' : 'DE',  u'ﾄﾞ' : 'DO', 
		 u'ﾊﾞ' : 'BA',  u'ﾋﾞ' : 'BI',  u'ﾌﾞ' : 'BU',  u'ﾍﾞ' : 'BE',  u'ﾎﾞ' : 'BO', 
		 u'ﾊﾟ' : 'PA',  u'ﾋﾟ' : 'PI',  u'ﾌﾟ' : 'PU',  u'ﾍﾟ' : 'PE',  u'ﾎﾟ' : 'PO'}


		self.kana_map_3 = {u'ｳｧ' : 'WA', u'ｳｨ' : 'WI', u'ｳｪ' : 'WE', u'ｳｫ' : 'WO',
		 u'ｷｬ' : 'KYA',  u'ｷｭ' : 'KYU',  u'ｷｮ' : 'KYO', 
		 u'ｼｬ' : 'SYA',  u'ｼｭ' : 'SYU',  u'ｼｪ' : 'SHE',  u'ｼｮ' : 'SYO', 
		 u'ﾁｬ' : 'TYA',  u'ﾁｭ' : 'TYU',  u'ﾁｪ' : 'CHE', u'ﾁｮ' : 'TYO', 
		 u'ﾃｨ' : 'TYI', u'ﾄｩ' : 'TYU',
		 u'ﾆｬ' : 'NYA',  u'ﾆｭ' : 'NYU',  u'ﾆｮ' : 'NYO', 
		 u'ﾋｬ' : 'HYA',  u'ﾋｭ' : 'HYU',  u'ﾋｮ' : 'HYO', 
		 u'ﾌｧ' : 'FA',  u'ﾌｨ' : 'FI',  u'ﾌｪ' : 'FE',  u'ﾌｫ' : 'FO', 
		 u'ﾐｬ' : 'MYA',  u'ﾐｭ' : 'MYU',  u'ﾐｮ' : 'MYO', 
		 u'ﾘｬ' : 'RYA',  u'ﾘｭ' : 'RYU',  u'ﾘｮ' : 'RYO'}

		self.kana_map_4 = {u'ｳﾞｧ' : 'VA', u'ｳﾞｨ': 'VI', u'ｳﾞｪ' : 'VE', u'ｳﾞｫ' : 'VO',
		 u'ｷﾞｬ' : 'GYA',  u'ｷﾞｭ' : 'GYU',  u'ｷﾞｮ' : 'GYO', 
		 u'ｸﾞｪ' : 'GYE',
		 u'ｼﾞｬ' : 'JA',  u'ｼﾞｭ' : 'JU',  u'ｼﾞｪ' : 'JE', u'ｼﾞｮ' : 'JO', 
		 u'ﾁﾞｬ' : 'DYA',  u'ﾁﾞｭ' : 'DYU',  u'ﾁﾞｮ' : 'DYO',
		 u'ﾃﾞｨ' : 'DYI', u'ﾃﾞｭ' : 'DYU',  u'ﾄﾞｩ' : 'DU',
		 u'ﾋﾞｬ' : 'BYA',  u'ﾋﾞｭ' : 'BYU',  u'ﾋﾞｮ' : 'BYO', 
		 u'ﾋﾟｬ' : 'PYA',  u'ﾋﾟｭ' : 'PYU',  u'ﾋﾟｮ' : 'PYO'}

		self.multiple_str = {u'ﾞ' : 1, u'ﾟ' : 1,  u'ｬ' : 1,  u'ｭ' : 1,  u'ｮ' : 1,  u'ｧ' : 1,  u'ｨ' : 1,  u'ｩ' : 1,  u'ｪ' : 1,  u'ｫ' : 1}
		self.small_tsu = u'ｯ'
		
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

