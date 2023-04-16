import sys

write = sys.stdout.write

class lineage:
	def __init__(self):
		# policy_data:
		#  row_id => policydata
		self.policy_data = {}

		# policy2id:
		# (key_policy_no) => row_id
		self.policy2id = {}

		# row_id => renewed flg (1 if there's a renewed policy for this)
		self.renew_flg = {}
		
		self.outdelim = '\t'
		
		self.idx_row_id = 0
		self.idx_key_policy_no = 1
		self.idx_prev_policy_no = 2

	def read_data(self, fname):
		fp = open(fname, 'r')
		header = fp.readline()
		
		# data format
		# 0: row_id
		# 1: key_policy_no
		# 2: old_policy_no
		
		for line in fp:
			data = [d.strip() for d in line[:-1].split('\t')]
			self.policy_data[data[self.idx_row_id]] = data
			
			if data[self.idx_key_policy_no] not in self.policy2id:
				self.policy2id[data[self.idx_key_policy_no]] = data[self.idx_row_id]
			else:
				sys.stderr.write("Error: policy_no already exists: "+data[self.idx_key_policy_no]+"\n")
				ptr = self.policy_data[self.policy2id[data[self.idx_key_policy_no]]]
				sys.stderr.write("ORG: "+"|".join(ptr)+"\n")
				sys.stderr.write("NEW: "+"|".join(data)+"\n")
		
		fp.close()
	
	def set_renew_flg(self):
		for row_id, data in self.policy_data.items():
			prev_policy_no = data[self.idx_prev_policy_no]
			if prev_policy_no in self.policy2id:
				self.renew_flg[self.policy2id[prev_policy_no]] = 1
			
	def name_match(self):
		for row_id, data in self.policy_data.items():
			flg = 1
			key_policy_no = data[self.idx_key_policy_no]
			prev_policy_no = data[self.idx_prev_policy_no]

			if row_id in self.renew_flg:
				renew = '1'
			elif self.policy2id[key_policy_no] in self.renew_flg:
				renew = '1'
			else:
				renew = '0'

			ptr = self.get_org_data(row_id, key_policy_no, prev_policy_no)

			# output:
			# row_id, org_row_id, num_steps, key_policy_no, org_policy_no
			write(row_id)
			write(self.outdelim)
			write(ptr['org_row_id'])
			write(self.outdelim)
			write(str(ptr['num_steps']))
			write(self.outdelim)
			write(renew)
			write(self.outdelim)
			write(key_policy_no)
			write(self.outdelim)
			write(ptr['org_policy_no'])
			write('\n')

	# returns org_row_id, org_policy_no, and num_steps
	def get_org_data(self, row_id, key_policy_no, prev_policy_no):
		result = {}
		
		num_steps = 1
		
		if row_id != self.policy2id[key_policy_no]:
			row_id = self.policy2id[key_policy_no]
			data = self.policy_data[row_id]
			key_policy_no = data[self.idx_key_policy_no]
			prev_policy_no = data[self.idx_prev_policy_no]
			num_steps += 1
		
		while num_steps <= 100:
			#if prev_policy_no == '' or prev_policy_no not in self.policy2id:
			if prev_policy_no == '':
				#print "no prev_policy_no"
				result['org_row_id'] = row_id
				result['org_policy_no'] = key_policy_no
				result['num_steps'] = num_steps
				return result
			elif prev_policy_no not in self.policy2id:
				#print "prev_policy_no not in list"
				result['org_row_id'] = row_id
				result['org_policy_no'] = key_policy_no
				result['num_steps'] = num_steps
				return result
			elif row_id == self.policy2id[prev_policy_no]:
				#print "referencing itself"
				result['org_row_id'] = row_id
				result['org_policy_no'] = key_policy_no
				result['num_steps'] = num_steps
				return result
			else:
				row_id = self.policy2id[prev_policy_no]
				data = self.policy_data[row_id]
				key_policy_no = data[self.idx_key_policy_no]
				prev_policy_no = data[self.idx_prev_policy_no]
				num_steps += 1
			
		sys.stderr.write("Error iin get_org_data. Cannot reach to org\n")
		sys.exit(1)
		
		
	def print_header(self):
		write('row_id')
		write(self.outdelim)
		write('org_row_id')
		write(self.outdelim)
		write('num_steps')
		write(self.outdelim)
		write('renew_flg')
		write(self.outdelim)
		write('key_policy_no')
		write(self.outdelim)
		write('org_policy_no')
		write('\n')

	
	def printdata(self):
		for policy_no, row_id in self.policy2id.items():
			print policy_no, ",", row_id
		

def main():
	if len(sys.argv) < 2:
		sys.stderr.write("Usage: data-lineage.py policy_fname\n")
		sys.exit(1)

	policy_fname = sys.argv[1]

	hd = lineage()
	hd.read_data(policy_fname)
	hd.set_renew_flg()
	hd.print_header()
	hd.name_match()
	
if __name__ == '__main__':
	main()
	

	
