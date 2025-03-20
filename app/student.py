class Student:

    proposals = []
    accepted_proposals = []

    def __init__(self,model,id,choices):        
        self.model =model
        self.id = id 
        self.choices = choices        
        self.num_remaining_slots = self.model.max_accepted_proposals
        self.proposals = []
        self.accepted_proposals = []

    # Student receives a proposal from one of the topics
    def receive_proposal(self, topic_id):        
        self.proposals.append(topic_id)

    def accept_proposal(self):           
        temp = []
        for x in self.proposals:
            # Remove duplicates
            if x not in temp:
                temp.append(x)
        self.proposals = temp
        # Sort the incoming topic proposals based on the students choice priorities and pick highest preference first
        self.proposals.sort(key=lambda proposal: self.choices.index(proposal))        

        if(self.num_remaining_slots > 0):
            # Accept proposals as long as there are slots remaining.
            self.accepted_proposals = self.accepted_proposals + self.proposals[:self.num_remaining_slots]            
            self.num_remaining_slots -= len(self.accepted_proposals)   
        self.proposals = [] #clear
        # Acknowledging acceptance of topics
        for topic_id in self.accepted_proposals:
            self.model.get_topic(topic_id).update_accepted_proposals(self.id)
        self.num_remaining_slots -= len(self.accepted_proposals)