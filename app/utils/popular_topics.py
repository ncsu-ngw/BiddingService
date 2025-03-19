from collections import Counter

def calculate_popular_topics(student_ids, input_data_dict, topic_lists):
    topics_counts = Counter()
    for student_id in student_ids:
        user_data = input_data_dict["users"][student_id]
        if "bids" in user_data and user_data["bids"]:
            chosen_topic_ids = [bid["tid"] for bid in user_data["bids"]]
        else:
            chosen_topic_ids = user_data.get("tid", [])
        topic_lists += chosen_topic_ids
    topics_counts = Counter(topic_lists)
    print(topics_counts)
    return topics_counts