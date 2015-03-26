inputFile = open('clinical.tsv', 'r')
outputFile = open('clinicalWithoutExtra.tsv', 'w+')
'''
# given list l and a list of integer li, generate a list of
# integer (intList) that less than len(l) not in li
def genIndexList ( list, notDeleteList, intList ):
	for i in xrange( 0, len(list) ):
		if i not in notDeleteList:
			intList.append(i)

# given list l and a list of integer li, delList will 
# delete all elements in l with index in li
def delList ( list, indexList ):
	sindexList = sorted ( indexList, key=int)
	for indexIndex, originIndexDeleted in enumerate(indexList):
		print "now delete the original %ith element" % indexIndex
		diff = indexIndex - 1
		originIndexDeleted = indexList[diff]
		indexShouldBeDeleted = originIndexDeleted - diff
		del list[indexShouldBeDeleted]

for line in inputFile:
	lineList = [x for x in line.split('\t')]
	keepIndexes = [1,2]
	extraIndexes = list()
	genIndexList (lineList, keepIndexes, extraIndexes)
	delList (lineList, extraIndexes)
	outputFile.write( '\t'.join(lineList) )
'''

for line in inputFile:
	colList = [x for x in line.split('\t')]
	keepIndexes = [1,2,4]
	newList = []
	index = 1
	for x in colList:
		if index in keepIndexes:
			newList.append(x)
		index = index+1
	outputFile.write( '\t'.join(newList) )
	outputFile.write("\n")
