import json

class JsonParser:
   
    def __init__(self,data):
        self.input_data_dict = data
        print(self.input_data_dict)
        self.topic_ids = self.input_data_dict['topic_ids']
        print('Topic ids: ', self.topic_ids)
        self.input_data_dict['users'].keys()
        self.student_ids = list(self.input_data_dict['users'].keys())
        print('Student ids: ', self.student_ids)

        self.student_priorities_dict = self.create_student_priorities(self.input_data_dict)
        self.topic_priorities_dict = self.create_topic_priorities(self.input_data_dict)
        self.max_accepted_proposals = int(self.input_data_dict['max_accepted_proposals'])

    def create_student_priorities(self,json_dict):
        student_priorities_dict = dict()                
        return student_priorities_dict

    def create_topic_priorities(self,json_dict):
        topic_priorities_dict = dict()        
        return topic_priorities_dict