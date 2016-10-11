import sys, csv, json, wppbatchlib
csv.field_size_limit(min(2147483647,sys.maxsize))

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

#try:
iFilePath = None
resultsFilePath = None

if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5 or sys.argv[1][-14:] != 'rawresults.csv':
	print 'Drop a CSV file containing raw JSON results onto this program to use it.'
	print '(you need to run SearchAddress.bat first)'
	quit()

iFilePath = sys.argv[1]
resultsFilePath = sys.argv[1][:-15]+'_results.csv'
print 'Extracting Reverse Address results from '+str(iFilePath)

csvReader = csv.reader(open(iFilePath,'rbU'), delimiter=',', quotechar = '"')
csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

rowNum = 0
for row in csvReader:
	#each raw results row will contain the original input file row, followed by the API URL,
	#followed by the JSON response.
	rowNum += 1
	
	if rowNum == 1:
		headers = ['Error']
		headers.append('Result Number')
		headers.append('UUID')
		headers.append('First Name')
		headers.append('Middle Name')
		headers.append('Last Name')
		headers.append('Age Range')
		headers.append('Gender')
		headers.append('Business Name')
		headers.append('Location Is Historical')
		headers.append('Location Type')
		headers.append('Location Valid From')
		headers.append('Location Valid To')
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
					
		if error == '':
			if results == None or len(results[0].keys()) == 0:
				error = 'No results found'
		
		resultNum = 0
		for location in results:
					
			isHistorical = location.get('is_historical','')	
			locType = location.get('type','')
			
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
			
			#fetch occupants
			for occupant in wppbatchlib.nvl(location.get('legal_entities_at',[{}]),[{}]):
				resultNum += 1
					
				id = occupant.get('id',{}).get('key','')	
				personName = wppbatchlib.nvl(occupant.get('names',[{}]),[{}])[0]
				firstName = personName.get('first_name','')
				middleName = personName.get('middle_name','')
				lastName = personName.get('last_name','')
				ageRange = str(wppbatchlib.nvl(occupant.get('age_range',{}),{}).get('start','?'))
				ageRange +='-'+str(wppbatchlib.nvl(occupant.get('age_range',{}),{}).get('end','?'))
				if ageRange == '?-?':
					ageRange = ''
				gender = occupant.get('gender','')
				
				bizName = occupant.get('name','')
				
				start = wppbatchlib.nvl(wppbatchlib.nvl(occupant.get('valid_for',{}),{}).get('start',{}),{})
				end = wppbatchlib.nvl(wppbatchlib.nvl(occupant.get('valid_for',{}),{}).get('stop',{}),{})
				validFrom = str(start.get('year',''))+'-'+str(start.get('month',''))+'-'+str(start.get('day',''))
				validTo = str(end.get('year',''))+'-'+str(end.get('month',''))+'-'+str(end.get('day',''))	
				
				phoneNumber = ''
				phones = wppbatchlib.nvl(occupant.get('phones',[{}]),[{}])
				if phones is not None:
					for p in phones:
						phoneNumber = p.get('phone_number','')
						break
			
				resultRow = [error]
				resultRow.append(resultNum)
				resultRow.append(id)
				resultRow.append(firstName)
				resultRow.append(middleName)
				resultRow.append(lastName)
				resultRow.append(ageRange)
				resultRow.append(gender)
				resultRow.append(bizName)
				resultRow.append(isHistorical)
				resultRow.append(locType)
				resultRow.append(validFrom)
				resultRow.append(validTo)
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
	
#except:
#	print 'An unknown error occurred: '+str(sys.exc_info()[0])