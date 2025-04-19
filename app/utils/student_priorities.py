import random
import email.utils
# processes student IDs and assigns each student a list of topic IDs sorted by priority.
def create_student_priorities(student_ids, json_dict):
    student_priorities_dict = {}
    for student_id in student_ids:
        user_data = json_dict["users"][student_id]
        # Check for non empty bids data
        if "bids" in user_data and user_data["bids"]:
            bids = user_data["bids"]
            sorted_bids = sorted(bids, key=lambda bid: bid["priority"])
            chosen_topic_ids = [bid["tid"] for bid in sorted_bids]
            timestamps = [email.utils.parsedate_to_datetime(bid["timestamp"]) for bid in bids]
            max_timestamp_dt = max(timestamps)
            max_timestamp_str = max_timestamp_dt.strftime("%a, %d %b %Y %H:%M:%S EST -05:00")
            user_data["max_timestamp"] = max_timestamp_str
        else:
            chosen_topic_ids = []
        if not chosen_topic_ids:
            # Randomly assign if the student didn't put in any bids
            all_topics = list(json_dict["tid"])
            random.shuffle(all_topics)
            student_priorities_dict[student_id] = all_topics
        else:
            if "bids" in user_data and user_data["bids"]:
                sorted_topics = chosen_topic_ids
            else:
                priorities = user_data.get("priority")
                if priorities is None:
                    raise ValueError(f"Student {student_id} is missing priority field")
                # Concats priorities and chosen topic ids into a single array of tuples
                sorted_topics = [topic for _, topic in sorted(zip(priorities, chosen_topic_ids))]
            student_priorities_dict[student_id] = sorted_topics
            unchosen_topic_ids = list(set(json_dict["tid"]) - set(chosen_topic_ids))
            # Remaining topic ids
            random.shuffle(unchosen_topic_ids)
            student_priorities_dict[student_id] += unchosen_topic_ids
            if "otid" in user_data:
                otid = user_data["otid"]
                if otid in student_priorities_dict[student_id]:
                    student_priorities_dict[student_id].remove(otid)
                student_priorities_dict[student_id].append(otid)
    return student_priorities_dict