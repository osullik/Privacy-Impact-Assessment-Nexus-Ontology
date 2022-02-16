import csv, stardog, os.path, json, pandas as pd, io 
from rdflib import Graph

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
	#This function is designed to turn the data held in the deviceDict dictionary into a series of RDF triples to be populated into a knowledgebase. 
	#It accetps an input of a dictionary of dictionaries describing each device in the Social IoT. 
	#It returns no value, and works as a frameword for other functions to achieve the data manipulation. 
	
	#Variables to hold each of the device descriptors. 
	deviceID = ""
	deviceType = ""
	userID = ""
	servicesList = []

	#Steps through each dictionary item & extracts the relevant values. From there, it pushes them into a function
	#that transforms them to a series of RDF triples, and then feeds those triples into a process that creates the knowledgevase in a Turtle file.
	firstTimeFlag = True # used by createTTLFile to clear out the old social_IOT_KB file if being rerun for the first time. 
	for key, value in deviceDict.items():
		deviceID = key
		deviceType = value["deviceType"]
		userID = value["userID"]
		servicesList = value["deviceServices"] 
		deviceTriples = makeRDFTriple(deviceID, deviceType, userID, servicesList)
		createTTLFile(deviceTriples, firstTimeFlag)
		firstTimeFlag = False




def makeRDFTriple(DeviceID, DeviceType, UserID, ServicesList):
	#This function is designed to create RDF triples out of various string and list values derived from the Social IoT dataset. 
	#It accepts string inputs of DeviceID, DeviceTye & userID, and a list input of Services List. 
	#It returns a formatted string that defines the properties of a SINGLE device from the Social IOT dataset. 

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

	#Formats the string into what is expected of an RDF parser (in this case, Stardog's)
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


def createSocial_IOT_KB(connection_details, database_name):
	#This function is designed to create the Social IOT Knowledgebase from available TTL Files. 
	#It accepts as an input the connection details and database name
	#It assumes that the .ttl files are contianed in the same directory as the python script
	#It returns no value, but does create & populate a database on the stardog server detailed in "connection_details"

	#Create the database from scratch, or if an older version exists, drop it. 
	with stardog.Admin(**connection_details) as admin:
		if database_name in [db.name for db in admin.databases()]:
			admin.database(database_name).drop()
		db = admin.new_database(database_name)


	#define the connection that data will be passed across
	conn = stardog.Connection(database_name, **connection_details)


	#Start a connection to the database defined in the line above
	conn.begin()


	#Add the content (here the two schema files and the Social IOT Knowledgebase.)
	conn.add_namespace("sense:", "https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl")
	conn.add_namespace("privacy:", "https://github.com/osullik/IoT-Privacy/blob/main/privacy.ttl")
	conn.add_namespace("social_IOT_KB:", "https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl")
	conn.add(stardog.content.File('privacy.ttl'))
	conn.add(stardog.content.File('senses.ttl'))
	conn.add(stardog.content.File('social_IOT_KB.ttl'))

	#Commit the added content
	conn.commit()

def createTTLFile(deviceTriples, firstTimeFlag):
	if firstTimeFlag == True:
		if os.path.isfile("./social_IOT_KB.ttl") == True:
			os.remove("./social_IOT_KB.ttl")
		else:
			pass 
	else:

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
		

def determineCollectionVectors(connection_details, database_name):
	#This is a function that runs constructor queries against the knowledgebase to 'discover' new knowledge. 
	#Here, based on the device features derived in the by the device dict made from the social IOT dataset
	#we are able to determine which collection vectors are available to each device. 

	conn = stardog.Connection(database_name, **connection_details)
	conn.begin()
	

	#For Sight 

	sightQuery = """
		PREFIX sense: <https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl>
		PREFIX social_IOT_KB: <https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl>

		CONSTRUCT {
    		?Device sense:collects sense:Sight
		}
		WHERE{
    		?Device sense:hasCamera true
		}
		"""
	sightGraph = conn.graph(sightQuery)


	#For Sound

	soundQuery = """
		PREFIX sense: <https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl>
		PREFIX social_IOT_KB: <https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl>

		CONSTRUCT {
    		?Device sense:collects sense:Sound
		}
		WHERE{
    		?Device sense:hasMicrophone true
		}
		"""
	soundGraph = conn.graph(soundQuery)

		#For Time 

	timeQuery = """
		PREFIX sense: <https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl>
		PREFIX social_IOT_KB: <https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl>

		CONSTRUCT {
    		?Device sense:collects sense:Time
		}
		WHERE{
    		?Device sense:hasClock true
		}
		"""
	timeGraph = conn.graph(timeQuery)

		#For Location

	locatorQuery = """
		PREFIX sense: <https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl>
		PREFIX social_IOT_KB: <https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl>
		CONSTRUCT {
    		?Device sense:collects sense:Location
		}
		WHERE{
    		?Device sense:hasLocator true
		}
		"""
	locatorGraph = conn.graph(locatorQuery)


	#Merge all the query results into one entity. 
	totalGraph = (sightGraph + soundGraph + timeGraph + locatorGraph)

	#decode the bytestream
	decodedTotal = (totalGraph.decode("utf-8"))

	#remove full URIs & Query Prefixes, Replacing with shortened URIs (on upload to stardog the "https:\\" was triggering a new domain)
	# & so removal was necessary for functionality. It also improves readability
	cleanedTotal = decodedTotal.replace("@prefix social_IOT_KB: <https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl> .","") #remove the prefix
	cleanedTotal = cleanedTotal.replace("@prefix sense: <https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl> .","") #remove the prefix
	cleanedTotal = cleanedTotal.replace("<https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl","social_IOT_KB:")
	cleanedTotal = cleanedTotal.replace("> <https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl"," sense:")
	cleanedTotal = cleanedTotal.replace("> ."," .")
	#Add in clean prefixes to the start of the file. 
	cleanedTotal = ("@prefix privacy: <https://github.com/osullik/IoT-Privacy/blob/main/privacy.ttl>.\n"
		+"@prefix sense: <https://github.com/osullik/IoT-Privacy/blob/main/senses.ttl>.\n"
		+"@prefix social_IOT_KB: <https://github.com/osullik/IoT-Privacy/blob/main/social_IOT_KB.ttl>.\n\n"
		+cleanedTotal)

	#Export the Collection Vectors to a File called "collectionVectors.ttl"
	with open("collectionVectors_KB.ttl", "w") as cvOut:
								cvOut.write(cleanedTotal)
	
	#Add the new triples to the data store. 						
	conn.add(stardog.content.File("collectionVectors_KB.ttl"))
	conn.commit


#Executes the function & puts the result into this deviceDict dictionary
#deviceDict = CreateDeviceDict()
#createKBTriples(deviceDict)
#createSocial_IOT_KB(connection_details, knowledgebase_name)
determineCollectionVectors(connection_details, knowledgebase_name)


	




