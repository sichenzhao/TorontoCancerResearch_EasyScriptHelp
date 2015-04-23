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

keyOfSSM = ["chromosome_start",
		  "chromosome_end",
		  "chromosome_strand",
		  "chromosome",
		  ]

# indexes of matching strings
def strToInt (strLst, firstLine):
	tmpIndex = 1
	indexList = []
	for tmpStr in firstLine:
		if tmpStr in strLst:
			indexList.append(tmpIndex)
		tmpIndex = tmpIndex + 1
	return indexList		  

# based on useful indexes, reduce file based on columns
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

# add new element for ssm dictionary
def specialAppend (dictMute, criticalStr, id):
	if criticalStr in dictMute:
		if id in dictMute[criticalStr]:
			return;
		else:
			dictMute[criticalStr].append(id)
	else:
		dictMute[criticalStr] = [id]

# group ssm file by mutation into dictionary
def groupSsm (reducedSsmFile, lines=-1):
	dictMute = dict()
	for line in reducedSsmFile:
		colList = [x for x in line.split('\t')]
		specialAppend(dictMute, '\t'.join(colList[-7:]), colList[0])
		lines = lines - 1
		if lines == 0:
			break
	return dictMute

# group clinic file by id into dictionary
def dictCli (reducedCliFile, lines=-1):
	dictId = dict()
	for line in reducedCliFile:
		colList = [x for x in line.split('\t')]
		dictId[colList[0]] = colList[1:]
		lines = lines - 1
		if lines == 0:
			break
		return dictId

# update totalInfo by combine with singleInfo
def updateInfo (totalInfo, singleInfo):
	if totalInfo == list():
		totalInfo = 
	else:
		totalInfo[3] = singleInfo[3] 
		singleInfo[4] 90-

# given cliDictionary and a idLst, should return list of combined info
def searchCli (cliDict, idLst):
	combinedInfo = list()
	for id in idLst:
		if id in cliDict:
			idLst.remove(id)
			if len(cliDict[id]) == 5:
				combinedInfo.append(cliDict[id].append(1))
			else:
				lst = cliDict[id]
				lst[-1] = lst[-1]+1
				combinedInfo.append(cliDict[id])

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