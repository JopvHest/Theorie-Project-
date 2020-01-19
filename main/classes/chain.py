from functions.MinChainLenNeeded import chain_can_reach_spot

class Chain(object):
    def __init__(self, chain):
        
        self.chain_list = chain

        self.can_still_mirror = True

        self.non_mirror_moves = 0

        self.matrix = []

        self.score = 0
        
        # Saves if a specific amino in chain has a odd or an even index.
        self.odd = True

        # Saves the available spots in the format: [[x,y],[x,y][x,y]]
        self.available_bonds_odd_H = []

        self.available_bonds_even_H = []
        
    
    # Update the can_still_mirror status, HAS TO BE CALLED EVERY TIME AN AMINO IS ADDED TO THE CHAIN.
    def update_mirror_status(self):
        if self.chain_list[-1].coordinates[0] == self.chain_list[0].coordinates[0] and self.chain_list[-1].fold == 1:
            self.non_mirror_moves += 1
        if self.can_still_mirror:
            if self.non_mirror_moves > 0:
                self.can_still_mirror = False

    def update_mirror_status_reverse(self):
        if self.can_still_mirror == False:
            if self.chain_list[-1].coordinates[0] == self.chain_list[0].coordinates[0] and self.chain_list[-1].fold == 1:
                self.non_mirror_moves -= 1
            
            if self.non_mirror_moves == 0:
                self.can_still_mirror = True
        
    def add_fold_spots(self, spot_list):
        for spot in spot_list:
            if self.odd:
                self.available_bonds_odd_H.append(spot)
            else:
                self.available_bonds_even_H.append(spot)
    
    def remove_fold_spots(self, spot_list):
        for spot in spot_list:     
            if self.odd:
                self.available_bonds_odd_H.remove(spot)
            
            if not self.odd:
                self.available_bonds_even_H.remove(spot)
    
    def get_max_possible_extra_score(self, chars_to_go):
        spots_to_remove_even = []
        spots_to_remove_odd = []

        # First remove the non attainable fold spots
        for spot in self.available_bonds_even_H:
            if not chain_can_reach_spot(self.chain_list[-1].coordinates, spot, len(chars_to_go)):
                spots_to_remove_even.append(spot)

        for spot in self.available_bonds_odd_H:
            if not chain_can_reach_spot(self.chain_list[-1].coordinates, spot, len(chars_to_go)):
                spots_to_remove_odd.append(spot)
        
        for spot in spots_to_remove_even:
            self.available_bonds_even_H.remove(spot)
        
        for spot in spots_to_remove_odd:
            self.available_bonds_odd_H.remove(spot)
        

        odd_H_amount = len(self.available_bonds_odd_H)
        even_H_amount = len(self.available_bonds_even_H)

        extra_score = 0

        for index, char in enumerate(chars_to_go):
            if char != "P":
                # index is even
                if index % 2 == 0:
                    char_odd = self.odd
                
                # Index is odd
                else:
                    char_odd = not self.odd
                
                # If odd
                if char_odd:
                    if odd_H_amount > 1:
                        odd_H_amount -= 1
                        extra_score -= 2
                    else:
                        extra_score -= 1
                
                # If even
                else:
                    if even_H_amount > 1:
                        even_H_amount -= 1
                        extra_score -= 2
                    else:
                        extra_score -= 1
        
        return extra_score, spots_to_remove_even, spots_to_remove_odd
    
    def add_back_even(self, spots):
        for spot in spots:
            self.available_bonds_even_H.append(spot)
    
    def add_back_odd(self, spots):
        for spot in spots:
            self.available_bonds_odd_H.append(spot)

