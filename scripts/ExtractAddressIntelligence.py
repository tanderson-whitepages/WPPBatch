import sys, csv, json, wppbatchlib
csv.field_size_limit(min(2147483647,sys.maxsize))

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

iFilePath = None
resultsFilePath = None

if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5 or sys.argv[1][-14:] != 'rawresults.csv':
	print 'Drop a CSV file containing raw JSON results onto this program to use it.'
	print '(you need to run SearchAddressIntelligence.bat first)'
	var = raw_input("Hit enter to quit")
	quit()

iFilePath = sys.argv[1]
resultsFilePath = sys.argv[1][:-15]+'_results.csv'
print 'Extracting Address Intelligence results from '+str(iFilePath)

csvReader = csv.reader(open(iFilePath,'rbU'), delimiter=',', quotechar = '"')
csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

rowNum = 0
for row in csvReader:
	#each raw results row will contain the original input file row, followed by the API URL,
	#followed by the JSON response.
	rowNum += 1
	if rowNum == 1:
		csvWriter.writerow(row[:-2]+['Error','ID','is_valid','street_line_1','street_line_2','city','state_code','postal_code','zip4','country_code','latitude','longitude','latlon precision','diagnostics'])
	else:
		data = {}
		try:
			data = json.loads(row[-1])
		except:
			print 'Error reading JSON on row '+str(rowNum)
			csvWriter.writerow(row[:-2]+['Failed to load JSON results','','','',''])
			continue
		
		error = wppbatchlib.nvl(data.get('error',{}),{}).get('message','')
		id = data.get('id','')
		isvalid = data.get('is_valid','')
		line1 = data.get('street_line_1','')
		line2 = data.get('street_line_2','')
		city = data.get('city','')
		state = data.get('state_code','')
		zip = data.get('postal_code','')
		zip4 = data.get('zip4','')
		country = data.get('country_code','')
		lat = wppbatchlib.nvl(data.get('lat_long',{}),{}).get('latitude','')
		lon = wppbatchlib.nvl(data.get('lat_long',{}),{}).get('longitude','')
		latlonacc = wppbatchlib.nvl(data.get('lat_long',{}),{}).get('accuracy','')
		diagnostic = wppbatchlib.nvl(data.get('diagnostics',['']),[''])[0]
		
		resultRow = [error,id,isvalid,line1,line2,city,state,zip,zip4,country,lat,lon,latlonacc,diagnostic]
		
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
