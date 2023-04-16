# -*- coding: shift_jis -*-
import math
import sys

write = sys.stdout.write

indent = '\t'

class make_graphviz:
	def __init__(self, graph_label, node_fname, edge_fname):
		self.node2id = {}
		self.rank_nodes = {}
		
		self.graph_name = 'test'
		
		if graph_label is None:
			self.graph_label = 'test'
		else:
			self.graph_label = graph_label

		self.node_fname = node_fname
		self.edge_fname = edge_fname
		
		self.node_attr = ['label', 'charset', 'fontname', 'fontsize', 'shape', 'style', 'color']
		self.edge_attr = ['label', 'charset', 'fontname', 'fontsize', 'style', 'color']

	def print_header(self):
		#'rotate=90', 'fontsize=20'
		options = ['labelloc=t', 'rankdir=LR']
		option_str = ', '.join(options)

		print 'digraph ' + self.graph_name + '{'
		print indent + 'graph [label="' + self.graph_label + '", ' + option_str + '];'
		print indent + 'node [shape=box, style=rounded]; edge [labelfloat=true];'
		print indent
		
	def print_footer(self):
		print '}'

	# node attributes
	# - label: (name)
	# - charset: UTF-8
	# - fontname: MS UI Gothic/
	# - fontsize: 10/
	# - shape: Mrecord/box/ellipse
	# - style: filled/rounded/etc.
	# - color: white/blue/black/blue/red/etc.
	def print_node(self, node):
		write(indent + indent + node['NODE_ID'])
		loop = 0
		for item in self.node_attr:
			if node.has_key(item):
				if loop == 0:
					write(' [')
				else:
					write(', ')
				if item == 'label':
					write(item+'="'+node[item]+'"')
				else:
					write(item+'='+node[item])
				loop += 1
		if loop > 0:
			write(']')
		write(';\n')
	
	# edge attributes
	# - label
	# - style: dashed/
	# - fontsize: 10/
	def print_edge(self, edge):
		write(indent + indent + edge['NODE_ID_FROM'] + ' -> ' + edge['NODE_ID_TO'])
		loop = 0
		for item in self.node_attr:
			if edge.has_key(item):
				if loop == 0:
					write(' [')
				else:
					write(', ')
				if item == 'label':
					write(item+'="'+edge[item]+'"')
				else:
					write(item+'='+edge[item])
				loop += 1
		if loop > 0:
			write(']')
		write(';\n')

	
	def set_rank(self):
		for (k, v) in self.rank_nodes.items():
			write(indent+indent+'{rank=same; ' + v + ';}\n')
			
	def process(self):
		##########################################
		#            process node                #
		##########################################
		fp = open(self.node_fname, 'r')
		header = fp.readline()
		field_name = header[:-1].split('\t')
		num_nodes = 0
		# input data
		# 0: label (node_name)
		# 1: attribute1
		# 2: attribute2
		# ...
		# x: LAYER
		for line in fp:
			data = line[:-1].split('\t')
			node = {}
			for loop in range(len(field_name)):
				if len(data[loop]) > 0:
					node[field_name[loop]] = data[loop].lower()

			node['NODE_ID'] = 'node_' + str(num_nodes)
			num_nodes += 1
			self.node2id[node['label']] = node['NODE_ID']

			# print node
			self.print_node(node)

			# set rank
			if node.has_key('layer'):
				rank = node['layer']
				if not self.rank_nodes.has_key(rank):
					dummy = ''
					self.rank_nodes[rank] = dummy
				self.rank_nodes[rank] = self.rank_nodes[rank] + ' ' + node['NODE_ID']

		fp.close()
		
		##########################################
		#            process edge                #
		##########################################
		fp = open(self.edge_fname, 'r')
		header = fp.readline()
		field_name = header[:-1].split('\t')
		# input data
		# 0: node_label_from
		# 1: node_label_to
		# 2: attribute 1
		# ...
		for line in fp:
			data = line[:-1].split('\t')
			edge = {}
			for loop in range(len(field_name)):
				if len(data[loop]) > 0:
					edge[field_name[loop]] = data[loop].lower()

			# set node_from
			if not self.node2id.has_key(edge['node_label_from']):
				self.node2id[edge['node_label_from']] = 'node_' + str(num_nodes)
				sys.stderr.write('ERROR: No node for '+edge['node_label_from']+'\n')
				num_nodes += 1
			edge['NODE_ID_FROM'] = self.node2id[edge['node_label_from']]

			# set node_label_to
			if not self.node2id.has_key(edge['node_label_to']):
				self.node2id[edge['node_label_to']] = 'node_' + str(num_nodes)
				sys.stderr.write('ERROR: No node for '+edge['node_label_to']+'\n')
				num_nodes += 1
			edge['NODE_ID_TO'] = self.node2id[edge['node_label_to']]
				
			# print edge
			self.print_edge(edge)
		fp.close()
		

def main():
	if len(sys.argv) < 4:
		sys.stderr.write('Usage: python $0 graph_name node_fname edge_fname > graphviz_file\n')
		sys.exit(1)
	
	graph_name = sys.argv[1]
	node_fname = sys.argv[2]
	edge_fname = sys.argv[3]

	hd = make_graphviz(graph_name, node_fname, edge_fname)
	hd.print_header()
	hd.process()
	hd.set_rank()
	hd.print_footer()

if __name__ == '__main__':
	main()
	
		
