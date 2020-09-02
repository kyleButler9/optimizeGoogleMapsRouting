import googlemaps
from datetime import datetime
from datetime import timedelta
import csv
import numpy as np
from string import ascii_lowercase

class googleAPI:
	def __init__(self,keyFile,addressesCSV):
		self.unlockGoogleAPI(keyFile)
		self.addresses = []
		self.locations = []
		self.latLongs = []
		self.departureTimes = []
		self.stayDuration = []
		self.readCSV(addressesCSV)
		self.geocodeAddresses()
		self.apiLocationsToLatLongs()
		
	def unlockGoogleAPI(self,googleKeyFile):
		try:
			f = open(googleKeyFile)
			googleKey = f.read()
			f.close()
			self.gmaps = googlemaps.Client(key=googleKey)
		except:
			print('read {} from {} \n'
			+'and it was not a valid key.'.format(googleKey,googleKeyFile))
		finally:
			return self
		
	def readCSV(self,addressesCSV):
		try:
			self.addresses = []
			self.departureTimes = []
			self.stayDuration = []
			firstIter = True
			with open(addressesCSV) as csvFile:
				reader = csv.reader(csvFile)
				for row in reader:
					self.addresses.append(', '.join(row[:-1]))
					if firstIter == True:
						#example proper format: '09/19/20 13:55:26'
						print('Unless you\'re excused below, you messed up the departure date/time in the addresses csv.')
						print("departure time is: ",row[-1])
						try:
							self.departureTime = datetime.strptime(row[-1], '%m/%d/%y %H:%M:%S')
						except:
							self.departureTime = datetime.strptime(row[-1], ' %m/%d/%y %H:%M:%S')
						finally:
							firstIter = False
							print('you did the date/time right! no worries your\'re excused.')
					else:
						self.stayDuration.append(row[-1])
		except:
			print('failed to read {}'.format(addressesCSV))
		finally:
			return self
			
	def geocodeAddresses(self):
		if len(self.addresses) == 0:
			print('no addresses list loaded')
		else:
			self.gmaps.geocode(self.addresses[0])
			self.locations = [self.gmaps.geocode(address) for address in self.addresses]
		return self
	
	def apiLocationsToLatLongs(self):
		if len(self.locations) == 0:
			print('no locations list loaded')
		else:
			self.latLongs = [
			(
				locs[0]['geometry']['location']['lat'],
				locs[0]['geometry']['location']['lng']
			) for locs in self.locations]
		return self
		
	def createTimeMatrix(self):
		#will come back to later
		mat = np.zeros([len(self.locations),len(self.locations)])
		return self
	
	def testSolutionStability(self,deltaMins):
		codings = []
		cashe = ''
		time = self.departureTime
		delta = timedelta(minutes=deltaMins)
		self.orderings = []
		first = True
		for i in range(23):
			time = time + delta
			optimized_ordering = self.gmaps.directions(
				self.latLongs[0],
				self.latLongs[0],
				departure_time=time,
				optimize_waypoints=True,
				waypoints=self.latLongs[1:])[0]['waypoint_order']
			coding = ''
			for index in range(len(optimized_ordering)):
				coding = coding + ascii_lowercase[index]*optimized_ordering[index]
			codings.append(coding)
			if cashe != coding:
				if not first:
					print('cashe updated from {} to {}'.format(cashe,coding))
				else:
					first = False
				cashe = coding
				self.orderings.append(optimized_ordering)
				
				
		uniqueCodes = set(codings)
		if len(list(uniqueCodes)) == 1:
			print('this is likely the best route regardless of traffic')
		else:
			print('departure time matters...')
		return self

if __name__ == "__main__":
	try:
		keyFile = 'googleAPIKey.txt'
		addressesCSV = 'sampleAddresses.csv'
		gAPI = googleAPI(keyFile,addressesCSV)
		gAPI.testSolutionStability(45)
		#print([ordering for ordering in gAPI.orderings])
		iter = 0
		for elem in gAPI.orderings:
			print('option {}\n'.format(iter))
			for i in elem:
				print(gAPI.addresses[i])
			print('\n\n')
	except:
		keyFile = input("File with google Key in it: ")
		addressesCSV = input("File with addresses in it: ")
		gAPI = googleAPI(keyFile,addressesCSV)
		gAPI.testSolutionStability(45)
		#print([ordering for ordering in gAPI.orderings])
		iter = 0
		for elem in gAPI.orderings:
			print('option {}\n'.format(iter))
			for i in elem:
				print(gAPI.addresses[i])
			print('\n\n')
	terminate = input("press enter to close.")
	
		

