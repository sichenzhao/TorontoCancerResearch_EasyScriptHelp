def strToInt (strLst, firstLine):
	tmpIndex = 1
	indexList = []
	for tmpStr in firstLine:
		if tmpStr in strLst:
			indexList.append(tmpIndex)
		tmpIndex = tmpIndex + 1
	return indexList

keepIndexes = []
ithLine = 1
strLst = ["chromosome_start",
		  "chromosome_end",
		  "chromosome_strand", 
		  "assembly_version",
		  "donor_tumour_stage_at_diagnosis",
		  "tumour_grade",
		  "icgc_donor_id",
		  "project_code",
		  "donor_age_at_diagnosis"]

def mainFun (inputFile, outputFile, keepIndexes):
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

inputFile = open('clinical.tsv', 'r')
outputFile = open('clinicalWithoutExtra.tsv', 'w+')
mainFun(inputFile, outputFile)

inputFile = open('ssm_open.tsv', 'r')
outputFile = open('ssm_openWithoutExtra.tsv', 'w+')
mainFun(inputFile, outputFile)
