# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.

from functions.MinChainLenNeeded import chain_can_reach_spot

# Chain is an object used to store amino chains inside search functions and inside the Protein object.
class Chain(object):
    def __init__(self, chain):
        
        # The list containing the aminos in the correct order of the chain.
        self.chain_list = chain

        # Used to represent if the chain is in the pre mirror state or post mirror state.
        self.can_still_mirror = True

        # The amount of "de-mirror" moves this chain has made. Used in determining mirror state.
        self.non_mirror_moves = 0

        # Contains the same aminos as the chain, but in a matrix.
        self.matrix = []

        self.score = 0
        
        # Saves if a specific amino in chain has a odd or an even index.
        self.odd = True

        # Saves the available spots in the format: [[x,y],[x,y][x,y]]
        # The spots in wich a c or h could make a connection.
        self.available_bonds_odd_H = []
        self.available_bonds_even_H = []

        self.available_bonds_odd_C = []
        self.available_bonds_even_C = []
        
    
    # Update the can_still_mirror status, HAS TO BE CALLED EVERY TIME AN AMINO IS ADDED TO THE CHAIN.
    def update_mirror_status(self):
        if self.chain_list[-1].coordinates[0] == self.chain_list[0].coordinates[0] and self.chain_list[-1].fold == 1:
            self.non_mirror_moves += 1
        if self.can_still_mirror:
            if self.non_mirror_moves > 0:
                self.can_still_mirror = False
    
    # Reverse the update that has been made using update_mirror_status
    def update_mirror_status_reverse(self):
        if self.can_still_mirror == False:
            if self.chain_list[-1].coordinates[0] == self.chain_list[0].coordinates[0] and self.chain_list[-1].fold == 1:
                self.non_mirror_moves -= 1
            
            if self.non_mirror_moves == 0:
                self.can_still_mirror = True
    
    # Adds fold spots to the correct list.
    def add_fold_spots(self, spot_list, mode):
        
        if mode == "H":
            for spot in spot_list:
                if self.odd:
                    self.available_bonds_odd_H.append(spot)
                else:
                    self.available_bonds_even_H.append(spot)
        
        if mode == "C":
            for spot in spot_list:
                if self.odd:
                    self.available_bonds_odd_C.append(spot)
                else:
                    self.available_bonds_even_C.append(spot)
        
     
    
    # Removes fold spots from the correct list
    def remove_fold_spots(self, spot_list, mode):
        if mode == "H":    
            for spot in spot_list:     
                if self.odd:
                    self.available_bonds_odd_H.remove(spot)
                
                if not self.odd:
                    self.available_bonds_even_H.remove(spot)
        if mode == "C":
            for spot in spot_list:     
                if self.odd:
                    self.available_bonds_odd_C.remove(spot)
                
                if not self.odd:
                    self.available_bonds_even_C.remove(spot)
    
    # Gets the max possible score from beyond that place in the chain
    def get_max_possible_extra_score(self, chars_to_go):
        spots_to_remove_even = []
        spots_to_remove_odd = []
        spots_to_remove_even_C = []
        spots_to_remove_odd_C = []

        # First remove the non attainable fold spots
        for spot in self.available_bonds_even_H:
            if not chain_can_reach_spot(self.chain_list[-1].coordinates, spot, len(chars_to_go)):
                spots_to_remove_even.append(spot)

        for spot in self.available_bonds_odd_H:
            if not chain_can_reach_spot(self.chain_list[-1].coordinates, spot, len(chars_to_go)):
                spots_to_remove_odd.append(spot)
        
        for spot in self.available_bonds_odd_C:
            if not chain_can_reach_spot(self.chain_list[-1].coordinates, spot, len(chars_to_go)):
                spots_to_remove_odd_C.append(spot)
        
        for spot in self.available_bonds_even_C:
            if not chain_can_reach_spot(self.chain_list[-1].coordinates, spot, len(chars_to_go)):
                spots_to_remove_even_C.append(spot)
        
        for spot in spots_to_remove_even:
            self.available_bonds_even_H.remove(spot)
        
        for spot in spots_to_remove_odd:
            self.available_bonds_odd_H.remove(spot)
        
        for spot in spots_to_remove_even_C:
            self.available_bonds_even_C.remove(spot)
        
        for spot in spots_to_remove_odd_C:
            self.available_bonds_odd_C.remove(spot)
        
        # The amount of spots that could be filled
        odd_H_amount = len(self.available_bonds_odd_H)
        even_H_amount = len(self.available_bonds_even_H)
        odd_C_amount = len(self.available_bonds_odd_C)
        even_C_amount = len(self.available_bonds_even_C)

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
                    if char == "C":
                        # Can make mutiple connections
                        if odd_C_amount > 1:
                            odd_C_amount -= 1
                            extra_score -= 10
                        # Can make 1 connection
                        else:
                            extra_score -= 5
                    # Can make mutiple connections
                    elif odd_H_amount > 1:
                        odd_H_amount -= 1
                        extra_score -= 2
                    # Can make 1 connection
                    else:
                        extra_score -= 1
                
                # If even
                else:
                    if char == "C":
                        # Can make multiple connections
                        if even_C_amount > 1:
                            even_C_amount -= 1
                            extra_score -= 10
                        # Can make 1 connection
                        else:
                            extra_score -= 5
                    # Can make multiple connections
                    elif even_H_amount > 1:
                        even_H_amount -= 1
                        extra_score -= 2
                    # Can make 1 connection.
                    else:
                        extra_score -= 1
        
        return extra_score, spots_to_remove_even, spots_to_remove_odd, spots_to_remove_even_C, spots_to_remove_odd_C
    
    # Adds back even spots that were previously removed
    def add_back_even(self, spots, mode):
        if mode == "H":
            for spot in spots:
                self.available_bonds_even_H.append(spot)
        if mode == "C":
            for spot in spots:
                self.available_bonds_even_C.append(spot)
    
    # Add back odd spots that were previously removed
    def add_back_odd(self, spots, mode):
        if mode == "H":
            for spot in spots:
                self.available_bonds_odd_H.append(spot)
        if mode == "C":
            for spot in spots:
                self.available_bonds_odd_C.append(spot)

