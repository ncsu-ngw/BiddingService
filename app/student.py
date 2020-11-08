class Student:

    proposals = []
    accepted_proposals = []

    def __init__(self,model,id,choices):        
        self.model =model
        self.id = id 
        self.choices = choices        
        self.num_remaining_slots = self.model.max_accepted_proposals

    def get_proposal(self, topic_id):
        self.proposals.append(topic_id)

    def accept_proposal(self):
        # TODO: First sort the proposals based on the choices index.
        # This way, we can pick the most high preference first.

        self.proposals.sort()
        # TODO: Write a method to accept the sorted proposals
        # Add condition if enough slots are available
        if(self.num_remaining_slots > 0):
            self.accepted_proposals = self.accepted_proposals + self.proposals
            self.num_remaining_slots -= len(self.accepted_proposals)