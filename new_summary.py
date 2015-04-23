import sqlite3

con = sqlite3.connect("tmp.db")
cur = con.cursor()
'''
cur.execute('SELECT DISTINCT donor_tumour_stage_at_diagnosis FROM big_comb')
stages = cur.fetchall()
for row in stages:
	print row[0]

cur.execute('SELECT DISTINCT tumour_grade FROM big_comb')
grades = cur.fetchall()
for row in grades:
	print row[0]
'''
cur.execute('CREATE INDEX MUTATIONS ON big_comb  (chromosome, chromosome_start, chromosome_end, chromosome_strand, assembly_version, reference_genome_allele, mutated_from_allele, mutated_to_allele)')

def helper(arg, row, patient_number):
	tmp_str = u''
	if patient_number != 1:
		cur.execute('SELECT %s, count() AS num_of_stage FROM big_comb INDEXED BY MUTATIONS WHERE chromosome=? AND chromosome_start=? AND chromosome_end=? AND chromosome_strand=? AND assembly_version=? AND reference_genome_allele=? AND mutated_from_allele=? AND mutated_to_allele=? GROUP BY %s' % (arg, arg), row)
		for nr in cur.fetchall():
			if nr[0] == u'':
				tmp_str = tmp_str + (u"%s: %s patients ||" % (u'empty', nr[1]))
			else:
				tmp_str = tmp_str + (u"%s: %s patients ||" % nr)
	else:
		return True
		cur.execute('SELECT %s FROM big_comb INDEXED BY MUTATIONS WHERE chromosome=? AND chromosome_start=? AND chromosome_end=? AND chromosome_strand=? AND assembly_version=? AND reference_genome_allele=? AND mutated_from_allele=? AND mutated_to_allele=?' % (arg,), row)
		nr = cur.fetchone()
		if nr[0] == u'':
			tmp_str = tmp_str + (u"%s: 1 patient ||" % (u'empty'))
		else:
			tmp_str = tmp_str + (u"%s: 1 patient ||" % nr)
	cur.execute('UPDATE OR FAIL final_result SET %s = ? WHERE chromosome=? AND chromosome_start=? AND chromosome_end=? AND chromosome_strand=? AND assembly_version=? AND reference_genome_allele=? AND mutated_from_allele=? AND mutated_to_allele=?' % (arg, ), (tmp_str, )+row)
	return False

cur.execute('SELECT chromosome, chromosome_start, chromosome_end, chromosome_strand, assembly_version, reference_genome_allele, mutated_from_allele, mutated_to_allele, patient_number FROM final_result')
mut = cur.fetchall()
faster = 0
for brow in mut:
	pn = brow[8]
	row = brow[0:8]
	if_stop1 =  helper('donor_tumour_stage_at_diagnosis', row, pn)
	if_stop2 =helper('tumour_grade', row, pn)
	assert(if_stop1==if_stop2)
	if if_stop1 and if_stop2:
		break
	if faster>=1500:
		faster = 0
		con.commit()
	else:
		faster = faster+1

con.commit()
cur.close()

print "END!!!!!!!!!!!"
