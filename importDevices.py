import csv

def ImportData():
	#This function imports the raw data from the Social IoT Dataset and holds it in memory for processing by the "CreateDeviceDict" function. 

	#Dataset location
	dataLoc = "/Users/kentosullivan/Documents/Uni/USQ/2021-S2/MSC8002 - Research Project II/Code/Datasets" #change this to reflect where you are storing the "Datasets" directory

	#Imported data Storage
	object_description = [] #stores the object_description data
	object_profile = [] #stores the object_profile data
	private_static_devices = [] #stores the content of the private_static_devices csv
	private_mobile_devices = [] #stores the content of the private_mobile_devices csv

	#import "object_description"

	with open (dataLoc+"/objects_description.csv", newline="") as csvfile:
		objDescReader = csv.reader(csvfile, delimiter=",")
		for row in objDescReader:
			object_description.append(row)		

	#import "object_profile"

	with open (dataLoc+"/objects_profile.csv", newline="") as csvfile:
		objProfReader = csv.reader(csvfile, delimiter=",")
		for row in objProfReader:
			object_profile.append(row)

	#import "private_static_devices"

	with open (dataLoc+"/private_devices/private_static_devices.csv", newline="") as csvfile:
		privStatReader = csv.reader(csvfile, delimiter=",")
		for row in privStatReader:
			private_static_devices.append(row)

	#import "private_mobile_devices"

	with open (dataLoc+"/private_devices/private_mobile_devices.csv", newline="") as csvfile:
		privMobReader = csv.reader(csvfile, delimiter=",")
		for row in privMobReader:
			private_mobile_devices.append(row)

	return(object_description, object_profile, private_static_devices, private_mobile_devices)


def getRelevantItems(fullServiceList):
	#This function takes the list of device types & services from the object_profile input and trims the list
	#to only the relevant values (1-9) of availiable services. "Apps" are deliberately discarded, and the 
	#device type is contained in the devicesDict dictionary the information is being passed into in "CreateDeviceDict" function.
	returnList = []

	#index rande here determined by the "services" items & excluding the applicaiton items. 
	prelimList = [fullServiceList[1],
					fullServiceList[2],
					fullServiceList[3],
					fullServiceList[4],
					fullServiceList[5],
					fullServiceList[6],
					fullServiceList[7],
					fullServiceList[8],
					fullServiceList[9],
					fullServiceList[10]]

	#Delete the blank values
	for item in prelimList:
		if item != '':
			returnList.append(item)

	return returnList


def CreateDeviceDict():
	#This function takes in the raw data from the CSV and transforms it into a Dict that can be serialised into the 
	#privacy ontology graph. 

	object_description, object_profile, private_static_devices, private_mobile_devices = ImportData()
	devicesDict = {}

	servicesDict = {}

	# Generates the dictionary of services availiable to each device type. 
	for deviceType in object_profile:
		servicesDict[deviceType[0]] = getRelevantItems(deviceType)

	# Generates the dictionary of key information from the dataset to feed the knowledgeBase creation. 
	for row in object_description:
		devicesDict[row[0]] = {"deviceType": row[2] , "userID":row[1], "deviceServices":servicesDict[row[2]]}
	

#Executes the function
CreateDeviceDict()


