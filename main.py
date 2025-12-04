import logging
from src.chat import chat
from src.prompt import conversation_history

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

def main():
    print("=" * 50)
    print("Chat Assistant Ready! (DEBUG MODE ACTIVE)")
    print("This assistant is extremely unstable, and may produce incorrect or incomplete answers.")
    print("Please be careful to input the name of the pipe or compoanant exactly as it is in the documentation.")
    print("Type 'quit' or 'exit' to end the conversation")
    print("=" * 50)
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nAssistant: Goodbye!")
            break
        if user_input.lower() in ['new', 'new chat']:
            conversation_history.clear()
            print("\nAssistant: Starting a new chat.\n")
            continue
        if not user_input:
            continue
        try:
            response = chat(user_input)
            print(f"\nAssistant: {response}\n")
        except Exception as e:
            logging.error("[main.py] Error in chat loop: %s", e)
            print("\nAssistant: Something went wrong while processing your request. Please try again.\n")

if __name__ == "__main__":
    main()