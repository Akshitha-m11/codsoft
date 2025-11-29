def reply(text):
    t = text.lower()

    if t in ["hi", "hello", "hey"]:
        return "Hello! What do you want to know?"
    
    if "help" in t:
        return "I can answer simple questions. Try asking me something."
    
    if "time" in t:
        from time import strftime
        return strftime("%I:%M %p")

    if "date" in t:
        from datetime import date
        return str(date.today())

    if "your name" in t:
        return "I'm a simple rule-based bot."

    if "bye" in t:
        return "Goodbye."

    return "I am not sure about that."

def start():
    print("Bot is active. Type 'bye' to exit.")
    while True:
        user = input("You: ")
        ans = reply(user)
        print("Bot:", ans)
        if ans == "Goodbye.":
            break

start()
