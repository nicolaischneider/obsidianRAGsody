from prompt_toolkit import prompt

# Main CLI orchestrator that handles the interactive loop.
def run_cli():
    print("Welcome to Obsidian RAGsody!")
    print("Type 'quit' or 'exit' to quit.\n")

    while True:
        try:
            user_input = prompt("obsidian-ragsody> ")

            if user_input.lower() in ['quit', 'exit']:
                print("\nBye, Dude!")
                break

            print(f"\nYou wrote: {user_input}\n")

        except KeyboardInterrupt:
            print("\nBye, Dude!")
            break

        except EOFError:
            print("\nBye, Dude!")
            break