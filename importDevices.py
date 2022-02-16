import csv, stardog, os.path 

#details for Stardog DB Connection
connection_details = {
	'endpoint': 'http://localhost:5820',
	'username': 'admin',
	'password': 'admin'
}

knowledgebase_name = 'social_IOT_KB' #KB holds the instances, as opposed to the DB which holds the schema

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
	count = 0 # a workaround to remove the header information, that was breaking the RDF Triple generation downstream by skipping row 0. 
	for row in object_description:
		if count == 0:
			pass 
		else:
			devicesDict[row[0]] = {"deviceType": row[2] , "userID":row[1], "deviceServices":servicesDict[row[2]]}
		count+= 1
	return devicesDict 


#for entry in deviceDict.items():
#	print(entry)

def createKBTriples(deviceDict):
	deviceID = ""
	deviceType = ""
	userID = ""
	servicesList = []
	for key, value in deviceDict.items():
		deviceID = key
		deviceType = value["deviceType"]
		userID = value["userID"]
		servicesList = value["deviceServices"] 
		deviceTriples = makeRDFTriple(deviceID, deviceType, userID, servicesList)
		#print(deviceTriples)
		createTTLFile(deviceTriples)




def makeRDFTriple(DeviceID, DeviceType, UserID, ServicesList):
	''' Format to get to is: 
		Social_IOT_KB:Device(<DeviceID>)
			rdf:type: sense:Device ;
			sense:deviceUser "<UserID>" ;
			sense:deviceType "<DeviceType" ;
			sense:hasCamera <TRUE where 4 in ServicesList> ;
			sense:hasMicrophone <TRUE where 5 in ServicesList> ;
			sense:hasClock <TRUE where 2 in ServicesList> ;
			sense:hasLocator <TRUE where 1 in ServicesList> .

	'''
	#Create individual strings that will form each line of the RDF triples that make up the device entity. 
	DeviceString = "social_IOT_KB:Device_{deviceID}".format(deviceID=DeviceID)
	typeString = "rdf:type sense:Device ;"
	userString = "sense:deviceUser \"{userID}\" ;".format(userID=UserID)
	devTypeString = "sense:deviceType \"{deviceType}\" ;".format(deviceType=DeviceType)

	#variable options based on whether the service is or is not present in that device. 
	if "4" in ServicesList:
		cameraBool = "sense:hasCamera \"true\"^^xsd:boolean ;"
	else:
		cameraBool = "sense:hasCamera \"false\"^^xsd:boolean ;"

	if "5" in ServicesList:
		micBool = "sense:hasMicrophone \"true\"^^xsd:boolean ;"
	else:
		micBool = "sense:hasMicrophone \"false\"^^xsd:boolean ;"

	if "2" in ServicesList:
		clockBool = "sense:hasClock \"true\"^^xsd:boolean ;"
	else:
		clockBool = "sense:hasClock \"false\"^^xsd:boolean ;"

	if "1" in ServicesList:
		locatorBool = "sense:hasLocator \"true\"^^xsd:boolean ."
	else:
		locatorBool = "sense:hasLocator \"false\"^^xsd:boolean ."

	#print("RDFTriple is: ")

	returnString = (
		DeviceString+"\n"
		"\t"+typeString+"\n"
		"\t"+devTypeString+"\n"
		"\t"+userString+"\n"
		"\t"+cameraBool+"\n"
		"\t"+micBool+"\n"
		"\t"+clockBool+"\n"
		"\t"+locatorBool+"\n"
		)
	return(returnString)


'''def createSocial_IOT_KB(connection_details, database_name):

	#Create the database from scratch, or if an older version exists, drop it. 
	with stardog.Admin(**connection_details) as admin:
	    if database_name in [db.name for db in admin.databases()]:
	        admin.database(database_name).drop()
	    db = admin.new_database(database_name)

	conn = stardog.Connection(database_name, **connection_details)


	#Start a connection to the database
	conn.begin()


	#Add the content
	conn.add(stardog.content.File('social_IOT_KB.ttl'))

	#Commit the added content
	conn.commit()'''

def instantiateKB(deviceTriples, connection_details, database_name):

	conn = stardog.Connection(database_name, **connection_details)


	#Start a connection to the database
	conn.begin()


	#Add the content
	print(deviceTriples)
	conn.add(stardog.content.Raw(deviceTriples,'text/turtle'))

	#Commit the added content
	conn.commit()

def createTTLFile(deviceTriples):
	if os.path.isfile("./social_IOT_KB.ttl") == True:
		with open("social_IOT_KB.ttl", "a") as KB_Output:
			KB_Output.write(deviceTriples+"\n")
	else:
		with open("social_IOT_KB.ttl", "w") as KB_Output:
			KB_Output.write("#RDF Triples generated automatically from the Social IOT Dataset"+"\n\n"
							"@prefix privacy: <https://github.com/osullik/IoT-Privacy/blob/main/privacy.ttl>."+"\n"
							"@prefix sense: <https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl>."+"\n"
							"@prefix social_IOT_KB: <https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl>."+"\n"
							"@prefix rdf:    	<http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."+"\n"
							"@prefix xsd:     	<http://www.w3.org/2001/XMLSchema#> ."+"\n"
							"@prefix rdfs:    	<http://www.w3.org/2000/01/rdf-schema#> ."+"\n"
							"@prefix owl:		<http://www.w3.org/2002/07/owl#> ."+"\n\n")
			KB_Output.write(deviceTriples+"\n")
		


#Executes the function & puts the result into this deviceDict dictionary
deviceDict = CreateDeviceDict()
#createSocial_IOT_KB(connection_details, knowledgebase_name)
createKBTriples(deviceDict)



	




