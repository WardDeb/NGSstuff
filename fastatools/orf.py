import os
import glob
import re
import warnings
warnings.filterwarnings("ignore")

from Bio import SeqIO
from Bio.Seq import Seq

class ORF:
	""" Class doc """
	
	def __init__ (self, fasta_path,out):
		""" Class initialiser """
		
		self.fasta = fasta_path
		self.min_orf = 300
		self.out = out
		
	def orf_density (self):
		""" Function doc """
		#print(self.fasta)
		fasta_sequences = SeqIO.parse(open(self.fasta),'fasta')
		out = open("{}/vrap_orf_density.csv".format(self.out),"w")
		result = {}
		for fasta in fasta_sequences:
			
			seq = fasta.seq
			seq_c = seq.reverse_complement()
			name = fasta.name
			
			frames = [1,2,3,-1,-2,-3]
			orfs = {}
			
			for f in frames:
				#print(f)
				if f < 0:
					orfs[f] = self.find_orfs(seq_c,f)
				else:
					orfs[f] = self.find_orfs(seq,f)
			
			max_orf_density = self.calc_orf_density(orfs,len(seq))
			out.write("{}\t{}\n".format(name,max_orf_density))
			result[name] = max_orf_density
		
		out.close()
		return result
	
	def calc_orf_density (self,orfs,length):
		""" Function doc """
		
		plus = [0]*length
		minus = [0]*length
		#print(orfs)
		for frame,orf in orfs.items():
			for of in orf:
				if frame>0:
					for t in of:
						plus[t]  = 1
				else:
					for t in of:
						minus[t] = 1
		
		t1 = plus.count(1)/length
		t2 = minus.count(1)/length
		
		return max(t1,t2)
	
	def find_orfs (self,seq,frame):
		""" Function doc """
		leng = len(seq)
		f = abs(frame)-1
		
		protein = str(seq[f:].translate())
		prot_leng = len(protein)
		dif = leng-(prot_leng*3)-f
		#print("dif:",+dif)
		orfs = set()

		#StartEnd
		for match in re.finditer(r'M[^*]{1,}[*]', protein):
			i,j = match.span()
			orfs.add(self.addORF((i*3)+f,(j*3)+f,frame,leng))
		#StartNoEnd
		for match in re.finditer(r'M[^*]{1,}', protein):
			
			i,j = match.span()
			if (j*3)+f==leng-dif:
				orfs.add(self.addORF((i*3)+f,leng-1,frame,leng))
		#EndNoStart
		for match in re.finditer(r'[^*M]{1,}[*]', protein):
			#print(match.span())
			i,j = match.span()
			if i==0:
				orfs.add(self.addORF(0,(j*3)+f,frame,leng))
		
		#print([frame,orfs-{None}])
		
		return orfs-{None}

	def addORF(self,i,j,frame,leng):
		r = range(0,0)
		
		if frame > 0:
			r = range(i,j)
		else:
			r = range(leng-j-1,leng-i-1)

		if len(r) >= self.min_orf:
			return r
		else:
			return None
