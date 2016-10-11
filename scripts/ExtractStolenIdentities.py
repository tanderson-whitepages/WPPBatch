import sys, csv, json, wppbatchlib
csv.field_size_limit(min(2147483647,sys.maxsize))

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

iFilePath = None
resultsFilePath = None

if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5 or sys.argv[1][-14:] != 'rawresults.csv':
	print 'Drop a CSV file containing raw JSON results onto this program to use it.'
	print '(you need to run SearchIDCheck.bat first)'
	var = raw_input("Hit enter to quit")
	quit()

iFilePath = sys.argv[1]
resultsFilePath = sys.argv[1][:-15]+'_results.csv'
print 'Extracting Identity Check results from '+str(iFilePath)
try:
	csvReader = csv.reader(open(iFilePath,'rb'), delimiter=',', quotechar = '"')
	csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')
except:
	print 'Error opening files'
	
headerRow = []
headerRow.append("Error")
headerRow.append("Stolen Identity Risk Level")

rowNum = 0
for row in csvReader:
	#each raw results row will contain the original input file row, followed by the API URL,
	#followed by the JSON response.
	
	rowNum += 1
	if rowNum == 1:
		csvWriter.writerow(row[:-2]+headerRow)
	else:
		data = {}
		try:
			data = json.loads(row[-1])
		except:
			print 'Error reading JSON on row '+str(rowNum)
			csvWriter.writerow(row[:-2]+['Failed to load JSON results'])
			continue
		resultRow = []
		resultRow.append('')
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('stolen_identity_check',{}),{}).get('risk_level',''),''))
		
		decodedRow = []
		for a in resultRow:
			if a is None:
				a = ''
			try:
				decodedRow.append(a.encode('utf-8'))
			except:
				try:
					decodedRow.append(str(a))
				except:
					decodedRow.append(a)
			
		try:
			csvWriter.writerow(row[:-2]+decodedRow)
		except:
			csvWriter.writerow(row[:-2]+['Failed to parse API results'])

print 'All done!'
print 'You can find your results file here: '+str(resultsFilePath)
print ''
