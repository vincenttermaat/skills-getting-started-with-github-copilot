# Example 1: Greeting message for morning
# Input: 9AM
# Output: "Good morning!"

# Generate python code that takes the current time as input using the datetime module
# and returns the appropriate greeting message

from datetime import datetime
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"
    
# Example usage
if __name__ == "__main__":
    greeting = get_greeting()
    print(greeting) 