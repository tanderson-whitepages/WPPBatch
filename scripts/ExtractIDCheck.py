import sys, csv, json, wppbatchlib

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

try:
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
	
	csvReader = csv.reader(open(iFilePath,'rb'), delimiter=',', quotechar = '"')
	csvWriter = csv.writer(open(resultsFilePath,'wb'),delimiter=',',quotechar='"')

	headerRow = []
	headerRow.append("Billing Name Warning")
	headerRow.append("Billing Name Matches Celebrity")
	headerRow.append("Billing Name Is Garbled")
	headerRow.append("Billing Phone Warning")
	headerRow.append("Billing Phone to Name")
	headerRow.append("Billing Phone to Address")
	headerRow.append("Billing Phone Subscriber Name")
	headerRow.append("Billing Phone Country Code")
	headerRow.append("Billing Phone Line Type")
	headerRow.append("Billing Phone Carrier")
	headerRow.append("Billing Phone Is Prepaid")
	headerRow.append("Billing Phone Is Connected")
	headerRow.append("Billing Phone on DNC")
	headerRow.append("Billing Phone Is Commercial")
	headerRow.append("Billing Address Warning")
	headerRow.append("Billing Address to Name")
	headerRow.append("Billing Address Resident Name")
	headerRow.append("Billing Address Type")
	headerRow.append("Billing Address Is Active")
	headerRow.append("Billing Address Is Commercial")
	headerRow.append("Shipping Name Warning")
	headerRow.append("Shipping Name Matches Celebrity")
	headerRow.append("Shipping Name Is Garbled")
	headerRow.append("Shipping Phone Warning")
	headerRow.append("Shipping Phone to Name")
	headerRow.append("Shipping Phone to Address")
	headerRow.append("Shipping Phone Subscriber Name")
	headerRow.append("Shipping Phone Country Code")
	headerRow.append("Shipping Phone Line Type")
	headerRow.append("Shipping Phone Carrier")
	headerRow.append("Shipping Phone Is Prepaid")
	headerRow.append("Shipping Phone Is Connected")
	headerRow.append("Shipping Phone on DNC")
	headerRow.append("Shipping Phone Is Commercial")
	headerRow.append("Shipping Address Warning")
	headerRow.append("Shipping Address to Name")
	headerRow.append("Shipping Address Resident Name")
	headerRow.append("Shipping Address Type")
	headerRow.append("Shipping Address Is Active")
	headerRow.append("Shipping Address Is Commercial")
	headerRow.append("Email Warning")
	headerRow.append("Email Is Valid")
	headerRow.append("Email Is Valid Details")
	headerRow.append("Email Is Disposable")
	headerRow.append("Email Is Auto-Generated")
	headerRow.append("Email to Name")
	headerRow.append("Email Registered Name")
	headerRow.append("Email First Seen Date")
	headerRow.append("Email First Seen Days")
	headerRow.append("Email Domain Creation Date")
	headerRow.append("Email Domain Creation Days")
	headerRow.append("IP Warning")
	headerRow.append("IP Distance From Address")
	headerRow.append("IP Geolocation")
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
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_name_checks',{}),{}).get('warnings',['']),[''])[0])
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_name_checks',{}),{}).get('celebrity_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_name_checks',{}),{}).get('fake_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('warnings',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('phone_to_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('phone_to_address',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('subscriber_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('country_code',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('line_type',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('carrier',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('is_prepaid',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('is_connected',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('is_do_not_call_registered',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_phone_checks',{}),{}).get('is_commercial',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_address_checks',{}),{}).get('warnings',['']),[''])[0])
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_address_checks',{}),{}).get('address_to_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_address_checks',{}),{}).get('resident_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_address_checks',{}),{}).get('type',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_address_checks',{}),{}).get('is_active',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('billing_address_checks',{}),{}).get('is_commercial',''),''))
			
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_name_checks',{}),{}).get('warnings',['']),[''])[0])
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_name_checks',{}),{}).get('celebrity_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_name_checks',{}),{}).get('fake_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('warnings',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('phone_to_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('phone_to_address',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('subscriber_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('country_code',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('line_type',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('carrier',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('is_prepaid',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('is_connected',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('is_do_not_call_registered',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_phone_checks',{}),{}).get('is_commercial',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_address_checks',{}),{}).get('warnings',['']),[''])[0])
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_address_checks',{}),{}).get('address_to_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_address_checks',{}),{}).get('resident_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_address_checks',{}),{}).get('type',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_address_checks',{}),{}).get('is_active',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('shipping_address_checks',{}),{}).get('is_commercial',''),''))
			
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('warnings',['']),[''])[0])
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('is_valid',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('is_valid_diagnostic_message',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('is_disposable',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('is_autogenerated',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('email_to_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('registered_name',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('email_first_seen_date',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('email_first_seen_days',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('email_domain_creation_date',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('email_address_checks',{}),{}).get('email_domain_creation_days',''),''))
			
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('warnings',['']),[''])[0])
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('distance_from_address',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('geolocation',''),''))
			resultRow.append(wppbatchlib.nvl(wppbatchlib.nvl(data.get('ip_address_checks',{}),{}).get('is_proxy',''),''))
			csvWriter.writerow(row[:-2]+resultRow)
	
	print 'All done!'
	print 'You can find your results file here: '+str(resultsFilePath)
	print ''
	var = raw_input("Hit enter to quit")
	quit()
except:
	print 'An unknown error occurred: '+str(sys.exc_info()[0])