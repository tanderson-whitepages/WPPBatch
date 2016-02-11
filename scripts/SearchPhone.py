import sys, re, csv, urllib, wppbatchlib, os

###################################################################################################
#  SEARCH PHONE
#  This script runs Whitepages Pro API reverse phone queries based on an input CSV file.
#  It walks the user through the required input parameters, executes the queries, and
#  writes the raw JSON responses to disk. The user can then pass that result file to
#  one of the Extract*.bat scripts to parse that JSON and generate the final results file.
###################################################################################################

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

try:
	iFilePath = None
	rawResultsFilePath = None

	if sys.argv == None or len(sys.argv) != 2 or len(sys.argv[1]) < 5:
		print 'Drop an input CSV file onto SearchPhone.bat to use this script.'
		var = raw_input("Hit enter to quit")
		quit()
		
	print '--------------------------------------------------'
	print '  Whitepages Pro Batch Script - Search by Phone   '
	print '   Author: '+AUTHOR
	print '   Version '+VERSION
	print '--------------------------------------------------'
	print ''

	apiKey = None
	numThreads = None

	#	READ AND VALIDATE INPUT FILE
	iFilePath = sys.argv[1]
	rawResultsFilePath = sys.argv[1][:-4]+'_rawresults.csv'
	iFileReader = None
	try:
		iFile = open(iFilePath,'rbU')
		iFileReader = csv.reader(iFile, delimiter=',', quotechar = '"')
		headerRow = next(iFileReader)
	except:
		print 'Failed to read input CSV file "'+str(sys.argv[1])+'"'
		var = raw_input("Hit enter to quit")
		quit()
		
	#	SET UP INPUT PARAMETERS 
	inputsFinalized = False
	while inputsFinalized == False:
		#read the ini file if it exists and set default params
		try:
			f = open(os.path.dirname(os.path.realpath(sys.argv[0]))+'/../wppbatch.ini','r')
			content = f.read()
			mApiKey = re.search('.*api.?key\:\s?([a-zA-Z0-9]+)',content)
			if mApiKey:
				apiKey = mApiKey.group(1)
			mThreads = re.search('.*threads\:\s?(\d+)',content)
			if mThreads:
				numThreads = int(mThreads.group(1))
		except:
			print 'Warning: no wppbatch.ini file found'

		#confirm input api key
		if apiKey is not None:
			print 'Paste or type in your API key, or just hit enter to use the default value of'
			print '"'+apiKey+'".'
		else:
			print 'What API key do you want to use to run this test?'
		var = raw_input(">")
		if var != '':
			apiKey = var
		print 'Using apiKey = '+str(apiKey)
		print ''

		#confirm input threads
		if numThreads is not None:
			print 'Type in how many threads to run, or just hit enter to use the default value'
			print '"'+str(numThreads)+'".'
		else:
			print 'How many threads would you like to run?'
		var = raw_input(">")
		if var != '':
			numThreads = int(var)
		print 'Using threads = '+str(numThreads)
		print ''
		
		#now iterate over input parameters for phone searches and map which column from the input file should be submitted.
		inputFields = ['phone','country_hint']
		inputMap = []
		
		print 'We\'re now going to iterate over all of the possible input parameters. '
		print 'For each of them, you will choose which column from your input file '
		print 'you want to submit to that parameter.'
	
		for i in inputFields:
			print ''
			print '"'+i+'" - hit enter to ignore this input, or choose the column to submit to it:'
			for j in range(0,len(headerRow)):
				print '  '+str(j)+') '+headerRow[j]
			var = raw_input('>')
			if var != '':
				inputMap.append([i,int(var)])
				print 'Submitting "'+headerRow[int(var)]+'" values for input parameter "'+i+'"'
			else:
				print 'Ignoring input parameter "'+i+'"'
		
		print ''
		print 'All done. Here is a summary of what you\'re about to search:'
		print 'API key: '+str(apiKey)
		print '# Threads: '+str(numThreads)
		print 'Inputs to submit:'
		for i in inputMap:
			print '  "'+headerRow[i[1]]+'" for "'+i[0]+'"'
		
		print ''
		var = None
		while var != 'y' and var != 'n':
			print 'Is this all correct? y/n'
			var = raw_input(">")
			
		if var == 'y':
			inputsFinalized = True
		else:
			print ''
			print 'Starting over...'
			print ''
	
except:
	print 'An unexpected error occurred building inputs: '+str(sys.exc_info()[0])
	var = raw_input("Hit enter to quit")

try:	
	###################################################################################################
	#	BUILD INPUT LIST
	###################################################################################################

	testInputs = wppbatchlib.inputData()

	numInputs = 0
	doneWithFile = False
	while not doneWithFile:
		iRow = next(iFileReader, 'thisistheend')
		row = [x.decode('utf8') for x in iRow]
		if row != 'thisistheend':
			numInputs += 1
			#build URL
			apiURL = 'http://proapi.whitepages.com/2.1/phone.json?'
			for i in inputMap:
				if len(row[int(i[1])]) > 0:
					apiURL += str(i[0]).lower()+'='+str(urllib.quote(row[int(i[1])]))+'&'
			apiURL += 'api_key='+apiKey
			#add to testInputs
			testInputs.addInput(row,apiURL)
		else:
			doneWithFile = True
		
	if numInputs < numThreads:
		print 'Reducing # threads to '+str(numInputs)+' since this is how many inputs are in the file'
		numThreads = numInputs
		
	###################################################################################################
	#	START EXECUTION
	###################################################################################################
	outFile = open(rawResultsFilePath,'wb')
	csvWriter = csv.writer(outFile,delimiter=',',quotechar='"')
	csvWriter.writerow(headerRow+['APIURL','JSON'])
	threads = []
	#initialize threads
	for i in range(0,numThreads):
		threads.append(wppbatchlib.apiThread(i,csvWriter,testInputs))

	print 'Execution has begun...'
		
	for i in range(0,numThreads):
		threads[i].start()		
		
	for t in threads:
		t.join()
	print 'All done! Raw results written to: '+str(rawResultsFilePath)
	
	outFile.flush()
	outFile.close()
except:
	print 'An unexpected error occurred running inputs: '+str(sys.exc_info()[0])
