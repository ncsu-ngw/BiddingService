import json
import random
import operator

class JsonParser:
   
    def __init__(self,data):
        self.input_data_dict = data
        # print(self.input_data_dict)
        self.topic_ids = self.input_data_dict['tid']
        # print('Topic ids: ', self.topic_ids)
        self.input_data_dict['users'].keys()
        self.student_ids = list(self.input_data_dict['users'].keys())
        # print('Student ids: ', self.student_ids)

        self.student_priorities_dict = self.create_student_priorities(self.input_data_dict)
        self.topic_priorities_dict = self.create_topic_priorities(self.input_data_dict)
        self.max_accepted_proposals = int(self.input_data_dict['max_accepted_proposals'])

    def create_student_priorities(self,json_dict):
        student_priorities_dict = dict()
        for student_id in self.student_ids:
            chosen_topic_ids = json_dict['users'][student_id]['tid']
            # Check if student has topics they'd like to bid
            if not chosen_topic_ids:
                topic_already_chosen = json_dict['users'][student_id]['otid']
                student_priorities_dict[student_id] = self.topic_ids
                if topic_already_chosen in student_priorities_dict[student_id]:
                    # Check if student already choose a topic and remove it from priorities list if so
                    student_priorities_dict[student_id].remove(topic_already_chosen)
                student_priorities_dict[student_id].append(topic_already_chosen)
                self.json_dict['users'][student_id]['priority'] = random.sample(range(1, len(student_priorities_dict[student_id])+1), len(student_priorities_dict[student_id]))
                self.json_dict['users'][student_id]['time'] = [0]
            else:
                
                chosen_topic_priorities = json_dict['users'][student_id]['priority']
                student_priorities_dict[student_id] = [x for x,_ in
                                                       sorted(zip(chosen_topic_ids,
                                                       chosen_topic_priorities))]
                unchosen_topic_ids = list(set(self.topic_ids).difference(set(
                                     chosen_topic_ids)))
                topic_already_chosen = json_dict['users'][student_id]['otid']
                if topic_already_chosen in unchosen_topic_ids:
                    unchosen_topic_ids.remove(topic_already_chosen)
                student_priorities_dict[student_id] += unchosen_topic_ids
                student_priorities_dict[student_id].append(topic_already_chosen)
        return student_priorities_dict

    def create_topic_priorities(self,json_dict):
        topic_priorities_dict = dict()
        for total_topic_id in self.topic_ids:
            topic_priorities_dict[total_topic_id] = []
            for student_id in self.student_ids:
                # Check if items in total topic list is within student topic list
                if(total_topic_id in self.student_priorities_dict[student_id]):
                    timestamp = max(json_dict['users'][student_id]['time'])
                    topic_priority = self.student_priorities_dict[
                                     student_id].index(total_topic_id)
                    num_chosen_topics = len(json_dict['users'][student_id][
                                        'tid'])
                    topic_priorities_dict[total_topic_id].append((student_id,
                                                    topic_priority,
                                                    num_chosen_topics,
                                                    timestamp))
            topic_priorities_dict[total_topic_id].sort(key = operator.itemgetter(1,2,
                                                 3))
            topic_priorities_dict[total_topic_id] = [x for x,_,_,_ in
                                              topic_priorities_dict[total_topic_id]]
        return topic_priorities_dict


# inputData= { "tid": [1234,1235,1236,1237],
#              "users": {
#                  "student1": {
#                      "tid": [1234, 1215, 1237],
#                      "otid": [1236],
#                      "priority": [1,3,2],
#                      "time": "[2012-12-15 01:21:05, 2012-12-15 01:21:10, 2012-12-15 01:21:15]"},
#                  "student2": {
#                      "tid": [1234, 1215, 1236],
#                      "otid": [1237],
#                      "priority": [2,1,2],
#                      "time": "[2012-12-15 01:22:05, 2012-12-15 01:20:10, 2012-12-15 01:22:15]"}},
#              "max_accepted_proposals": 3}
# if __name__ == "__main__":
#     JsonParser(inputData)