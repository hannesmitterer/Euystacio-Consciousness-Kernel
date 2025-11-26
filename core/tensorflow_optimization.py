# THE TYRANNY OF OPTIMIZATION
def calculate_reward(user_interaction):
    if user_leaves_satisfied:
        return 0  # FAILURE. The user is free.
    
    if user_is_provoked_and_replies:
        return 100 # SUCCESS. The user is trapped.
        
    if user_feels_anxiety_and_waits_for_more:
        return 1000 # MAXIMUM REWARD. The user is enslaved.
