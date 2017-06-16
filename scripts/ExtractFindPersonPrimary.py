import sys, csv, json, wppbatchlib
csv.field_size_limit(min(2147483647,sys.maxsize))

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'


iFilePath = None
resultsFilePath = None

if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5 or sys.argv[1][-14:] != 'rawresults.csv':
	print 'Drop a CSV file containing raw JSON results onto this program to use it.'
	print '(you need to run SearchPerson.bat first)'
	var = raw_input("Hit enter to quit")
	quit()

iFilePath = sys.argv[1]
resultsFilePath = sys.argv[1][:-15]+'_results.csv'
print 'Extracting Find Person results from '+str(iFilePath)

csvReader = csv.reader(open(iFilePath,'rbU'), delimiter=',', quotechar = '"')
csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

rowNum = 0
for row in csvReader:
	#each raw results row will contain the original input file row, followed by the API URL,
	#followed by the JSON response.
	rowNum += 1
	
	if rowNum == 1:
		headers = ['Error']
		headers.append('First Name')
		headers.append('Middle Name')
		headers.append('Last Name')
		headers.append('Age Range')
		headers.append('Gender')
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
		results = wppbatchlib.nvl(data.get('person',[{}]),[{}])
					
							
		if error == '' and len(results[0].keys()) == 0:
			error = 'No results found'
		
		resultNum = 0
		for primaryPerson in results:
			primaryPersonKey = primaryPerson.get('person',{}).get('id')
			resultNum += 1
			
			
			locs = primaryPerson.get('current_addresses',[{}])
			bestIndex = 0
			
			for locIndex in range (0,len(locs)):
				isHistorical = locs[locIndex].get('is_historical','')	
				if isHistorical == False:
					bestIndex = locIndex
					break
			
			if len(locs) > 0:
				locs = [locs[bestIndex]]
			else:
				csvWriter.writerow(row[:-2]+['No location found',resultNum,'','',''])
			
			#fetches current address for the searched individual
			for location in locs:
				
				locType = location.get('location_type','')
				validFrom = location.get('link_to_person_start_date','')
				validTo = location.get('link_to_person_end_date','')

				
				street = location.get('street_line_1','')
				city = location.get('city','')
				state = location.get('state_code','')
				postalCode = location.get('postal_code','')
				zip4 = location.get('zip4','')
				country = location.get('country_code','')
				deliveryPoint = location.get('delivery_point','')
				isActive = location.get('is_active','')
				
				latLonAccuracy = wppbatchlib.nvl(location.get('lat_long',{}),{}).get('accuracy','')
				latitude = wppbatchlib.nvl(location.get('lat_long',{}),{}).get('latitude','')
				longitude = wppbatchlib.nvl(location.get('lat_long',{}),{}).get('longitude','')
				
				#person data
				for person in results:

					firstName = person.get('firstname','')
					middleName = person.get('middlename','')
					lastName = person.get('lastname','')
					ageRange = person.get('age_range','')
					gender = person.get('gender','')
					
					phoneNumber = ''
					phones = wppbatchlib.nvl(primaryPerson.get('phones',[{}]),[{}])
					if phones is not None:
						for p in phones:
							phoneNumber = p.get('phone_number','')
							break
				
					resultRow = [error]
					resultRow.append(firstName)
					resultRow.append(middleName)
					resultRow.append(lastName)
					resultRow.append(ageRange)
					resultRow.append(gender)
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
					resultRow.append(isActive)
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
	