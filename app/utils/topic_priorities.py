

def create_topic_priorities(topic_ids, student_ids, student_priorities_dict, json_dict):
        topic_priorities_dict = {}
        # Build a priority list for each topic.
        for total_topic_id in topic_ids:
            topic_priorities_dict[total_topic_id] = []
            for student_id in student_ids:
                user_data = json_dict["users"][student_id]
                # If a student has the topic, we will use their timestamp and number of bids
                if total_topic_id in student_priorities_dict[student_id]:
                    if "bids" in user_data and user_data["bids"]:
                        timestamp = user_data["max_timestamp"]
                        num_chosen_topics = len(user_data["bids"])
                    else:
                        timestamp = max(user_data.get("time", [0]))
                        num_chosen_topics = len(user_data.get("tid", []))
                    topic_priority = student_priorities_dict[student_id].index(total_topic_id)
                    topic_priorities_dict[total_topic_id].append((student_id, topic_priority, num_chosen_topics, timestamp))
            # Sort students for a specific topic by priority then number of topics selected then timestamp
            topic_priorities_dict[total_topic_id].sort(key=lambda x: (x[1], x[2], x[3]))
            topic_priorities_dict[total_topic_id] = [x[0] for x in topic_priorities_dict[total_topic_id]]
        return topic_priorities_dict