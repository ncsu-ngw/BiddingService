class Topic:
    proposals = []
    accepted_proposals = []
    last_proposed = -1

    def __init__(self, model, id, priorities):
        self.id = id
        self.priorities = priorities
        self.model = model        
        self.num_remaining_slots = self.model.p_ceil

    def propose(self,num):                
        if((self.last_proposed + num) <= (len(self.priorities)-1)):        
            if((self.last_proposed + 1) > (self.last_proposed+num+1)):
                self.proposals = self.priorities[self.last_proposed + 1]
            else:
                self.proposals = self.priorities[self.last_proposed+num+1]
            self.last_proposed = self.last_proposed + num
        else:
            if(self.last_proposed + 1 > len(self.priorities)):
                self.proposals = self.priorities[self.last_proposed + 1]
            else:
                self.proposals = self.priorities[len(self.priorities)]
            self.last_proposed = len(self.priorities)-1
        
        #Iterate current proposals and the students who selected the topic will receive proposals
        for student_id in self.proposals:
            self.model.get_student_by_id(student_id).get_proposal(self.id)
    
    def accept_proposal(self,student_id):
        self.accepted_proposals.append(student_id)
        self.num_remaining_slots -= 1

    def is_proposing_complete(self):
        return (self.last_proposed >= len(self.priorities)-1)

    def is_slots_remaining(self):
        return self.num_remaining_slots > 0