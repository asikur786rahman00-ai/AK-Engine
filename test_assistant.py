from ak_engine.assistant.assistant import AKAssistant

assistant = AKAssistant()

while True:
    msg = input("You: ")

    if msg.lower() in ["exit", "quit"]:
        break

    print()
    print("AK:", assistant.chat(msg))
    print()
