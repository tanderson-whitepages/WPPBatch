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
		headers.append('Is Prepaid')
		headers.append('Is Commercial')
		headers.append('Result Number')
		headers.append('Result Type')
		headers.append('Name')
		headers.append('Age Range')
		headers.append('Gender')
		headers.append('Street')
		headers.append('City')
		headers.append('State')
		headers.append('Postal Code')
		headers.append('Zip+4')
		headers.append('Country')
		headers.append('Location Delivery Point')
		headers.append('Location Is Active')
		headers.append('Location LatLon Accuracy')
		headers.append('Location Latitude')
		headers.append('Location Longitude')
		csvWriter.writerow(row[:-2]+headers)
	else:
		data = {}
		try:
			data = json.loads(row[-1])
		except:
			print 'Error reading JSON on row '+str(rowNum)
			csvWriter.writerow(row[:-2]+['Failed to load JSON results','','','',''])
			continue
		
		resultNum = 0
		
		error = wppbatchlib.nvl(data.get('error',{}),{}).get('message','')
		inputPhone = data.get('phone_number','')
		lineType = data.get('line_type','')
		carrier = data.get('carrier','')
		isValid = data.get('is_valid','')
		isPrepaid = data.get('is_prepaid','')
		isCommercial = data.get('is_commercial','')
				
		belongsTo = wppbatchlib.nvl(data.get('belongs_to',[{}]),[{}])
		currAddresses = wppbatchlib.nvl(data.get('current_addresses',[{}]),[{}])
		associatedPeople = wppbatchlib.nvl(data.get('associated_people',[]),[])
		
		for owner in belongsTo:
	
			name = wppbatchlib.nvl(owner.get('name',''),'')
			ageRange = wppbatchlib.nvl(owner.get('age_range',''),'')
			gender = owner.get('gender','')
			
			for location in currAddresses:
								
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
						
				resultNum += 1
				resultRow = [error]
				resultRow.append(lineType)
				resultRow.append(carrier)
				resultRow.append(isValid)
				resultRow.append(isPrepaid)
				resultRow.append(isCommercial)
				resultRow.append(resultNum)
				resultRow.append('Owner')
				resultRow.append(name)
				resultRow.append(ageRange)
				resultRow.append(gender)
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
					
		for person in associatedPeople:
	
			name = wppbatchlib.nvl(person.get('name',''),'')
			ageRange = wppbatchlib.nvl(person.get('age_range',''),'')
			gender = person.get('gender','')
			
			for location in currAddresses:
								
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
						
				resultNum += 1
				resultRow = [error]
				resultRow.append(lineType)
				resultRow.append(carrier)
				resultRow.append(isValid)
				resultRow.append(isPrepaid)
				resultRow.append(isCommercial)
				resultRow.append(resultNum)
				resultRow.append('Household')
				resultRow.append(name)
				resultRow.append(ageRange)
				resultRow.append(gender)
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
