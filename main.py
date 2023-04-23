import model
import speech
import voice_input

quit_list = ["STOP", "EXIT", "ABORT", "QUIT", "BYE", "TERMINATE"]
chat_bot = """
 --------- | |      | |       | |     ----------------  --------_    ----------    -------------
| |``````` | |      | |     | | | |   ------    ------ | |`````| |  | |```````| |  -----  ------
| |        | _______  |    | |   | |        |  |       | |-----| |  | |       | |       | |
| |        | _______  |   | | --- | |       |  |       | |-----  |  | |       | |       | |
| |_______ | |      | |  | | ----- | |      |  |       | |_____| |  | |_______| |       | |
 --------- | |      | | | |         | |     |  |       | |______/     ---------         | |
"""


def interact(username: str) -> bool:
    question = input(f'{username}, Ask a question: ')
    if question.upper() in quit_list:
        return False
    if 'my name' in question.lower():
        question = 'My name is ' + username + '.' + question
    answer = model.generate_answer(question)
    print("Answer:", answer)
    speech.say(answer)
    return True


def talk(username: str) -> bool:
    speech.say("listening.")
    question = voice_input.listen_for_speech()
    if 'Could not understand audio.' == question:
        return True
    if question.upper() in quit_list:
        return False
    if 'my name' in question.lower():
        question = 'My name is ' + username + '.' + question
    answer = model.generate_answer(question)
    print("Answer:", answer)
    speech.say(answer)
    return True


if __name__ == "__main__":
    username = str(input("Enter your name > ")).upper()
    print(f'\033[1;32mHi {username}, Welcome to the\033[0m')
    print(f"\033[31mAdvanced {chat_bot}\033[0m")
    print('Write', quit_list, 'to stop.')
    choice = int(input('Press 1 to communicate and 2 to ask: '))
    if choice == 1:
        while talk(username):
            print()
    else:
        while interact(username):
            print()
    print('See You Again.')
    speech.say(f'See You Again. {username.title()}')
