import googlemaps
from datetime import datetime
import googlemaps
from datetime import datetime
import csv
import numpy as np
class googleAPI:
	def __init__(self,keyFile,addressesCSV):
		self.unlockGoogleAPI(keyFile)
		self.addresses = []
		self.locations = []
		self.latLongs = []
		self.departureTimes = []
		self.stayDuration = []
		self.departureTime = 0
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
			print('read {} from {} \nand it was not a valid key.'.format(googleKey,googleKeyFile))
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
						self.departureTime = datetime.strptime(row[-1], '%m/%d/%y %H:%M:%S')
						firstIter = False
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
		mat = np.zeros([len(self.locations),len(self.locations)])


if __name__ == "__main__":
	keyFile = 'googleAPIKey.txt'
	addressesCSV = 'sampleAddresses.txt'
	gAPI = googleAPI(keyFile,addressesCSV)
	locs = gAPI.latLongs
	now = datetime.now()
	datetime_str = '09/19/20 13:55:26'

	datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
	#print(datetime_object)
	#print(gAPI.addresses[0])
	optimized_ordering = gAPI.gmaps.directions(locs[0],locs[0],departure_time=now,optimize_waypoints=True,waypoints=locs[1:])[0]['waypoint_order']
	print(optimized_ordering)
	print([gAPI.addresses[1+item] for item in optimized_ordering])

	
	#keys = list(locs[0][0].keys())
	#print(keys[2])
	#print(locs[1][0]['geometry']['location']['lat'])


