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
		headers.append('Owner')
		headers.append('Name')
	#	headers.append('Last Name')
		headers.append('Age Range')
		headers.append('Gender')
		headers.append('Location Valid From')
	#	headers.append('Location Valid To')
		headers.append('Street')
		headers.append('City')
		headers.append('State')
		headers.append('Postal Code')
		headers.append('Zip+4')
		headers.append('Country')
		headers.append('Location Delivery Point')
		headers.append('Location is Commercial')
		headers.append('Location is Forwarder')
		headers.append('Location Last Sale Date')
		headers.append('Location Total Value')
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
		
		error = data.get('error',{})
						
		isHistorical = data.get('is_historical','')	
		
		street = data.get('street_line_1','')
		city = data.get('city','')
		state = data.get('state_code','')
		postalCode = data.get('postal_code','')
		zip4 = data.get('zip4','')
		country = data.get('country_code','')
		deliveryPoint = data.get('delivery_point','')
		isCommercial = data.get('is_commercial','')
		rcvMail = data.get('is_active','')
		isForwarder = data.get('is_forwarder','')
		lastSaleDate = data.get('last_sale_date','')
		totalValue = '$' + str(data.get('total_value',''))
		
		latLonAccuracy = wppbatchlib.nvl(data.get('lat_long',{}),{}).get('accuracy','')
		latitude = wppbatchlib.nvl(data.get('lat_long',{}),{}).get('latitude','')
		longitude = wppbatchlib.nvl(data.get('lat_long',{}),{}).get('longitude','')
		owner = ""
		#fetch owners
		for owners in wppbatchlib.nvl(data.get('owners',[{}]),[{}]):
			
			owner += str(owners.get('name')) + '; '
			decodedRow = []
			
		#fetch occupants
		for occupant in wppbatchlib.nvl(data.get('current_residents',[{}]),[{}]):
	

			firstName = occupant.get('firstname','')
			middleName = occupant.get('middlename','')
			lastName = occupant.get('lastname','')
			ageRange = occupant.get('age_range','')
			gender = occupant.get('gender','')
			bizName = occupant.get('name','')

			validFrom = occupant.get('link_to_address_start_date','')
		#	validTo = str(end.get('year',''))+'-'+str(end.get('month',''))+'-'+str(end.get('day',''))	
			
			phoneNumber = ''
			phones = wppbatchlib.nvl(occupant.get('phones',[{}]),[{}])
			if phones is not None:
				for p in phones:
					phoneNumber = p.get('phone_number','')
					break
		
			resultRow = [error]
			resultRow.append(owner)
			resultRow.append(bizName)
		##	resultRow.append(firstName)
		##	resultRow.append(middleName)
		##	resultRow.append(lastName)
			resultRow.append(ageRange)
			resultRow.append(gender)
		##	resultRow.append(bizName)
			resultRow.append(validFrom)
		##	resultRow.append(validTo)
			resultRow.append(street)
			resultRow.append(city)
			resultRow.append(state)
			resultRow.append(postalCode)
			resultRow.append(zip4)
			resultRow.append(country)
			resultRow.append(deliveryPoint)
			resultRow.append(isCommercial)
			resultRow.append(isForwarder)
			resultRow.append(lastSaleDate)
			resultRow.append(totalValue)
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