import json
import operator
from .utils import create_topic_priorities
from .utils import create_student_priorities
from .utils import calculate_popular_topics

class JsonParser:
    def __init__(self, data):
        self.input_data_dict = self.transform_data(data)
        self.max_accepted_proposals = int(self.input_data_dict["max_accepted_proposals"])
        self.topic_ids = self.input_data_dict["tid"]
        self.student_ids = list(self.input_data_dict["users"].keys())
        self.topic_lists = []
        self.topic_counts = calculate_popular_topics(self.student_ids, self.input_data_dict, self.topic_lists)
        self.student_priorities_dict = create_student_priorities(self.student_ids, self.input_data_dict)
        self.topic_priorities_dict = create_topic_priorities(self.topic_ids, self.student_ids, self.student_priorities_dict, self.input_data_dict)

    def transform_data(self, data):
        sample_user = next(iter(data["users"].values()))
        if "bids" in data:
            users = {}
            all_topics = set()
            for bid in data["bids"]:
                tid = bid["tid"]
                priority = bid["priority"]
                timestamp = bid["timestamp"]
                all_topics.add(tid)
            return {
                "users": users,
                "tid": list(all_topics),
                "max_accepted_proposals": data["max_accepted_proposals"]
            }
        else:
            return data


