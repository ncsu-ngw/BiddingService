#Intelligent Assignment

Intelligent assignment assigns review topics to students based off of each individual users ranking of topic preference. The service requires topic ids [tid], as well as the max number of topics per student.

Accessing the service
------------------

###1) Access the Webservice online
This service is hosted at: https://app-csc517.herokuapp.com/[match_topics]. This service can be called without copying the code onto your local machine, simply make a post request to this url with one of the method names mentioned below. 

###2) Run it on your local machine
The service can be copied from its github repository (https://github.com/uahamedncsu/IntelligentAssignment). It should be deployed as a webservice; though, it will also require the python libraries flask and scipy:

-[Scipy](https://www.scipy.org/scipylib/download.html)

-[Flask](https://pypi.python.org/pypi/Flask)

Methods
------------------

###Assigning topics (/match_topics):
Uses Gale shapeley algorithm to assign topics to students based on their topic interests. Works to eliminate competition for any single topic and increase the likelihood that each user obtains their most preferred topic. The preference is given to students who bid for the topics by using their timestamp when the bid was submitted.

**Sample input and output**:

-Input: 
```
{"tid":[4427,4428,4429,4430],"users":
{"40763":{"tid":[4430,4427,4428],"otid":4429,"priority":[1,3,2],"time":["2020-11-15T17:16:51.000-05:00","2020-11-15T17:16:52.000-05:00",       "2020-11-15T17:16:53.000-05:00"]},
"40764":{"tid":[4429,4430,4428],"otid":4427,"priority":[3,2,1],"time":["2020-11-15T17:16:34.000-05:00","2020-11-15T17:16:35.000-05:00","2020-11-15T17:16:37.000-05:00"]},
"40765":{"tid":[4427,4430,4429],"otid":4428,"priority":[3,2,1],"time":["2020-11-15T17:17:15.000-05:00","2020-11-15T17:17:16.000-05:00",   "2020-11-15T17:17:17.000-05:00"]}},
"max_accepted_proposals":3}
```

-Output: 
```
Assigned Topics to Students:
{
    "40763": [
        4427,
        4428,
        4430
    ],
    "40764": [
        4428,
        4429,
        4430
    ],
    "40765": [
        4427,
        4429,
        4430
    ]
}
```

Client Code Example
------------------

```python

import requests
import json

#Test data
data = json.dumps({"tid":[4427,4428,4429,4430],"users":{"40763":{"tid":[4430,4427,4428],"otid":4429,"priority":[1,3,2],"time":["2020-11-15T17:16:51.000-05:00","2020-11-15T17:16:52.000-05:00","2020-11-15T17:16:53.000-05:00"]},"40764":{"tid":[4429,4430,4428],"otid":4427,"priority":[3,2,1],"time":["2020-11-15T17:16:34.000-05:00","2020-11-15T17:16:35.000-05:00","2020-11-15T17:16:37.000-05:00"]},"40765":{"tid":[4427,4430,4429],"otid":4428,"priority":[3,2,1],"time":["2020-11-15T17:17:15.000-05:00","2020-11-15T17:17:16.000-05:00","2020-11-15T17:17:17.000-05:00"]}},"max_accepted_proposals":3})
header = {'content-type': 'application/json'}
response = requests.post("http://127.0.0.1:5000/match_topics",data= data,headers=header)
print response.text
```
