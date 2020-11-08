import math
import random
import json
from student import Student
from topic import Topic

class TopicsMatcher:
    def __init__(self,student_ids,topic_ids,student_priorities_map,
                topic_preferences_map,max_accepted_proposals):
    #   max_accepted_proposals is the Number of topics a student must be assigned.
    #   Each student accepts no more than max_accepted_proposals proposals as per preferences, rejecting the rest.
        self.student_ids = student_ids
        self.topic_ids = topic_ids
        self.max_accepted_proposals = max_accepted_proposals
        self.num_students = len(self.student_ids)
        self.num_topics = len(self.topic_ids)
        if(self.num_topics==0):
            self.num_topics=1        
        self.students = []
        self.topics = []

    def get_student_topic_matches(self):
        matches = dict()      
        return matches
