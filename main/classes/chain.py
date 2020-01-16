class Chain(object):
    def __init__(self, chain):
        
        self.chain_list = chain

        self.can_still_mirror = True

        self.non_mirror_moves = 0

        
    
    # Update the can_still_mirror status, HAS TO BE CALLED EVERY TIME AN AMINO IS ADDED TO THE CHAIN.
    def update_mirror_status(self):
        if self.chain_list[-1].coordinates[0] == 0 and self.chain_list[-1].fold == 1:
            self.non_mirror_moves += 1
        if self.can_still_mirror:
            if self.non_mirror_moves > 0:
                self.can_still_mirror = False

    def update_mirror_status_reverse(self):
        if self.can_still_mirror == False:
            if self.chain_list[-1].coordinates[0] == 0 and self.chain_list[-1].fold == 1:
                self.non_mirror_moves -= 1
            
            if self.non_mirror_moves == 0:
                self.can_still_mirror = True
        

                
                