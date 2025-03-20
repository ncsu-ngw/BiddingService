# Bidding Service

The student Bidding Service assigns review topics to students based off of each individual users ranking of topic preference. The service requires topic ids [tid], as well as the max number of topics per student.

Accessing the service
------------------

###1) Access the Webservice online
This service is hosted at: [http://152.7.178.10:8080/match_topics](http://152.7.178.10:8080/match_topics). This service can be called without copying the code onto your local machine, simply make a post request to this url. \
        - You can use: \
                - curl \
                - Postman \
                - Your preferred programming language!

###2) Run it on your local machine
The service can be copied from its github repository (https://github.com/ncsu-ngw/BiddingService). It should be deployed as a webservice; though, it will also require the python library flask

-[Flask](https://pypi.python.org/pypi/Flask)

Methods
------------------

###Assigning topics (/match_topics):
Uses Gale shapeley algorithm to assign topics to students based on their topic interests. Works to eliminate competition for any single topic and increase the likelihood that each user obtains their most preferred topic. The preference is given to students who bid for the topics by using their timestamp when the bid was submitted.

**Sample input and output**:

-Input: 
```
{
        "tid": [4427, 4428, 4429, 4430],
        "users": {
            "40763": {
                "bids": [
                    { "tid": 4430, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:16:51 EST -05:00" },
                    { "tid": 4427, "priority": 3, "timestamp": "Sun, 15 Nov 2020 17:16:52 EST -05:00" },
                    { "tid": 4428, "priority": 2, "timestamp": "Sun, 15 Nov 2020 17:16:53 EST -05:00" }
                ],
                "otid": 4429
            },
            "40764": {
                "bids": [
                    { "tid": 4429, "priority": 3, "timestamp": "Sun, 15 Nov 2020 17:16:34 EST -05:00" },
                    { "tid": 4430, "priority": 2, "timestamp": "Sun, 15 Nov 2020 17:16:35 EST -05:00" },
                    { "tid": 4428, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:16:37 EST -05:00" }
                ],
                "otid": 4427
            },
            "40765": {
                "bids": [
                    { "tid": 4427, "priority": 3, "timestamp": "Sun, 15 Nov 2020 17:17:15 EST -05:00" },
                    { "tid": 4430, "priority": 2, "timestamp": "Sun, 15 Nov 2020 17:17:16 EST -05:00" },
                    { "tid": 4429, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:17:17 EST -05:00" }
                ],
                "otid": 4428
            }
        },
        "max_accepted_proposals": 3
    }
```

-Output: 
```
{
        "40763": [4430, 4428, 4427],
        "40764": [4428, 4430, 4429],
        "40765": [4429, 4430, 4427]
    }
```
which are the assigned topics to the students based on the student id provided.

Client Code Example
------------------

```python

import requests
import json

#Test data
data = json.dumps({
        "tid": [4427, 4428, 4429, 4430],
        "users": {
            "40763": {
                "bids": [
                    { "tid": 4430, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:16:51 EST -05:00" },
                    { "tid": 4427, "priority": 3, "timestamp": "Sun, 15 Nov 2020 17:16:52 EST -05:00" },
                    { "tid": 4428, "priority": 2, "timestamp": "Sun, 15 Nov 2020 17:16:53 EST -05:00" }
                ],
                "otid": 4429
            },
            "40764": {
                "bids": [
                    { "tid": 4429, "priority": 3, "timestamp": "Sun, 15 Nov 2020 17:16:34 EST -05:00" },
                    { "tid": 4430, "priority": 2, "timestamp": "Sun, 15 Nov 2020 17:16:35 EST -05:00" },
                    { "tid": 4428, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:16:37 EST -05:00" }
                ],
                "otid": 4427
            },
            "40765": {
                "bids": [
                    { "tid": 4427, "priority": 3, "timestamp": "Sun, 15 Nov 2020 17:17:15 EST -05:00" },
                    { "tid": 4430, "priority": 2, "timestamp": "Sun, 15 Nov 2020 17:17:16 EST -05:00" },
                    { "tid": 4429, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:17:17 EST -05:00" }
                ],
                "otid": 4428
            }
        },
        "max_accepted_proposals": 3
    })
header = {'content-type': 'application/json'}
response = requests.post("http://152.7.178.10:8080/match_topics",data= data,headers=header)
print response.text
```
