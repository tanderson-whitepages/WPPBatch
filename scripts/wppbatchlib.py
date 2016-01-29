import threading, urllib, sys, math, urllib2
from urllib2 import HTTPError
threadLock = threading.Lock()

###################################################################################################
# class inputData
# This class stores the original input rows and apiURLs.
# It provides a method for pulling new inputs, which is used by apiThread
class inputData():
	def __init__(self):
		self.inputs = []
		self.currRow = 0
		self.pctComplete = 0
	
	def addInput(self, row,url):
		self.inputs.append(row+[url])
		
	def fetchInput(self):
		if self.currRow < len(self.inputs):
			row = list(self.inputs[self.currRow])
			self.currRow += 1
			#see if we need to print a new pct complete status
			newPct = math.floor(20*self.currRow/len(self.inputs))*5
			if newPct > self.pctComplete:
				print str(newPct)+'% complete'
				self.pctComplete = newPct
			return row
		else:
			return None

###################################################################################################
# class apiThread
#   This class provides multi-threading support to load API queries in parallel.
#   It handles the tasks of loading API URLs and writing the raw JSON results to disk.
class apiThread(threading.Thread):
	def __init__(self, threadID, csvWriter, inputs):
		try:
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.csvWriter = csvWriter
			self.inputs = inputs
		except:
			log.add("error initializing thread #"+str(threadID))
		
	#This is the main function of the thread, which loops through the following steps:
	# - Pick up new input (synchronously)
	# - Load API URL
	# - Write raw JSON response to disk
	def run(self):
		try:
			done = False
			while not done:
				threadLock.acquire()
				inputRow = self.inputs.fetchInput()
				threadLock.release()
				if inputRow == None:
					done = True
				else:
					#api URL is the last column in the input row
					apiURL = inputRow[-1]
					i = 0
					while i < 3:
						i += 1
						try:
							response = urllib2.urlopen(apiURL, timeout = 5).read().replace('\n','')
							self.csvWriter.writerow(inputRow+[response])
							break
						except HTTPError, e:
							response = e.read().replace('\n','')
							self.csvWriter.writerow(inputRow+[response])
							break
						except:
							print 'Encountered an error loading URL "'+apiURL+'": '+str(sys.exc_info())
					if i == 3:
						self.csvWriter.writerow(inputRow+[''])
		except:
			print 'Thread #'+str(self.threadID)+' encountered an error: '+str(sys.exc_info())

###################################################################################################
# function nvl
# This function just makes life easier when trying to parse JSON data that may or may not be present			
def nvl(var,default):
	if var is None or var == []:
		return default
	return var			
			