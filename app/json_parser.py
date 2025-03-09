import json
import random
import operator
from collections import Counter

class JsonParser:
    def __init__(self, data):
        self.input_data_dict = self.transform_data(data)
        self.topic_ids = self.input_data_dict["tid"]
        self.student_ids = list(self.input_data_dict["users"].keys())
        self.topic_lists = []
        self.calculate_popular_topics()
        self.student_priorities_dict = self.create_student_priorities(self.input_data_dict)
        self.topic_priorities_dict = self.create_topic_priorities(self.input_data_dict)
        self.max_accepted_proposals = int(self.input_data_dict["max_accepted_proposals"])

    def transform_data(self, data):
        if "bids" in data:
            users = {}
            all_topics = set()
            for bid in data["bids"]:
                if "sid" not in bid:
                    raise ValueError("Each bid must include a student id ('sid').")
                sid = bid["sid"]
                tid = bid["tid"]
                priority = bid["priority"]
                timestamp = bid["timestamp"]
                all_topics.add(tid)
                if sid not in users:
                    users[sid] = {"tid": [], "priority": [], "time": []}
                users[sid]["tid"].append(tid)
                users[sid]["priority"].append(priority)
                users[sid]["time"].append(timestamp)
            return {
                "users": users,
                "tid": list(all_topics),
                "max_accepted_proposals": data["max_accepted_proposals"]
            }
        else:
            return data

    def create_student_priorities(self, json_dict):
        student_priorities_dict = {}
        for student_id in self.student_ids:
            chosen_topic_ids = json_dict["users"][student_id].get("tid", [])

            popular_tuple = self.topics_counts.most_common(3) if hasattr(self, 'topics_counts') else []
            popular_topics_list = [x[0] for x in popular_tuple]

            if not chosen_topic_ids:
                all_topics = list(json_dict["tid"])
                random.shuffle(all_topics)
                student_priorities_dict[student_id] = all_topics
            else:
                sorted_topics = [x for _, x in sorted(zip(json_dict["users"][student_id]["priority"], chosen_topic_ids))]
                student_priorities_dict[student_id] = sorted_topics

                unchosen_topic_ids = list(set(json_dict["tid"]).difference(set(chosen_topic_ids)))
                random.shuffle(unchosen_topic_ids)
                student_priorities_dict[student_id] += unchosen_topic_ids
                if "otid" in json_dict["users"][student_id]:
                    otid = json_dict["users"][student_id]["otid"]
                    if otid in student_priorities_dict[student_id]:
                        student_priorities_dict[student_id].remove(otid)
                    student_priorities_dict[student_id].append(otid)
        return student_priorities_dict

    def calculate_popular_topics(self):
        self.topics_counts = Counter()
        for student_id in self.student_ids:
            chosen_topic_ids = self.input_data_dict["users"][student_id].get("tid", [])
            self.topics_counts.update(chosen_topic_ids)

    def create_topic_priorities(self, json_dict):
        topic_priorities_dict = {}
        for total_topic_id in self.topic_ids:
            topic_priorities_dict[total_topic_id] = []
            for student_id in self.student_ids:
                if total_topic_id in self.student_priorities_dict[student_id]:
                    bids = []
                    user_data = json_dict["users"][student_id]
                    for idx, tid in enumerate(user_data.get("tid", [])):
                        if tid == total_topic_id:
                            bids.append(user_data["time"][idx])
                    bid_timestamp = max(bids) if bids else ""
                    topic_priority = self.student_priorities_dict[student_id].index(total_topic_id)
                    num_chosen_topics = len(user_data.get("tid", []))
                    topic_priorities_dict[total_topic_id].append((student_id, topic_priority, num_chosen_topics, bid_timestamp))
            topic_priorities_dict[total_topic_id].sort(key=lambda x: (x[1], x[2], x[3]))
            topic_priorities_dict[total_topic_id] = [x[0] for x in topic_priorities_dict[total_topic_id]]
        return topic_priorities_dict
