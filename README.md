#Intelligent Assignment

Intelligent assignment creates teams based off of each individual users ranking of topic preference, using k-means clustering. This webservice requires an input of each users ranks [1 being most preferred and 0 indicating no preference] and unique id [pid], as well as the max team size. This also uses top trading cycles to switch members of teams who have already worked with other members on that team.

Accessing the service
------------------

###1) Access the Webservice online
This service is hosted at: http://peerlogic.csc.ncsu.edu/intelligent_assignment/ [method name]. This service can be called without copying the code onto your local machine, simply make a post request to this url with one of the method names mentioned below. 

###2) Run it on your local machine
The service can be copied from its github repository (https://github.com/peerlogic/IntelligentAssignment). It should be deployed as a webservice; though, it will also require the python libraries flask and scipy:

-[Scipy](https://www.scipy.org/scipylib/download.html)

-[Flask](https://pypi.python.org/pypi/Flask)

Methods
------------------

###Creating teams (/match_topics):
Uses Gale shapeley algorithm to assign topics to students based on their topic interests. Works to eliminate competition for any single topic and increase the likelihood that each user obtains their most preferred topic. When multiple users need a topic and 

**Sample input and output**:

-Input: 
```
{
  "tid": [
    1234,
    1235,
    1236,
    1237,
    1238,
    1239
  ],
  "users": {
      "123": {
              
        "tid": [
            1234,1236,1237,1235
        ],
        "otid": [
            1237
            ],        
        "priority": [2,1,3,4],
        "time": ["2012-12-15 01:21:10",
                "2012-12-15 01:21:12",
                "2012-12-15 01:21:14",
                "2012-12-15 01:21:16"
        ]
       } ,
        "124": {
              
        "tid": [
            1234,1237,1239,1235
        ],
        "otid": [
            1238
            ],    
        "priority": [3,2,1,4],
        "time": ["2012-12-15 01:21:11",
                "2012-12-15 01:21:13",
                "2012-12-15 01:21:15",
                "2012-12-15 01:21:17"
        ]
       } 
  },
  "max_accepted_proposals": 3
}
```

-Output: 
```
{
    "123": [
        1234,
        1235,
        1236
    ],
    "124": [
        1234,
        1235,
        1237
    ]
}
```

Client Code Example
------------------

```python

import requests
import json

#Test data
data = json.dumps({"users":[{"ranks":[1,0,2,3], "history":[4535,9841,9843], "pid":1023},{"ranks":[1,2,0,3], "history":[1023,9843,8542], "pid":4535},{"ranks":[0,2,3,1], "history":[3649,9841,9843], "pid":1363},{"ranks":[2,1,0,3], "history":[1363,1023,3649], "pid":9841}],"max_team_size":2})
header = {'content-type': 'application/json'}
response = requests.post("http://127.0.0.1:5000/merge_teams",data= data,headers=header)
print response.text
#The response from merge teams can be used in swap team members if
#history was given in the body of the request to merge teams	
response = requests.post("http://127.0.0.1:5000/swap_team_members", data=response.text,headers=header)
print response.text
```
