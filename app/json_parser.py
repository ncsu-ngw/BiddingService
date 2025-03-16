import json
import random
import operator
import email.utils
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
        # Check if the data is in the new format (users contain "bids")
        sample_user = next(iter(data["users"].values()))
        if "bids" in sample_user:
            # Data is already in new format
            return data
        elif "bids" in data:
            # Old format: Convert top-level bids into per-user bids
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
                    users[sid] = {"bids": []}
                users[sid]["bids"].append({"tid": tid, "priority": priority, "timestamp": timestamp})
            # Merge otids if available.
            if "otids" in data:
                for sid, otid in data["otids"].items():
                    if sid in users:
                        users[sid]["otid"] = otid
            return {
                "users": users,
                "tid": list(all_topics),
                "max_accepted_proposals": data["max_accepted_proposals"]
            }
        else:
            # Fallback: Return data as is
            return data

    def calculate_popular_topics(self):
        self.topics_counts = Counter()
        for student_id in self.student_ids:
            user_data = self.input_data_dict["users"][student_id]
            if "bids" in user_data and user_data["bids"]:
                chosen_topic_ids = [bid["tid"] for bid in user_data["bids"]]
            else:
                chosen_topic_ids = user_data.get("tid", [])
            self.topic_lists += chosen_topic_ids
        self.topics_counts = Counter(self.topic_lists)

    def create_student_priorities(self, json_dict):
        student_priorities_dict = {}
        for student_id in self.student_ids:
            user_data = json_dict["users"][student_id]
            if "bids" in user_data and user_data["bids"]:
                bids = user_data["bids"]
                sorted_bids = sorted(bids, key=lambda bid: bid["priority"])
                chosen_topic_ids = [bid["tid"] for bid in sorted_bids]
                timestamps = [email.utils.parsedate_to_datetime(bid["timestamp"]) for bid in bids]
                max_timestamp_dt = max(timestamps)
                max_timestamp_str = max_timestamp_dt.strftime("%a, %d %b %Y %H:%M:%S EST -05:00")
                user_data["max_timestamp"] = max_timestamp_str
            else:
                chosen_topic_ids = user_data.get("tid", [])
            if not chosen_topic_ids:
                all_topics = list(json_dict["tid"])
                random.shuffle(all_topics)
                student_priorities_dict[student_id] = all_topics
            else:
                if "bids" in user_data and user_data["bids"]:
                    sorted_topics = chosen_topic_ids
                else:
                    sorted_topics = [x for _, x in sorted(zip(user_data.get("priority", []), chosen_topic_ids))]
                student_priorities_dict[student_id] = sorted_topics
                unchosen_topic_ids = list(set(json_dict["tid"]).difference(set(chosen_topic_ids)))
                random.shuffle(unchosen_topic_ids)
                student_priorities_dict[student_id] += unchosen_topic_ids
                if "otid" in user_data:
                    otid = user_data["otid"]
                    if otid in student_priorities_dict[student_id]:
                        student_priorities_dict[student_id].remove(otid)
                    student_priorities_dict[student_id].append(otid)
        return student_priorities_dict

    def create_topic_priorities(self, json_dict):
        topic_priorities_dict = {}
        for total_topic_id in self.topic_ids:
            topic_priorities_dict[total_topic_id] = []
            for student_id in self.student_ids:
                user_data = json_dict["users"][student_id]
                if total_topic_id in self.student_priorities_dict[student_id]:
                    if "bids" in user_data and user_data["bids"]:
                        timestamp = user_data["max_timestamp"]
                        num_chosen_topics = len(user_data["bids"])
                    else:
                        timestamp = max(user_data.get("time", [0]))
                        num_chosen_topics = len(user_data.get("tid", []))
                    topic_priority = self.student_priorities_dict[student_id].index(total_topic_id)
                    topic_priorities_dict[total_topic_id].append((student_id, topic_priority, num_chosen_topics, timestamp))
            topic_priorities_dict[total_topic_id].sort(key=lambda x: (x[1], x[2], x[3]))
            topic_priorities_dict[total_topic_id] = [x[0] for x in topic_priorities_dict[total_topic_id]]
        return topic_priorities_dict
