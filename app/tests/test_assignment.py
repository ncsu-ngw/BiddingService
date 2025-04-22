import pytest
import requests


def test_match_topics():
    sample_input = {
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

    expected_output = {
        "40763": [4430, 4428, 4427],
        "40764": [4428, 4430, 4429],
        "40765": [4429, 4430, 4427]
    }

    response = requests.post("http://152.7.177.36:8080/match_topics", json=sample_input)
    assert response.status_code == 200
    assert response.json() == expected_output
    

def test_match_topics_failure():
    malformed_input = {
        "tid": [4427, 4428, 4429, 4430],
        "user": {
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

    response = requests.post("http://152.7.177.36:8080/match_topics", json=malformed_input)
    assert response.status_code == 400


def test_match_topics_one_allowed_same_topic():
    sample_input = {
        "tid": [4427, 4428, 4429],
        "users": {
            "40763": {
                "bids": [
                    { "tid": 4427, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:16:51 EST -05:00" }
                ],
                "otid": 4429
            },
            "40764": {
                "bids": [
                    { "tid": 4427, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:17:51 EST -05:00" }
                ],
                "otid": 4428
            },
            "40765": {
                "bids": [
                    { "tid": 4427, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:18:51 EST -05:00" }
                ],
                "otid": 4429
            }
        },
        "max_accepted_proposals": 1
    }

    expected_output = {
    "40763": [
        4427
    ],
    "40764": [
        4429
    ],
    "40765": []
}

    response = requests.post("http://152.7.177.36:8080/match_topics", json=sample_input)
    assert response.status_code == 200
    assert response.json() == expected_output
    
def test_match_topics_same_exact_time():
    sample_input = {
        "tid": [4427, 4428, 4429],
        "users": {
            "40763": {
                "bids": [
                    { "tid": 4427, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:16:51 EST -05:00" }
                ],
                "otid": 4429
            },
            "40764": {
                "bids": [
                    { "tid": 4427, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:16:51 EST -05:00" }
                ],
                "otid": 4428
            },
            "40765": {
                "bids": [
                    { "tid": 4428, "priority": 1, "timestamp": "Sun, 15 Nov 2020 17:18:51 EST -05:00" }
                ],
                "otid": 4429
            }
        },
        "max_accepted_proposals": 1
    }

    expected_output = {
    "40763": [
        4427
    ],
    "40764": [ # They get this one because their otid is the lowest priority automatically
        4429
    ],
    "40765": [
        4428
    ]
}

    response = requests.post("http://152.7.177.36:8080/match_topics", json=sample_input)
    assert response.status_code == 200
    assert response.json() == expected_output
    