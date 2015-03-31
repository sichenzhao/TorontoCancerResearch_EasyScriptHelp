ithLine = 1
strLst = ["chromosome_start",
		  "chromosome_end",
		  "chromosome_strand", 
		  "assembly_version",
		  "donor_tumour_stage_at_diagnosis",
		  "tumour_grade",
		  "icgc_donor_id",
		  "project_code",
		  "donor_age_at_diagnosis",
		  "mutated_to_allele",
		  "mutated_from_allele",
		  "reference_genome_allele",
		  "chromosome",
		  "donor_age_at_enrollment"
		  ]

def strToInt (strLst, firstLine):
	tmpIndex = 1
	indexList = []
	for tmpStr in firstLine:
		if tmpStr in strLst:
			indexList.append(tmpIndex)
		tmpIndex = tmpIndex + 1
	return indexList		  

def reduceFiles (inputFile, outputFile, keepIndexes):
	for line in inputFile:
		colList = [x for x in line.split('\t')]
		if ithLine==1:
			keepIndexes = strToInt(strLst, colList) + keepIndexes
		newList = []
		index = 1
		for x in colList:
			if index in keepIndexes:
				newList.append(x)
			index = index+1
		outputFile.write( '\t'.join(newList) )
		outputFile.write("\n")

def specialAppend (dictMute, criticalStr, id):
	if criticalStr in dictMute:
		if id in dictMute[criticalStr]:
			return;
		else:
			dictMute[criticalStr].append(id)
	else:
		dictMute[criticalStr] = [id]

def groupSsm (reducedSsmFile, lines=-1):
	dictMute = dict()
	for line in reducedSsmFile:
		colList = [x for x in line.split('\t')]
		specialAppend(dictMute, '\t'.join(colList[-7:]), colList[0])
		lines = lines - 1
		if lines == 0:
			break
	return dictMute

keepIndexes = []
inputFile = open('clinical.tsv', 'r')
#outputFile = open('clinicalWithoutExtra.tsv', 'w+')
#reduceFiles(inputFile, outputFile, keepIndexes)

keepIndexes = []
inputFile = open('ssm_open.tsv', 'r')
#outputFile = open('ssm_openWithoutExtra.tsv', 'w+')
outputFile = open('ssm_openWithoutExtra.tsv', 'r')
#reduceFiles(inputFile, outputFile, keepIndexes)
di = groupSsm(outputFile,100)