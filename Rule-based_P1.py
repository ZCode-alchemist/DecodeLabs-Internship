import re
import random
import datetime

class RuleBasedChatbot:
    def __init__(self, name="BotBuddy"):
        self.name = name

        # --- Rule tables -------------------------------------------------
        self.greetings = ["hello", "hi", "hey", "good morning",
                          "good afternoon", "good evening", "greetings",
                          "yo", "howdy"]

        self.farewells = ["bye", "goodbye", "see you", "exit", "quit",
                          "later", "take care", "farewell"]

        self.thanks = ["thanks", "thank you", "appreciate it", "cheers"]

        self.affirmations = ["yes", "yeah", "yep", "sure", "ok", "okay",
                             "alright", "of course"]
        self.negations = ["no", "nope", "nah", "not really"]

        self.compliments = ["you're smart", "you are smart", "good bot",
                            "you're helpful", "you're great", "nice job",
                            "well done", "you're cool"]
        self.insults = ["you're dumb", "you are dumb", "you're stupid",
                        "bad bot", "you suck", "useless"]

        self.questions = ["how you doing", "what is your condition", "wasup"]

        # General small talk — keyword -> list of possible responses
        self.small_talk = {
            "how are you": [
                "I'm just a program, but I'm running smoothly. Thanks for asking!",
                "Doing great, all my rules are firing correctly!",
            ],
            "how old are you": [
                "I don't have an age — I'm just code that runs whenever you start me!",
            ],
            "where are you from": [
                "I don't live anywhere — I exist as a Python script on your computer!",
            ],
            "what is your name": [
                f"My name is {self.name}, a simple rule-based chatbot."
            ],
            "who are you": [
                f"I'm {self.name}! I follow fixed rules to answer you, no AI model involved."
            ],
            "what can you do": [
                ("I can chat a bit, answer basic questions, tell you the date/time, "
                 "and do simple math like '5 + 3' or '10 divided by 2'.")
            ],
            "who created you": [
                "I was built as a demo of rule-based chatbot logic in Python."
            ],
            "i love you": [
                "That's sweet of you to say! I'm just a simple program though. 😄"
            ],
            "tell me a joke": [
                "Why do programmers prefer dark mode?...\n Because light attracts bugs!",
                "Why was the equal sign so humble?...\n Because it knew it wasn't less than or greater than anyone else.",
                "Why did the AI go to therapy?...\n Because it had too many deep learning issues. 😄"
            ],
            "what is ai": [
                "AI is technology that lets computers learn from data and make smart decisions or predictions, kind of like how humans think."
            ],
            "fun fact": [
                "The term 'Artificial Intelligence' was coined in 1956 at a conference at Dartmouth College—decades before AI could even hold a basic conversation like this one!",
                "The first computer 'bug' was an actual moth found stuck in a Harvard Mark II computer in 1947.",
                "Oxford University is older than the Aztec Empire — it was already teaching students by 1096."
            ],
            "help": [
                ("What can I do for you? You can ask me by saying things like: \n 'hello',\n 'what's the date', \n'what time is it'\n, "
                 "'12 * 4',\n 'tell me a joke',\n 'tell a fun fact' or \n'what can you do'.")
            ],
        }

        # Multi-word operators placed FIRST to avoid partial replacement issues
        self.word_operators = [
            ("subtracted from", "-"),
            ("multiplied by", "*"),
            ("added to", "+"),
            ("divided by", "/"),
            ("plus", "+"),
            ("add", "+"),
            ("minus", "-"),
            ("subtract", "-"),
            ("times", "*"),
            ("multiply", "*"),
            ("divide", "/"),
            ("over", "/")
        ]

        self.fallback_responses = [
            "Hmm, I'm not sure I understand. Could you rephrase that?",
            "I didn't quite catch that. Try asking about the date, time, "
            "a calculation, or say 'help' to see what I can do.",
            "I'm a rule-based bot, so I only understand certain patterns. "
            "Type 'help' for some ideas!",
            "Not sure how to respond to that yet — maybe try 'help'?",
        ]

    # ----------------------------------------------------------------
    # Helper rule-checkers
    # ----------------------------------------------------------------
    def _matches_any(self, text, keywords):
        # Word-boundary match so short keywords (e.g. 'yo', 'no') don't
        # false-positive inside longer words (e.g. 'you', 'know').
        return any(re.search(r"\b" + re.escape(keyword) + r"\b", text)
                   for keyword in keywords)

    def _check_small_talk(self, text):
        for key, responses in self.small_talk.items():
            if re.search(r"\b" + re.escape(key) + r"\b", text):
                return random.choice(responses)
        return None

    def _check_datetime(self, text):
        now = datetime.datetime.now()
        has_date = bool(re.search(r"\bdate\b", text) or "day is it" in text)
        has_time = bool(re.search(r"\btime\b", text))
        
        if has_date and has_time:
            return f"Today's date is {now.strftime('%Y-%m-%d')} and the time is {now.strftime('%H:%M:%S')}."
        if has_date:
            return f"Today's date is {now.strftime('%Y-%m-%d')}."
        if has_time:
            return f"The current time is {now.strftime('%H:%M:%S')}."
        return None

    def _normalize_word_math(self, text):
        """Convert word-based operators into symbols in order of string length."""
        normalized = text
        for word, symbol in self.word_operators:
            normalized = normalized.replace(word, f" {symbol} ")
        return normalized

    def _check_calculation(self, text):
        """
        Detects arithmetic expressions using symbols (+ - * / x ×) or words
        (plus, minus, times, divided by, etc.).
        """
        normalized = self._normalize_word_math(text)
        pattern = r"(-?\d+(?:\.\d+)?)\s*([\+\-\*/x×])\s*(-?\d+(?:\.\d+)?)"
        match = re.search(pattern, normalized)
        if not match:
            return None

        num1_str, op, num2_str = match.groups()
        num1, num2 = float(num1_str), float(num2_str)

        try:
            if op == "+":
                result = num1 + num2
            elif op == "-":
                result = num1 - num2
            elif op in ("*", "x", "×"):
                result = num1 * num2
            elif op == "/":
                if num2 == 0:
                    return "I can't divide by zero!"
                result = num1 / num2
            else:
                return None
        except Exception:
            return None

        if result.is_integer():
            result = int(result)

        return f"The result of {num1:g} {op} {num2:g} is {result}."

    # ----------------------------------------------------------------
    # Main response generator
    # ----------------------------------------------------------------
    def generate_response(self, user_input):
        text = user_input.lower().strip()

        if not text:
            return "Please say something!"

        # Rule evaluation pipeline by priority
        if self._matches_any(text, self.farewells):
            return "Goodbye! Have a great day. 👋"

        if self._matches_any(text, self.thanks):
            return "You're welcome!"

        if self._matches_any(text, self.compliments):
            return "Aw, thank you! I try my best with my rules. 😊"

        if self._matches_any(text, self.insults):
            return "I'm sorry you feel that way — I'll try to be more helpful!"

        if self._matches_any(text, self.greetings):
            return f"Hello there! I'm {self.name}. How can I help you today?"

        if self._matches_any(text, self.questions):
            return "I'm good. Hope you are doing well too!"

        dt_response = self._check_datetime(text)
        if dt_response:
            return dt_response

        calc_response = self._check_calculation(text)
        if calc_response:
            return calc_response

        small_talk_response = self._check_small_talk(text)
        if small_talk_response:
            return small_talk_response

        if self._matches_any(text, self.affirmations):
            return "Great, glad to hear it!"

        if self._matches_any(text, self.negations):
            return "No worries, let me know if there's something else I can help with."

        return random.choice(self.fallback_responses)

    def chat(self):
        print(f"------------------------------------------------------\n")
        print(f"{self.name}: Hi! Type 'help' for ideas, or 'bye'/'quit' to exit.\n")
        while True:
            user_input = input("Zarnab: ")
            response = self.generate_response(user_input)
            print(f"{self.name}: {response}")
            if self._matches_any(user_input.lower(), self.farewells):
                break


if __name__ == "__main__":
    bot = RuleBasedChatbot(name="BotBuddy")
    bot.chat()