from collections import Counter

# This function agthers the chosen topic IDs by the list of Students
# It then counts how many times a topic has been bid on
# Then it returns a dictionary of topics with how many bids it has such as {77: 2, 44: 4}
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
    return topics_counts