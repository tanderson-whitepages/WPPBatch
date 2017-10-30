import sys, csv, json, wppbatchlib
csv.field_size_limit(min(2147483647,sys.maxsize))

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

iFilePath = None
resultsFilePath = None

if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5 or sys.argv[1][-14:] != 'rawresults.csv':
	print 'Drop a CSV file containing raw JSON results onto this program to use it.'
	print '(you need to run SearchPhone.bat first)'
	var = raw_input("Hit enter to quit")
	quit()

iFilePath = sys.argv[1]
resultsFilePath = sys.argv[1][:-15]+'_results.csv'
print 'Extracting Phone Reputation results from '+str(iFilePath)

csvReader = csv.reader(open(iFilePath,'rbU'), delimiter=',', quotechar = '"')
csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

rowNum = 0
for row in csvReader:
	#each raw results row will contain the original input file row, followed by the API URL,
	#followed by the JSON response.
	rowNum += 1
	if rowNum == 1:
		csvWriter.writerow(row[:-2]+['Error','Reputation Level','Volume Score','Report Count','Reputation Score','Reputation Type','Reputation Category'])
	else:
		data = {}
		try:
			data = json.loads(row[-1])
		except:
			print 'Error reading JSON on row '+str(rowNum)
			csvWriter.writerow(row[:-2]+['Failed to load JSON results','','','',''])
			continue
		
		error = wppbatchlib.nvl(data.get('error',{}),{}).get('message','')
		repLevel = data.get('reputation_level','')
		repVolume = data.get('volume_score','')
		repReport = data.get('report_count','')
		score = wppbatchlib.nvl(data.get('reputation_details',{}),{}).get('score','')
		type = wppbatchlib.nvl(data.get('reputation_details',{}),{}).get('type','')
		category = wppbatchlib.nvl(data.get('reputation_details',{}),{}).get('category','')
		
		
		resultRow = [error,repLevel,repVolume,repReport,score,type,category]
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
