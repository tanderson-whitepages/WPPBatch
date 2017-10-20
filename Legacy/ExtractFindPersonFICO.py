import sys, csv, json, wppbatchlib, time
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
resultsFilePath = sys.argv[1][:-15]+'_WhitepagesStamp_'+time.strftime('%Y%m%d')+'.csv'
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
		headers.append('Matching Persons Found')
		headers.append('Link Type')
		headers.append('Person First Name')
		headers.append('Person Middle Name')
		headers.append('Person Last Name')
		headers.append('Age Range')
		headers.append('Street')
		headers.append('City')
		headers.append('State')
		headers.append('Postal Code')
		headers.append('Zip+4')
		headers.append('Country')
		headers.append('Location Latitude')
		headers.append('Location Longitude')
		headers.append('Geoprecision')
		headers.append('Address Type')
		headers.append('Delivery Point')
		headers.append('Receiving Mail')
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
					
							
		if error == '' and len(results[0].keys()) == 0:
			error = 'No results found'
		
		resultNum = 0
		totalResults = len(results)
		for primaryPerson in results:
			primaryPersonKey = primaryPerson.get('id',{}).get('key')
			resultNum += 1
			
			locs = primaryPerson.get('locations',[{}])
			
			for location in locs:
				
				start = wppbatchlib.nvl(wppbatchlib.nvl(location.get('valid_for',{}),{}).get('start',{}),{})
				end = wppbatchlib.nvl(wppbatchlib.nvl(location.get('valid_for',{}),{}).get('stop',{}),{})
				linkType = ''
				if location.get('is_historical','') == False:
					linkType = 'current'
				else:
					linkType = str(start.get('year',''))+'-'+str(end.get('year',''))
				
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
				
				#fetch household members
				for person in location.get('legal_entities_at',[{}]):
					personKey = person.get('id',{}).get('key')
					if personKey == primaryPersonKey:
						personType = 'Primary'
					else:
						personType = 'Household'
						
					personName = wppbatchlib.nvl(person.get('names',[{}]),[{}])[0]
					firstName = personName.get('first_name','')
					middleName = personName.get('middle_name','')
					lastName = personName.get('last_name','')
					ageRange = str(wppbatchlib.nvl(person.get('age_range',{}),{}).get('start','?'))
					ageRange +='-'+str(wppbatchlib.nvl(person.get('age_range',{}),{}).get('end','?'))
					if ageRange == '?-?':
						ageRange = ''
					gender = person.get('gender','')
					
					phoneNumber = ''
					phones = wppbatchlib.nvl(person.get('phones',[{}]),[{}])
					#get phones from top level results if this is the primary
					if personKey == primaryPersonKey:
						phones = wppbatchlib.nvl(primaryPerson.get('phones',[{}]),[{}])
					if phones is not None:
						for p in phones:
							phoneNumber = p.get('phone_number','')
							break
				
					resultRow = [error]
					resultRow.append(totalResults)
					resultRow.append(linkType)
					resultRow.append(firstName)
					resultRow.append(middleName)
					resultRow.append(lastName)
					resultRow.append(ageRange)
					resultRow.append(street)
					resultRow.append(city)
					resultRow.append(state)
					resultRow.append(postalCode)
					resultRow.append(zip4)
					resultRow.append(country)
					resultRow.append(latitude)
					resultRow.append(longitude)
					resultRow.append(latLonAccuracy)
					resultRow.append(usageType)
					resultRow.append(deliveryPoint)
					resultRow.append(rcvMail)
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
	
