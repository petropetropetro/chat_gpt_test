import openai
import argparse
from pathlib import Path
import enum
import datetime
import json
from json.decoder import JSONDecodeError

class AcrionMode(enum.Enum):
    f_read = 0
    f_write = 1

def help_msg():
    print()
    print('Print anything to use chat')
    print('Print \'Quit\' to  - exit')
    print()

def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='api key path', default='key.txt')
    parser.add_argument('--history', help='history file path based on data (json format)', default=None)
    return parser.parse_args()

def init_gpt(key_file_path):
    openai.api_key = open(key_file_path, "r").read().strip("\n")

def predict_answer(input, message_history):

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message_history
    )
    reply_content = completion.choices[0].message.content
    return reply_content

def read_write_history(file_path, mode, input_str):
    if file_path is None:
        file_path = str(datetime.datetime.now().date())+'.json'
    data_from_file = None
    fp = Path(file_path)
    fp.touch(exist_ok=True)

    with open(file_path, 'r+') as f:
        try:
            data_from_file = json.load(f)
        except JSONDecodeError:
            print(JSONDecodeError)
            exit()
        if mode == AcrionMode.f_read:
            return data_from_file
        f.seek(0)
        if data_from_file is None:
            f.write(json.dumps(input_str))
        else:
            f.write(json.dumps(input_str)+ ',' + json.dumps(data_from_file))
        f.close()

def main(history):

    message_history = []
    # if history is not None:
        # message_history = read_write_history(history, AcrionMode.f_read, None)
        # print(message_history)
    while True:
        help_msg()
        user_option = input('Enter text and press enter: ')
        if user_option == 'Quit':
            print('Thanks for using my chat')
            exit()
        #message_history.append({"role": "user", "content": f"{user_option}"})
        read_write_history(history, AcrionMode.f_write, {"role": "user", "content": f"{user_option}"})
        response = predict_answer(input, message_history)
        print('ChatGPT responce: ', response)
        # message_history.append({"role": "assistant", "content": f"{response}"})
        response = "1234"
        read_write_history(history, AcrionMode.f_write, {"role": "assistant", "content": f"{response}"})


if __name__ == "__main__":
    args = init_args()
    if args.key is not None:
        init_gpt(args.key)
        main(args.history)
    else:
        print("Wrong parametrs!")
    