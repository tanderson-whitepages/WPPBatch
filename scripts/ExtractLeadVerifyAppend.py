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

csvReader = csv.reader(open(iFilePath,'rbU'), delimiter=',', quotechar = '"')
csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

headerRow = []
headerRow.append("Error")
headerRow.append("Name Warning")
headerRow.append("Name Matches Celebrity")
headerRow.append("Name Is Garbled")
headerRow.append("Phone Contact Score")
headerRow.append("Phone Is Valid")
headerRow.append("Phone Warning")
headerRow.append("Phone to Name")
headerRow.append("Phone Subscriber Name")
headerRow.append("Phone Country Code")
headerRow.append("Phone Line Type")
headerRow.append("Phone Carrier")
headerRow.append("Phone Is Prepaid")
headerRow.append("Phone Is Connected")
headerRow.append("Phone on DNC")
headerRow.append("Phone Is Commercial")
headerRow.append("Phone Address Line 1")
headerRow.append("Phone Address Line 2")
headerRow.append("Phone Address City")
headerRow.append("Phone Address State")
headerRow.append("Phone Address Postal Code")
headerRow.append("Phone Address Country")
headerRow.append("Phone Subscriber Age Range")
headerRow.append("Phone Subscriber Gender")
headerRow.append("Address Contact Score")
headerRow.append("Address Is Valid")
headerRow.append("Address Warning")
headerRow.append("Address to Name")
headerRow.append("Address Resident Name")
headerRow.append("Address Resident Age Range")
headerRow.append("Address Resident Gender")
headerRow.append("Address Type")
headerRow.append("Address Is Active")
headerRow.append("Address Is Commercial")
headerRow.append("Email Contact Score")
headerRow.append("Email Warning")
headerRow.append("Email Error")
headerRow.append("Email Is Valid")
headerRow.append("Email Is Valid Details")
headerRow.append("Email Is Disposable")
headerRow.append("Email Is Auto-Generated")
headerRow.append("Email to Name")
headerRow.append("Email Registered Name")
headerRow.append("IP Warning")
headerRow.append("IP Location Postal Code")
headerRow.append("IP Location City")
headerRow.append("IP Location Country")
headerRow.append("IP Location Continent")
headerRow.append("IP Distance")
headerRow.append("IP Is Proxy")

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
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('name_checks',{}),{}).get('warnings',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('name_checks',{}),{}).get('celebrity_name',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('name_checks',{}),{}).get('fake_name',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('phone_contact_score',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('is_valid',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('warnings',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('phone_to_name',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_name',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('country_code',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('line_type',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('carrier',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('is_prepaid',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('is_connected',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('is_do_not_call_registered',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('is_commercial',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_address',{}),{}).get('street_line_1',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_address',{}),{}).get('street_line_2',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_address',{}),{}).get('city',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_address',{}),{}).get('state_code',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_address',{}),{}).get('postal_code',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_address',{}),{}).get('country_code',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_age_range',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('phone_checks',{}),{}).get('subscriber_gender',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('address_contact_score',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('is_valid',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('warnings',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('address_to_name',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('resident_name',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('resident_age_range',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('resident_gender',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('type',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('is_active',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('address_checks',{}),{}).get('is_commercial',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('email_contact_score',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('warnings',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('error',{}),{}).get('message'))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('is_valid',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('diagnostics',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('is_disposable',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('is_autogenerated',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('email_to_name',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('registered_name',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('warnings',['']),[''])[0])
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('geolocation',{}),{}).get('postal_code',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('geolocation',{}),{}).get('city_name',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('geolocation',{}),{}).get('country_name',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('geolocation',{}),{}).get('continent_code',''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('distance_from_address',''),''))
		resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('is_proxy',''),''))
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
