def chatbot_response(user_input):
    # Convert user input to lower case for case-insensitive matching
    user_input = user_input.lower()

    # Define responses based on predefined rules
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "how are you" in user_input:
        return "I'm just a chatbot, but I'm here to help you!"
    elif "your name" in user_input:
        return "I'm a rule-based chatbot created to assist you with your queries."
    elif "help" in user_input:
        return "Sure, I'm here to help! What do you need assistance with?"
    elif "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I don't understand that. Can you please rephrase?"

# Main program loop
def main():
    print("Chatbot: Hello! Type 'bye' to exit the chat.")
    while True:
        user_input = input("You: ")
        if "bye" in user_input.lower():
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = chatbot_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
