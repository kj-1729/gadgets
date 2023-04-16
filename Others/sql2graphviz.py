# -*- coding: utf-8 -*-

import sys
import re
import ky_vars

write = sys.stdout.write


class sql2graphviz:
	def __init__(self, node_fname, edge_fname):
		self.ky_vars = ky_vars.ky_vars()
		self.node_fname = node_fname
		self.edge_fname = edge_fname
		self.color_list = []

	##########################################################################
	#                                                                        #
	#                                                                        #
	#                         Init Functions                                 #
	#                                                                        #
	#                                                                        #
	##########################################################################
	def init_vars(self):
		self.sql_fname = ''
		self.status_cd = 0
		# 3: SQL
		# ...
		# 0: Other

		self.proc_name = ''
		self.full_proc_name = ''
		self.this_script = ''
		self.to_table = ''
		self.from_tables = {}

		self.cnt_edges = 1
		self.cnt_nodes = 1
		self.nodes = {}
		self.edges = {}
		
		self.node_to_color = {}
		self.edge_to_color = {}

	def set_colors(self):
		#self.color_list = ['aliceblue', 'antiquewhite', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornsilk', 'crimson', 'cyan', 'darkgoldenrod', 'darkgreen', 'darkkhaki', 'darkolivegreen', 'darkorchid', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'invis', 'ivory', 'khaki', 'lavender', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrod', 'lightgray', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'limegreen', 'linen', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'navyblue', 'none', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato', 'transparent', 'turquoise', 'violet']
		self.color_list = ['aliceblue', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornsilk', 'crimson', 'cyan', 'darkgoldenrod', 'darkgreen', 'darkkhaki', 'darkolivegreen', 'darkorchid', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'forestgreen', 'gainsboro', 'gold', 'goldenrod', 'gray', 'green', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'invis', 'ivory', 'khaki', 'lavender', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrod', 'lightgray', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'limegreen', 'linen', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'mintcream', 'mistyrose', 'moccasin', 'navy', 'navyblue', 'none', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato', 'transparent', 'turquoise', 'violet']


	##########################################################################
	#                                                                        #
	#                                                                        #
	#                         Process Input Data                             #
	#                                                                        #
	#                                                                        #
	##########################################################################

	def process(self):
		
		self.init_vars()
		self.set_colors()
		
		for line in sys.stdin:
			self.sql_fname = line[:-1]
			self.do_process(self.sql_fname)

		self.fp_node = open(self.node_fname, 'w')
		self.fp_edge = open(self.edge_fname, 'w')
		self.print_nodes_header()
		self.print_edges_header()
		self.print_nodes()
		self.print_edges()
		self.fp_node.close()
		self.fp_edge.close()
		
	def do_process(self, sql_fname):
		cnt = 0
		#sys.stderr.write("# Process "+sql_fname+self.ky_vars.eol)
		fp = open(sql_fname, 'r')
		
		for line in fp:
			#sys.stderr.write("(I)"+line)
			line_u = unicode(line, self.ky_vars.incode)

			if self.status_cd == 0:
				# SAS: extract "proc xxx"
				m = re.search('^\s*create\s+([^\s;]*)[\s;]', line_u)
				if m is not None:
					self.status_cd = 3
					self.proc_name = m.group(1)
					self.full_proc_name = line_u
					self.this_script = line_u
						
			elif self.status_cd == 3:
				m = re.search('^\-\-', line_u)
				if m is not None:
					continue
				else:
					m = re.search('^/\*', line_u)
					if m is not None:
						self.process_a_script()
					else:
						self.this_script += line_u
			
			cnt += 1
		
		fp.close()


	##########################################################################
	#                                                                        #
	#                                                                        #
	#                 Process proc sql/data/SQL scripts                      #
	#                                                                        #
	#                                                                        #
	##########################################################################
	def process_a_script(self):
		#sys.stderr.write("===== process_a_script ==========\n")
		#sys.stderr.write(self.this_script.encode('cp932')+"\n")
		#sys.stderr.write("============ Script End ============\n")
		
		#if self.proc_name[:3] == 'sql':
		if self.status_cd == 3:
			self.process_sql()
			self.update_data()
			#self.print_stderr_nodes()
			#self.print_script()
		else:
			sys.stderr.write('Warning\n')
			self.print_stderr_script()
				
		self.status_cd = 0
		self.proc_name = ''
		self.this_script = ''
		self.to_table = ''
		self.from_tables = {}
	
	def process_sql(self):
		copy_script = re.sub('\n', ' ', self.this_script)
		copy_script = ' ' + re.sub('/\*.*?\*/', '', copy_script)

		m = re.search('\s+create\s+(table|view)\s+([^\s]*)\s+as\s+(.*)', copy_script)
		if m is not None:
			self.to_table = self.pretty_str(m.group(2))
			#sys.stderr.write("------ process_sql: to_table ------------\n")
			#sys.stderr.write(self.to_table+'\n')
			#sys.stderr.write("------- to_table End ----------\n")
			script_remain = m.group(3)
		else:
			#sys.stderr.write('### Not create table/view\n')
			return
		#sys.stderr.write("------ process_sql: script remain ------------\n")
		#sys.stderr.write(script_remain.encode('cp932')+'\n')
		#sys.stderr.write("------- script_remain End ----------\n")

		cnt = 1
		m = re.search('\s+from\s+([^\s]*)\s+(.*)', script_remain)
		if m is not None:
			from_table = self.pretty_str(m.group(1))
			#sys.stderr.write("------ process_sql: from_table ------------\n")
			#sys.stderr.write(from_table+'\n')
			#sys.stderr.write("------- from_table End ----------\n")
			
			if len(from_table) > 0 and not self.from_tables.has_key(from_table):
				self.from_tables[from_table] = cnt
				cnt += 1
			script_remain = m.group(2)
			#sys.stderr.write("------ process_sql: script remain(2) ------------\n")
			#sys.stderr.write(script_remain.encode('cp932')+'\n')
			#sys.stderr.write("------- script_remain(2) End ----------\n")
		else:
			sys.stderr.write('### Error: from not found\n')
			
			return
		
		flg = 1
		while flg == 1:
			m = re.search('\s(left join|right join|inner join|from)\s+([^\s]*)\s+(.*)$', script_remain)
			if m is not None:
				from_table = self.pretty_str(m.group(2))
				#sys.stderr.write("------ process_sql: from_table(2) ------------\n")
				#sys.stderr.write(from_table+'\n')
				#sys.stderr.write("------- from_table(2) End ----------\n")
				if len(from_table) > 0 and not self.from_tables.has_key(from_table):
					self.from_tables[from_table] = cnt
					cnt += 1
				script_remain = m.group(3)
				#sys.stderr.write("------ process_sql: script remain(3) ------------\n")
				#sys.stderr.write(script_remain.encode('cp932')+'\n')
				#sys.stderr.write("------- script_remain(3) End ----------\n")
			else:
				flg = 0
		
		return

		
	def update_data(self):
		if self.to_table == '_null_':
			return
			
		# nodes
		if not self.nodes.has_key(self.to_table):
			self.nodes[self.to_table] = self.cnt_nodes
			self.cnt_nodes += 1
		for k, v in sorted(self.from_tables.items(), key=lambda x:x[1]):
			if not self.nodes.has_key(k):
				self.nodes[k] = self.cnt_nodes
				self.cnt_nodes += 1
		
		# edges
		for from_t, v in sorted(self.from_tables.items(), key=lambda x:x[1]):
			str = from_t + '\t' + self.to_table + '\t' + self.sql_fname
			if not self.edges.has_key(str):
				self.edges[str] = self.cnt_edges
				self.cnt_edges += 1
	
	def pretty_str(self, str):
		#chr = "\\"
		str = re.sub("'", '', str)
		str = re.sub('"', '', str)
		str = re.sub("\(", '', str)
		str = re.sub('\)', '', str)
		
		path = []
		st = 0
		for loop in range(len(str)):
			if str[loop] == '\\':
				path.append(str[st:loop])
				st = loop+1
		path.append(str[st:])
		
		str = '/'.join(path)
			
		return str.lower()
	
	def split_str(self, str):
		m = re.search('^([^\.]*)\.(.*)$', str)
		if m is not None:
			name_space = m.group(1)
			tbl = str # m.group(2)
		else:
			name_space = 'work'
			tbl = str
			
		return [name_space, tbl]
		
	##########################################################################
	#                                                                        #
	#                                                                        #
	#                   Output Functions                                     #
	#                                                                        #
	#                                                                        #
	##########################################################################
	def print_nodes_header(self):
		# header
		self.fp_node.write('name_space')
		self.fp_node.write(self.ky_vars.outdelim)
		self.fp_node.write('layer')
		self.fp_node.write(self.ky_vars.outdelim)
		self.fp_node.write('label')
		self.fp_node.write(self.ky_vars.outdelim)
		self.fp_node.write('shape')
		self.fp_node.write(self.ky_vars.outdelim)
		self.fp_node.write('style')
		self.fp_node.write(self.ky_vars.outdelim)
		self.fp_node.write('color')
		self.fp_node.write(self.ky_vars.outdelim)
		self.fp_node.write('charset')
		self.fp_node.write(self.ky_vars.outdelim)
		self.fp_node.write('fontname')
		self.fp_node.write(self.ky_vars.outdelim)
		self.fp_node.write('fontsize')
		self.fp_node.write(self.ky_vars.eol)
		

	def print_nodes(self):
		cnt = 0

		for k, v in sorted(self.nodes.items(), key=lambda x:x[1]):
			[name_space, tbl] = self.split_str(k)

			# Temporary
			m = re.search('^\s*$', tbl)
			if m is not None:
				continue
				
			if self.node_to_color.has_key(name_space):
				color = self.node_to_color[name_space]
			else:
				color = self.color_list[cnt]
				self.node_to_color[name_space] = color
				cnt += 1
				if cnt >= len(self.color_list):
					cnt = 0
				
			self.fp_node.write(name_space)
			self.fp_node.write(self.ky_vars.outdelim)
			self.fp_node.write('')  # layer
			self.fp_node.write(self.ky_vars.outdelim)
			self.fp_node.write(tbl) # Table
			self.fp_node.write(self.ky_vars.outdelim)
			self.fp_node.write('')  # Shape
			self.fp_node.write(self.ky_vars.outdelim)
			self.fp_node.write('')  # Style
			self.fp_node.write(self.ky_vars.outdelim)
			self.fp_node.write(color)  # Color
			self.fp_node.write(self.ky_vars.outdelim)
			self.fp_node.write('')  # Charset
			self.fp_node.write(self.ky_vars.outdelim)
			self.fp_node.write('')  # Fontname
			self.fp_node.write(self.ky_vars.outdelim)
			self.fp_node.write('')  # Fontsize
			self.fp_node.write(self.ky_vars.eol)


	def print_edges_header(self):
		# header
		self.fp_edge.write('name_space_from')
		self.fp_edge.write(self.ky_vars.outdelim)
		self.fp_edge.write('name_space_to')
		self.fp_edge.write(self.ky_vars.outdelim)
		self.fp_edge.write('node_label_from')
		self.fp_edge.write(self.ky_vars.outdelim)
		self.fp_edge.write('node_label_to')
		self.fp_edge.write(self.ky_vars.outdelim)
		self.fp_edge.write('label')
		self.fp_edge.write(self.ky_vars.outdelim)
		self.fp_edge.write('style')
		self.fp_edge.write(self.ky_vars.outdelim)
		self.fp_edge.write('color')
		self.fp_edge.write(self.ky_vars.outdelim)
		self.fp_edge.write('fontname')
		self.fp_edge.write(self.ky_vars.outdelim)
		self.fp_edge.write('fontsize')
		self.fp_edge.write(self.ky_vars.eol)

	def print_edges(self):
		cnt = 0
		for k, v in sorted(self.edges.items(), key=lambda x:x[1]):
			[from_tbl, to_tbl, sql_fname] = k.split('\t')
			[from_name_space, from_tbl] = self.split_str(from_tbl)
			[to_name_space, to_tbl] = self.split_str(to_tbl)

			if self.edge_to_color.has_key(sql_fname):
				color = self.edge_to_color[sql_fname]
			else:
				color = self.color_list[cnt]
				self.edge_to_color[sql_fname] = color
				cnt += 1
				if cnt >= len(self.color_list):
					cnt = 0
			
			self.fp_edge.write(from_name_space) # name_space_from
			self.fp_edge.write(self.ky_vars.outdelim)
			self.fp_edge.write(to_name_space)   # name space to
			self.fp_edge.write(self.ky_vars.outdelim)
			self.fp_edge.write(from_tbl)        # node from
			self.fp_edge.write(self.ky_vars.outdelim)
			self.fp_edge.write(to_tbl)          # node to
			self.fp_edge.write(self.ky_vars.outdelim)
			self.fp_edge.write('')              # edge
			#self.fp_edge.write(sql_fname)              # edge
			self.fp_edge.write(self.ky_vars.outdelim)
			self.fp_edge.write('')              # style
			self.fp_edge.write(self.ky_vars.outdelim)
			self.fp_edge.write(color)              # color
			self.fp_edge.write(self.ky_vars.outdelim)
			self.fp_edge.write('')              # fontname
			self.fp_edge.write(self.ky_vars.outdelim)
			self.fp_edge.write('')              # fontsize
			self.fp_edge.write('\n')
			
	def print_stderr_nodes(self):
		cnt = 0

		sys.stderr.write("--------------- print_stderr_nodes ------------------\n")
		for k, v in sorted(self.nodes.items(), key=lambda x:x[1]):
			[name_space, tbl] = self.split_str(k)

			# Temporary
			m = re.search('^\s*$', tbl)
			if m is not None:
				continue
				
			if self.node_to_color.has_key(name_space):
				color = self.node_to_color[name_space]
			else:
				color = self.color_list[cnt]
				self.node_to_color[name_space] = color
				cnt += 1
				if cnt >= len(self.color_list):
					cnt = 0
				
			sys.stderr.write(name_space)
			sys.stderr.write(self.ky_vars.outdelim)
			sys.stderr.write('')  # layer
			sys.stderr.write(self.ky_vars.outdelim)
			sys.stderr.write(tbl) # Table
			sys.stderr.write(self.ky_vars.outdelim)
			sys.stderr.write('')  # Shape
			sys.stderr.write(self.ky_vars.outdelim)
			sys.stderr.write('')  # Style
			sys.stderr.write(self.ky_vars.outdelim)
			sys.stderr.write(color)  # Color
			sys.stderr.write(self.ky_vars.outdelim)
			sys.stderr.write('')  # Charset
			sys.stderr.write(self.ky_vars.outdelim)
			sys.stderr.write('')  # Fontname
			sys.stderr.write(self.ky_vars.outdelim)
			sys.stderr.write('')  # Fontsize
			sys.stderr.write(self.ky_vars.eol)
		sys.stderr.write("--------------- print_stderr_nodes ------------------\n")

	def print_script(self):
		print "<-------------------------------------------------"
		print '###################'
		write('Proc: '+self.proc_name+'\n')
		write('Table(To): '+self.to_table+'\n')
		for t in self.from_tables.keys():
			write('Table(From): '+t+'\n')
			
		print '###################'
		write(self.this_script.encode(self.ky_vars.outcode))
		print "------------------------------------------------->"

	def print_stderr_script(self):
		sys.stderr.write("<-------------------------------------------------"+self.ky_vars.eol)
		sys.stderr.write('###################'+self.ky_vars.eol)
		sys.stderr.write('Proc: '+self.proc_name+'\n')
		sys.stderr.write('Table(To): '+self.to_table+'\n')
		for t in self.from_tables.keys():
			sys.stderr.write('Table(From): '+t+'\n')
			
		sys.stderr.write('###################'+self.ky_vars.eol)
		sys.stderr.write(self.full_proc_name.encode(self.ky_vars.outcode)+self.ky_vars.eol)
		sys.stderr.write(self.this_script.encode(self.ky_vars.outcode)+self.ky_vars.eol)
		sys.stderr.write("------------------------------------------------->"+self.ky_vars.eol)

# Need all sqls are separated by a line /***** xxx ****/ in sql files.
def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: cat datafile | python $0 node_fname edge_fname\n')
		sys.exit(1)
	
	node_fname = sys.argv[1]
	edge_fname = sys.argv[2]
	
	hd = sql2graphviz(node_fname, edge_fname)
	hd.process()

	
if __name__ == '__main__':
	main()


		