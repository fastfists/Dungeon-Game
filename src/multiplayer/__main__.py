import sys
import server
import client

def ask(again=False):
    if again:
        print("That is not an option")
    choice = input("server or [Client]")
    choice.lower()
    run(choice)

def run(choice):
    if choice == 'server':
        server.execute()
    elif choice == 'client':
        client.execute()
    else:
        ask(again=True)

if len(sys.argv) == 1:
    ask()
else:
    choice = sys.argv[1]
    choice.lower()
    run(choice)