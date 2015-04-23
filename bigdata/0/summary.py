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

def helper(arg, row):
	cur.execute('SELECT %s, count() AS num_of_stage FROM big_comb WHERE chromosome=? AND chromosome_start=? AND chromosome_end=? AND chromosome_strand=? AND assembly_version=? AND reference_genome_allele=? AND mutated_from_allele=? AND mutated_to_allele=? GROUP BY %s' % (arg, arg), row)
	tmp_str = u''
	for nr in cur.fetchall():
		if nr[0] == u'':
			tmp_str = tmp_str + (u"%s: %s patients ||" % (u'empty', nr[1]))
		else:
			tmp_str = tmp_str + (u"%s: %s patients ||" % nr)
	cur.execute('UPDATE OR FAIL final_result SET %s = ? WHERE chromosome=? AND chromosome_start=? AND chromosome_end=? AND chromosome_strand=? AND assembly_version=? AND reference_genome_allele=? AND mutated_from_allele=? AND mutated_to_allele=?' % (arg, ), (tmp_str, )+row)

cur.execute('SELECT DISTINCT chromosome, chromosome_start, chromosome_end, chromosome_strand, assembly_version, reference_genome_allele, mutated_from_allele, mutated_to_allele FROM final_result')
mut = cur.fetchall()
for row in mut:
	helper('donor_tumour_stage_at_diagnosis', row)
	helper('tumour_grade', row)
	con.commit()


cur.close()




