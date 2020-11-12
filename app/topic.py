class Topic:
    proposals = []
    accepted_proposals = []
    last_proposed = -1

    def __init__(self, model, id, priorities):
        self.id = id
        self.priorities = priorities
        self.model = model        
        self.num_remaining_slots = self.model.p_ceil
        

    def propose(self,topic_remaining_slots):
        self.last_proposed += 1 # initialize

        # Prepare list of proposals to make to each student for this one topic
        # case 1: More students needing the topic than the topics allowed slots
        if((self.last_proposed + topic_remaining_slots) <= (len(self.priorities)-1)):
            if(self.last_proposed == 0 ):
                self.proposals = self.priorities[self.last_proposed : topic_remaining_slots ]
            self.last_proposed = self.last_proposed + topic_remaining_slots
        else:
            # case 2: propose to assign topics to all students who need it.
            if(self.last_proposed <= len(self.priorities)):
                self.proposals = self.priorities[self.last_proposed : len(self.priorities)]
            self.last_proposed = len(self.priorities)-1

        for stud_id in self.proposals:
            # Add this topic to list of the student's proposals
            self.model.get_student(stud_id).receive_proposal(self.id)

    # After student accepts the proposals, the topic is updated to reflect the change
    def update_accepted_proposals(self, student_id):
        print('Topic id: ',self.id)
        print('Accepted proposal of Student: ', student_id)
        self.accepted_proposals.append(student_id)
        self.num_remaining_slots -= 1

    def is_proposing_complete(self):
        print('Topic proposing complete: ',self.last_proposed >= len(self.priorities)-1)
        return (self.last_proposed >= len(self.priorities)-1)

    def is_slots_remaining(self):
        return self.num_remaining_slots > 0