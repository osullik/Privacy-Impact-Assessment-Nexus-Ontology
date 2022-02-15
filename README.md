# IoT-Privacy
MSC8001 Research Project

The File privacy.ttl is an RDF Turtle syntax file that defines the privacy namespace. 
The privacy namespace consists of two key entity groups: PrivacyTypes and Interrogatives. 

## PRIVACY TYPES
- These are derived from Finn's 2013 Paper "Seven Types of Privacy"
- They describe the seven types of "privacy". I.e. the natural states that are vulnerable to being breached. 

## INTERROGATIVES
- These are derived from the five key sensing dimensions: "Who, What, When, Where and Why". 
- The Five sensing dimensions will link to how things can come to be known and will be the gateway to understanding privacy risk. For example, If a camera "Sees" someone at a particular place at a particular time, we can link that to WHO, WHEN and WHERE.
- The privacy states will be vulnerable to "violation" when one or more of the interrogatives intersects with a privacy type

## INTERSECTION
- Where an interrogative intersects with a privacy type, there is a risk of a privacy violation occuring. 
- To follow the previous example, if we know WHO, WHEN and WHERE something has occured there are potential risks to their Personal Privacy, Behaviour and Location & Space. 
- The current logic is described in: 

|              			| Identity (WHO) | Action (WHAT) | Time (WHEN) | Location (WHERE) | Motive (WHY) |
|-----------------------|----------------|---------------|-------------|------------------|--------------|
| Personal Privacy 	    | whoIs 		 |				 | whenIs	   | whereIs		  |				 |
| Behaviour and Action  | whoDid		 | whatDid		 | whenDid	   | whereDid 		  |				 |   
| Communication			| whoSaid		 | 				 | whenSaid	   | whereSaid		  | whySaid		 |
| Data and Image		| whoData		 | whatData		 | whenData    | 				  | 			 |
| Thoughts and Feelings | whoThought	 | whatThought 	 | whenThought | 				  | whyThought 	 |
| Location and space 	| whoAt 		 | 				 | whenAt 	   | 				  | 			 |
| Association 			| whoWith		 | 				 | whenWith    | whereWith 		  | 			 |


The File senses.ttl is an RDF Trutle syntax file that defines the sense namespace. 
The sense namespace consists of a "Collection Vector" entity group and a a number of relationships to the 
privacy interrogatives. 

## COLLECTION VECTORS
- These are derived from the privacy interrogatives defined in privacy.ttl, associating them with the type of information that feeds that interrogative. They are: 

|              			| Identity (WHO) | Action (WHAT) | Time (WHEN) | Location (WHERE) | Motive (WHY) |
|-----------------------|----------------|---------------|-------------|------------------|--------------|
| Sight	        	    | seesWho 		 | seesWhat		 | 			   | 				  |				 |
| Sound	        	    | hearsWho 		 | hearsWhat	 | 			   | 				  |				 |
| Time	        	    | 		 		 |				 | occursWhen  | 				  |				 |
| Location        	    | 		 		 |				 | 			   | locatesWhere	  |				 |



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