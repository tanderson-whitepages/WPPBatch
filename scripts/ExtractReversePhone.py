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
print 'Extracting Reverse Phone results from '+str(iFilePath)

csvReader = csv.reader(open(iFilePath,'rbU'), delimiter=',', quotechar = '"')
csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

rowNum = 0
for row in csvReader:
	#each raw results row will contain the original input file row, followed by the API URL,
	#followed by the JSON response.
	rowNum += 1
	
	if rowNum == 1:
		headers = ['Error']
		headers.append('Line Type')
		headers.append('Carrier')
		headers.append('Is Valid')
		headers.append('Is Connected')
		headers.append('Is Prepaid')
		headers.append('Do Not Call Registered')
		headers.append('Reputation Level')
		headers.append('Reputation Details')
		headers.append('Report Count')
		headers.append('Volume Score')
		headers.append('Phone Owner Number')
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
		results = wppbatchlib.nvl(data.get('results',[{}]),[{}])[0]
		inputPhone = results.get('phone_number','')
		lineType = results.get('line_type','')
		carrier = results.get('carrier','')
		isValid = results.get('is_valid','')
		isConnected = results.get('is_connected','')
		isPrepaid = results.get('is_prepaid','')
		dncRegistered = results.get('do_not_call','')
		rep = wppbatchlib.nvl(results.get('reputation',{}),{})
		repLevel = rep.get('level','')
		repVolume = rep.get('volume_score',0)
		repReport = rep.get('report_count',0)
		repDetails = ''
		numDetails = 0
		
		for x in rep.get('details',[]):
			numDetails += 1
			if numDetails > 1:
				repDetails += '|'
			repDetails += x.get('type','')
			repDetails += ';'
			repDetails += x.get('category','')
			repDetails += ';'
			repDetails += str(x.get('score',''))
		
		belongsTo = wppbatchlib.nvl(results.get('belongs_to',[{}]),[{}])
		phoneLocation = wppbatchlib.nvl(results.get('best_location',{}),{})
		
		ownerNum = 0
		for owner in belongsTo:
			ownerNum += 1
			
			personName = wppbatchlib.nvl(owner.get('names',[{}]),[{}])[0]
			firstName = personName.get('first_name','')
			middleName = personName.get('middle_name','')
			lastName = personName.get('last_name','')
			ageRange = str(wppbatchlib.nvl(owner.get('age_range',{}),{}).get('start','?'))
			ageRange +='-'+str(wppbatchlib.nvl(owner.get('age_range',{}),{}).get('end','?'))
			if ageRange == '?-?':
				ageRange = ''
			gender = owner.get('gender','')
			bizName = owner.get('name','')
			
			phoneNumber = ''
			phones = wppbatchlib.nvl(owner.get('phones',[{}]),[{}])
			if phones is not None:
				for p in phones:
					pn = p.get('phone_number','')
					if pn != inputPhone:
						phoneNumber = pn
						break
			
			#if we ran on a caller identification key, then we want to just take the result best_location.
			#however, if we ran a full reverse phone pull and are trying to parse out a result that conforms
			#to caller identification, then we need to override the phone location with the person location,
			#if it exists. 
			locs = owner.get('locations',None)
			if locs is None:
				locs = [phoneLocation]
				
			if locs == []:
				locs = [{}]
			
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
				resultRow.append(lineType)
				resultRow.append(carrier)
				resultRow.append(isValid)
				resultRow.append(isConnected)
				resultRow.append(isPrepaid)
				resultRow.append(dncRegistered)
				resultRow.append(repLevel)
				resultRow.append(repDetails)
				resultRow.append(repReport)
				resultRow.append(repVolume)
				resultRow.append(ownerNum)
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
