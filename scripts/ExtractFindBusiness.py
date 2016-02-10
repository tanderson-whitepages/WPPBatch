import sys, csv, json, wppbatchlib
csv.field_size_limit(min(2147483647,sys.maxsize))

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

try:
	iFilePath = None
	resultsFilePath = None

	if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5 or sys.argv[1][-14:] != 'rawresults.csv':
		print 'Drop a CSV file containing raw JSON results onto this program to use it.'
		print '(you need to run SearchPerson.bat first)'
		var = raw_input("Hit enter to quit")
		quit()

	iFilePath = sys.argv[1]
	resultsFilePath = sys.argv[1][:-15]+'_results.csv'
	print 'Extracting Find Business results from '+str(iFilePath)

	csvReader = csv.reader(open(iFilePath,'rb'), delimiter=',', quotechar = '"')
	csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

	rowNum = 0
	for row in csvReader:
		#each raw results row will contain the original input file row, followed by the API URL,
		#followed by the JSON response.
		rowNum += 1
		
		if rowNum == 1:
			headers = ['Error']
			headers.append('Result Number')
			headers.append('Business Name')
			headers.append('Location Type')
			headers.append('Street')
			headers.append('City')
			headers.append('State')
			headers.append('Postal Code')
			headers.append('Zip+4')
			headers.append('Country')
			headers.append('Location Delivery Point')
			headers.append('Location Usage Type')
			headers.append('Location Receiving Mail')
			headers.append('Location LatLon Accuracy')
			headers.append('Location Latitude')
			headers.append('Location Longitude')
			headers.append('Landline Phone')
			csvWriter.writerow(row[:-2]+headers)
		else:
			data = {}
			try:
				data = json.loads(row[-1])
			except:
				print 'Error reading JSON on row '+str(rowNum)
				csvWriter.writerow(row[:-2]+['Failed to load JSON results','','','',''])
				continue
			
			error = wppbatchlib.nvl(data.get('error',{}),{}).get('message','')
			results = wppbatchlib.nvl(data.get('results',[{}]),[{}])
						
			if len(results[0].keys()) == 0:
				error = 'No results found'
			
			resultNum = 0
			for result in results:
				resultNum += 1
				
				bizName = result.get('name','')
				
				phoneNumber = ''
				phones = wppbatchlib.nvl(result.get('phones',[{}]),[{}])
				if phones is not None:
					for p in phones:
						phoneNumber = p.get('phone_number','')
						break
				
				locs = result.get('locations',[{}])				
				for location in locs:
						
					isHistorical = location.get('is_historical','')	
					locType = location.get('type','')
					start = wppbatchlib.nvl(wppbatchlib.nvl(location.get('valid_for',{}),{}).get('start',{}),{})
					end = wppbatchlib.nvl(wppbatchlib.nvl(location.get('valid_for',{}),{}).get('stop',{}),{})
					validFrom = str(start.get('year',''))+'-'+str(start.get('month',''))+'-'+str(start.get('day',''))
					validTo = str(end.get('year',''))+'-'+str(end.get('month',''))+'-'+str(end.get('day',''))	
					
					street = location.get('standard_address_line1','')
					city = location.get('city','')
					state = location.get('state_code','')
					postalCode = location.get('postal_code','')
					zip4 = location.get('zip4','')
					country = location.get('country_code','')
					deliveryPoint = location.get('delivery_point','')
					usageType = location.get('usage','')
					rcvMail = location.get('is_receiving_mail','')
					
					latLonAccuracy = wppbatchlib.nvl(location.get('lat_long',{}),{}).get('accuracy','')
					latitude = wppbatchlib.nvl(location.get('lat_long',{}),{}).get('latitude','')
					longitude = wppbatchlib.nvl(location.get('lat_long',{}),{}).get('longitude','')
					
					resultRow = [error]
					resultRow.append(resultNum)
					resultRow.append(bizName)
					resultRow.append(locType)
					resultRow.append(street)
					resultRow.append(city)
					resultRow.append(state)
					resultRow.append(postalCode)
					resultRow.append(zip4)
					resultRow.append(country)
					resultRow.append(deliveryPoint)
					resultRow.append(usageType)
					resultRow.append(rcvMail)
					resultRow.append(latLonAccuracy)
					resultRow.append(latitude)
					resultRow.append(longitude)
					resultRow.append(phoneNumber)
					
					csvWriter.writerow(row[:-2]+resultRow)

	print 'All done!'
	print 'You can find your results file here: '+str(resultsFilePath)
	print ''
	
except:
	print 'An unknown error occurred: '+str(sys.exc_info()[0])