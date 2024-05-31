# The Privacy Impact Assessment Nexus Ontology (PIANO)
MSC8001/MSC8002 Research Project
Kent O'Sullivan

Video seminar explaining the research project and results is available on YouTube: https://www.youtube.com/watch?v=_LCFuxtUpRk 

## System Setup: 
- Download Anaconda
- Use the YAML file inclded here to build the appropriate virtual environment. 
- Download Stardog
- Install stardog to listen on the default port and use the default credentials
- Interact with Stardog using the Stardog Studio Web Interface (n.b. you may need to select the appropriate databases)

## Files and Purposes:

- *.gitignore*: used to prevent unwanted testing files being uploaded to git from the local folders
- *ConstructionQueries.SPARQL*: Holds SPARQL formatted copies of the constructor queries used for 'learning' within the social_IOT_KB
- *IOTPrivacy.YAML* holds the anaconda virtual environment needed to execute the python scripts. 
- *README.MD* This document. 
- *ImportDevices.py* Holds the python code required to generate the social_IOT_KB. If executed inside the anaconda virtual environment built out of IOTPrivacy.YAML it should execute smoothly. Note: The "Datasets" directory must be kept in the same directory that ImportDevices.py is kept in. 
- *privacy.ttl* The RDF Turtle File that defines the 'privacy' namespace.
- *privacyCompetencyQuestions.SPARQL* The SPARQL queries used during the initial building, then testing of the privacy, sense and social_IOT_KB namespaces. CQs are written in natural langauge, then in SPARQL. 
- *senses.ttl* the RDF Turtle file that defines the "sense" namespace. 
- *social_IOT_KB* the RDF Turtle file that holds the current instance of the Social IoT Knowledgebase. Note, this file will be overwritten each time that ImportDevices.py is executed. 

## PRIVACY TYPES
- These are derived from Finn's 2013 Paper "Seven Types of Privacy"
- They describe the seven types of "privacy". I.e. the natural states that are vulnerable to being breached. 

## PERSONAS
- These are derived from the five key sensing dimensions: "Who, What, When, Where and Why". 
- The Five sensing dimensions will link to how things can come to be known and will be the gateway to understanding privacy risk. For example, If a camera "Sees" someone at a particular place at a particular time, we can link that to WHO, WHEN and WHERE.
- The privacy states will be vulnerable to "violation" when one or more of the interrogatives intersects with a privacy type
- In the ontology, these are subclasses of a "persona" entity. For example, all Identities are part of a persona, but not all Personas have known identity. 

## INTERSECTION
- Where an interrogative intersects with a privacy type, there is a risk of a privacy violation occuring. 
- To follow the previous example, if we know WHO, WHEN and WHERE something has occured there are potential risks to their Personal Privacy, Behaviour and Location & Space. 
- The current logic is described in: 

|              			| Identity (WHO) | Action (WHAT) | Time (WHEN) | Location (WHERE) | Motive (WHY) |
|-----------------------|----------------|---------------|-------------|------------------|--------------|
| Personal Privacy 	    | whoIs 		 |				 | 			   | 				  |				 |
| Behaviour and Action  | whoDid		 | whatDid		 | 			   | 		 		  |				 |   
| Communication			| whoSaid		 | whatSaid		 | whenSaid	   | 				  | 			 |
| Data and Image		| whoData		 | whatData		 | 			   | 				  | 			 |
| Thoughts and Feelings | whoThought	 | whatThought 	 |			   | 				  | whyThought 	 |
| Location and space 	| whoAt 		 | 				 | whenAt 	   | whereAt		  | 			 |
| Association 			| whoWith		 | 				 | whenWith    | whereWith 		  | 			 |


The File senses.ttl is an RDF Trutle syntax file that defines the sense namespace. 
The sense namespace consists of a "Collection Vector" entity group and a a number of relationships to the 
privacy interrogatives. 

## COLLECTION VECTORS
- These are derived from the privacy interrogatives defined in privacy.ttl, associating them with the type of information that feeds that interrogative. They are: 

|              			| Identity (WHO) | Action (WHAT) | Time (WHEN) | Location (WHERE) | Motive (WHY) |
|-----------------------|----------------|---------------|-------------|------------------|--------------|
| Sight	        	    | seesWho 		 | seesWhat		 | 			   | 				  |	seesWhy		 |
| Sound	        	    | hearsWho 		 | hearsWhat	 | 			   | 				  |	hearsWhy	 |
| Time	        	    | 		 		 |				 | occursWhen  | 				  |				 |
| Location        	    | 		 		 |				 | 			   | locatesWhere	  |				 |

## INTERSECTION
- Where a Persona Entity and a Device Entity overlap in userID we make an assertion that they are the one being threatened. There is room to extend this based on proximity to other users, but that will come on future work (though I note it is possible using the existing Social IoT Dataset)
- Where a Persona and Device share a user ID, a check compares the Collection Vectors available to the Device, and the Persona Elements being projected by the individual. Where there is an equivalency (i.e. a "Compromises" sub-relationship (such as "seesWho" between "senses:Sight" and "privacy:Identity" that will be instantiated in the KB))

## THE DEVICE ENTITY
- The Device entity is designed as a 'PortKey' (ontology bridge). It serves as the interface point for the abstraction layer of the privacy impact assessment distinct from the physical network or device. In this manner, a the extensibility of this ontology to others is maximised. 

- The instantiation of the Device Properties in the Knowledge Base is derived from a mix of the *"objects_description"*, *"objectsProfile"* and *"Service and Application Description"* documents within the relevant datasets (https://github.com/osullik/IoT-Privacy/tree/main/Datasets). The definitions of numerical codes to their services is in the *"Service and Application Description"* pdf, but is summarised here: 

| Collection Vector 	| NumberCode	 |	   Definition	 | 
|-----------------------|----------------|-------------------|
| Sight	        	    | 		4 		 | "People Presence" |
| Sound	        	    | 		5 		 | "Environment"	 |
| Time	        	    | 		2 		 | "DateTime"		 |
| Location	        	| 		1 		 | "Location"		 |

While there are 18 defined classes of "service" in the dataset, these have been determined to have the most significant "first-order" impact on privacy. That is, a first-order method of deriving the time (a clock) is included, but a second-order method (e.g. combining location + temprature & external data) has not been accounted for at this time and should be examined in future work. 


## Datasets

-The Datasets folder contains data taken from **Marche, Claudio, et al. "How to exploit the Social Internet of Things: Query Generation Model and Device Profiles’ Dataset". Computer Networks (2020): 107248.**. It is available at: https://www.social-iot.org/index.php?p=downloads in its original format. Copies are kept here for data posterity. 

## Citation
If this work is of use please cite it using: 

    @mastersthesis{Osullivan2022,
        author = {O'Sullivan, Kent},
        title = {Development of a Privacy Impact Assessment Ontology for the Internet of Things},
        publisher = {University of Southern Queensland},
        url = {https://github.com/osullik/Privacy-Impact-Assessment-Nexus-Ontology/tree/main/papers},
        year = {2022}
        }