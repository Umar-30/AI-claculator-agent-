from agent import ask_agent
from memory import get_memory
from rich import print

print("[bold green]AI Calculator Agent Started[/bold green]")
print("Commands: 'exit' to quit, 'history' to see memory")

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("[bold red]Goodbye![/bold red]")
        break
    
    if user_input.lower() == "history":
        print("\n[bold yellow]Conversation History:[/bold yellow]")
        for msg in get_memory():
            print(f"[dim]{msg['role']}:[/dim] {msg['content']}")
        continue

    response = ask_agent(user_input)

    print("\n[bold cyan]Agent Response:[/bold cyan]")
    print(response)