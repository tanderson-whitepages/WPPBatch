import sys, re, csv, urllib, wppbatchlib, os, codecs

###################################################################################################
#  SEARCH PERSON
#  This script runs Whitepages Pro API find person queries based on an input CSV file.
#  It walks the user through the required input parameters, executes the queries, and
#  writes the raw JSON responses to disk. The user can then pass that result file to
#  ExtractPerson.bat to parse that JSON and generate the final results file.
###################################################################################################

VERSION = '0.1'
AUTHOR = 'Trevor Anderson <tanderson@whitepages.com>'

predefinedInputs = []
inputIndex = 0

print sys.argv

def getInput():
	global inputIndex
	if inputIndex < len(predefinedInputs):
		inputIndex += 1
		return predefinedInputs[inputIndex-1]
	else:
		return raw_input(">")

try:
	iFilePath = None
	rawResultsFilePath = None
	apiHost = 'proapi.whitepages.com'

	if sys.argv == None or len(sys.argv) < 2 or len(sys.argv[1]) < 5:
		print 'Drop an input CSV file onto SearchPhone.bat to use this script.'
		var = raw_input("Hit enter to quit")
		quit()
		
	if len(sys.argv) == 3:
		predefinedInputs = sys.argv[2].split(';')
		
	print '--------------------------------------------------'
	print '  Whitepages Pro Batch Script - Find Person   '
	print '   Author: '+AUTHOR
	print '   Version '+VERSION
	print '--------------------------------------------------'
	print ''

	apiKey = None
	numThreads = None
	useMetro = False
	useHistoric = False

	#	READ AND VALIDATE INPUT FILE
	iFilePath = sys.argv[1]
	rawResultsFilePath = sys.argv[1][:-4]+'_rawresults.csv'
	iFileReader = None
	iData = None
	try:
		iData = codecs.open(iFilePath, "r",encoding='ascii', errors='ignore')
		iFileReader = csv.reader(iData, delimiter=',', quotechar = '"')
		headerRow = next(iFileReader)
	except:
		print 'Failed to read input CSV file "'+str(sys.argv[1])+'"'
		var = raw_input("Hit enter to quit")
		quit()
		
	print 'foo'
	#	SET UP INPUT PARAMETERS 
	inputsFinalized = False
	while inputsFinalized == False:
		#read the ini file if it exists and set default params
		try:
			f = open(os.path.dirname(os.path.realpath(sys.argv[0]))+'/../wppbatch.ini','r')
			content = f.read()
			mApiKey = re.search('.*api.?key\:\\s?([a-zA-Z0-9]+)',content)
			if mApiKey:
				apiKey = mApiKey.group(1)
			mThreads = re.search('.*threads\:\\s?(\\d+)',content)
			if mThreads:
				numThreads = int(mThreads.group(1))
			mMetro = re.search('.*searchperson\.metro\:\\s?(\\w+)',content)
			if mMetro:
				if mMetro.group(1).lower() == 'true':
					useMetro = True
			mHistoric = re.search('.*searchperson\.historical\:\\s?(\\w+)',content)
			if mHistoric:
				if mHistoric.group(1).lower() == 'true':
					useHistoric = True
			mHost = re.search('.*host\:\\s?([^\\s]+)',content)
			if mHost:
				apiHost = mHost.group(1)
		except:
			print 'Warning: no wppbatch.ini file found'

		#confirm api host
		print 'Paste or type in the API host, or just hit enter to use the default value of'
		print '"'+apiHost+'".'
		var = getInput()
		if var != '':
			apiHost = var
		print 'Using API host = '+str(apiHost)
		print ''
		
		#confirm input api key
		if apiKey is not None:
			print 'Paste or type in your API key, or just hit enter to use the default value of'
			print '"'+apiKey+'".'
		else:
			print 'What API key do you want to use to run this test?'
		var = getInput()
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
		var = getInput()
		if var != '':
			numThreads = int(var)
		print 'Using threads = '+str(numThreads)
		print ''
		
		#confirm whether to use metro
		if useMetro is not None:
			print 'Would you like to use metro area expansion? Enter y/n or just hit enter to use'
			print 'the default value of '+str(useMetro)+'.'
		else:
			print 'Would you like to use metro area expansion? y/n'
		var = getInput()
		if var != '':
			if var == 'y':
				useMetro = True
			else:
				useMetro = False
		print 'Using metro = '+str(useMetro)
		print ''
		
		#confirm whether to use historical
		if useHistoric is not None:
			print 'Would you like to use historical search? Enter y/n or just hit enter to use'
			print 'the default value of '+str(useHistoric)+'.'
		else:
			print 'Would you like to use historical search? y/n'
		var = getInput()
		if var != '':
			if var == 'y':
				useHistoric = True
			else:
				useHistoric = False
		print 'Using historical = '+str(useHistoric)
		print ''
		#now iterate over input parameters for phone searches and map which column from the input file should be submitted.
		inputFields = ['name','first_name','last_name','street_line_1','city','state_code','postal_code']
		inputMap = []
		
		print 'We\'re now going to iterate over all of the possible input parameters. '
		print 'For each of them, you will choose which column from your input file '
		print 'you want to submit to that parameter.'
	
		for i in inputFields:
			print ''
			print '"'+i+'" - hit enter to ignore this input, or choose the column to submit to it:'
			for j in range(0,len(headerRow)):
				print '  '+str(j)+') '+headerRow[j]
			var = getInput()
			if var != '':
				inputMap.append([i,int(var)])
				print 'Submitting "'+headerRow[int(var)]+'" values for input parameter "'+i+'"'
			else:
				print 'Ignoring input parameter "'+i+'"'
		
		print ''
		print 'All done. Here is a summary of what you\'re about to search:'
		print 'API host: '+apiHost
		print 'API key: '+str(apiKey)
		print '# Threads: '+str(numThreads)
		print 'Use Metro: '+str(useMetro)
		print 'Use Historical: '+str(useHistoric)
		print 'Inputs to submit:'
		for i in inputMap:
			print '  "'+headerRow[i[1]]+'" for "'+i[0]+'"'
		
		print ''
		var = None
		while var != 'y' and var != 'n':
			print 'Is this all correct? y/n'
			var = getInput()
			
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
		row = next(iFileReader, 'thisistheend')
		if row != 'thisistheend':
			numInputs += 1
			#build URL
			apiURL = 'http://'+apiHost+'/2.1/person.json?'
			for i in inputMap:
				if len(row[int(i[1])]) > 0:
					apiURL += str(i[0]).lower()+'='+str(urllib.quote(row[int(i[1])]))+'&'
			
			if useMetro:
				apiURL += 'use_metro=true&'
			if useHistoric:
				apiURL += 'use_historical=true&'
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
