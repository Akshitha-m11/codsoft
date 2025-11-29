#!/usr/bin/env python3
import re
import random
import sys
try:
    import tkinter as tk
    from tkinter.scrolledtext import ScrolledText
except Exception:
    tk = None

class RuleBasedChatbot:
    def __init__(self):
        self.rules = [
            (r'hi|hello|hey', "Hello! 👋 How can I help you today?", "greeting"),
            (r'how are you|how are you doing', "I'm doing great! How about you?", "how_are_you"),
            (r'my name is (.+)', self._respond_name_capture, "introduce"),
            (r'what is your name|who are you', "I'm RuleBot — a rule-based chatbot.", "identity"),
            (r'(?:help|assist|how to) (?:with )?(.*)', self._respond_help_capture, "help"),
            (r'open file (.+)', "I can't open files, but I can explain how to open '{}'.", "open_file"),
            (r'thank you|thanks', "You're welcome! 😊", "thanks"),
            (r'bye|goodbye|see you', "Goodbye! Have a nice day.", "farewell"),
            (r'what is (\d+)\s*([\+\-\*\/])\s*(\d+)', self._respond_math, "math"),
            (r'weather in (.+)', "I can't check live weather, but you can search for {}.", "weather")
        ]
        self.fallbacks = [
            "I didn't understand that. Can you rephrase?",
            "I'm not sure I follow.",
            "I don't know about that yet."
        ]
        self.context = {"last_intent": None, "user_name": None}

    def _respond_name_capture(self, match):
        name = match.group(1).strip().title()
        self.context["user_name"] = name
        return f"Nice to meet you, {name}! What can I do for you?"

    def _respond_help_capture(self, match):
        topic = match.group(1).strip()
        if not topic:
            return "What do you need help with?"
        return f"What do you want to know about {topic}?"

    def _respond_math(self, match):
        a = int(match.group(1))
        op = match.group(2)
        b = int(match.group(3))
        if op == '+': res = a + b
        elif op == '-': res = a - b
        elif op == '*': res = a * b
        elif op == '/': res = a / b
        else: return "Unknown operation."
        return f"{a} {op} {b} = {res}"

    def get_response(self, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return "Please say something."
        for pattern, responder, intent in self.rules:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                self.context["last_intent"] = intent
                if callable(responder):
                    return responder(m)
                return responder.format(*(g.strip() for g in m.groups())) if m.groups() else responder
        if self.context["last_intent"] == "greeting":
            return "Anything else you'd like to ask?"
        return random.choice(self.fallbacks)

def run_console(bot: RuleBasedChatbot):
    print("RuleBot (console). Type 'quit' to exit.")
    while True:
        try:
            user = input("You: ").strip()
        except:
            print("\nBye.")
            return
        if user.lower() in {"quit", "exit", "bye"}:
            print("Bot:", bot.get_response("bye"))
            return
        print("Bot:", bot.get_response(user))

def run_gui(bot: RuleBasedChatbot):
    if tk is None:
        run_console(bot)
        return
    root = tk.Tk()
    root.title("RuleBot")

    text = ScrolledText(root, state='disabled', width=60, height=20, wrap='word')
    text.grid(row=0, column=0, columnspan=2, padx=8, pady=8)

    entry = tk.Entry(root, width=50)
    entry.grid(row=1, column=0, padx=8, pady=8, sticky='we')

    def append(who, msg):
        text.configure(state='normal')
        text.insert('end', f"{who}: {msg}\n")
        text.configure(state='disabled')
        text.see('end')

    def send(_=None):
        user_msg = entry.get().strip()
        if not user_msg:
            return
        append("You", user_msg)
        entry.delete(0, 'end')
        append("Bot", bot.get_response(user_msg))

    tk.Button(root, text="Send", command=send).grid(row=1, column=1, padx=8, pady=8)
    entry.bind("<Return>", send)
    append("Bot", "Hello! I'm RuleBot. Ask me anything.")
    root.mainloop()

if __name__ == "__main__":
    bot = RuleBasedChatbot()
    if len(sys.argv) > 1 and sys.argv[1] in {"--console", "console"}:
        run_console(bot)
    else:
        run_gui(bot)
