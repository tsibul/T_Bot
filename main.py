from telebot import TeleBot, types
from functions import *


BOT_PATH ='t.me/gbl_8_191222_bot'


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def menu(msg: types.Message):
     bot.send_message(chat_id=msg.from_user.id, text='/calc - Калькулятор \n /cross - Крестики/нолики  \n /log - Логирование')


@bot.message_handler(commands=['calc'])
def calc(msg: types.Message):
     bot.send_message(chat_id=msg.from_user.id, text='Введите выражение без пробелов')
     bot.register_next_step_handler(msg, calc_r)

@bot.message_handler(commands=['log'])
def answer(msg: types.Message):
     bot.send_message(chat_id=msg.from_user.id, text='Вывожу лог')


def calc_r(msg: types.Message):
     string = msg.text
     bot.send_message(chat_id=msg.from_user.id, text=f'{string} = {calc_result(string)}')
     bot.send_message(chat_id=msg.from_user.id, text=f'calculation finished')
     bot.send_message(chat_id=msg.from_user.id, text='/calc - Калькулятор \n /cross - Крестики/нолики \n /log - Логирование')



@bot.message_handler(commands=['cross'])
def cross(msg: types.Message):
    global field
    field = [' '] * 9
    turn = 'x'
    print_board(msg, field)
    move(msg, field, turn)

def move(msg, field, turn):
    bot.send_message(chat_id=msg.from_user.id, text=f'turn {turn}')
    coord = ['', '']
    bot.send_message(chat_id=msg.from_user.id, text='input row number (from top)')
    bot.register_next_step_handler(msg, inp_row, coord=coord, turn=turn)

def inp_row(msg: types.Message, coord, turn):
    #    global row
    try:
        coord[0] = int(msg.text)
        bot.send_message(chat_id=msg.from_user.id, text='input position number (from left)')
        bot.register_next_step_handler(msg, inp_pos, coord=coord, turn=turn)
    except:
        bot.send_message(chat_id=msg.from_user.id, text='wrong input, repeat please')
        move(msg, field, turn)

def inp_pos(msg: types.Message, coord, turn):
    #    global pos
    try:
        coord[1] = int(msg.text)
        if coord[1] < 1 or coord[1] > 3 or field[coord[0] * 3 - 3 + coord[1] - 1] != ' ' or coord[0] < 1 or coord[0] > 3:
            bot.send_message(chat_id=msg.from_user.id, text='wrong input, repeat please')
            move(msg, field, turn)
        else:
            field[coord[0] * 3 - 4 + coord[1]] = turn
            check_result(msg, field, turn)
    except:
        bot.send_message(chat_id=msg.from_user.id, text='wrong input, repeat please')
        move(msg, field, turn)

def check_result(msg, field, turn):
    for i in range(3):
        if field[i * 3] == field[i * 3 + 1] == field[i * 3 + 2] and field[i * 3] != ' ':
            bot.send_message(chat_id=msg.from_user.id, text=f'GameOver {field[i+3]} WIN!')
            bot.send_message(chat_id=msg.from_user.id, text='/calc - Калькулятор \n /cross - Крестики/нолики \n /log - Логирование')
            return
        elif field[i] == field[i + 3] == field[i + 6] and field[i] != ' ':
            bot.send_message(chat_id=msg.from_user.id, text=f'GameOver {field[i]} WIN!')
            bot.send_message(chat_id=msg.from_user.id, text='/calc - Калькулятор \n /cross - Крестики/нолики \n /log - Логирование')
            return
        elif (field[0] == field[4] == field[8] or field[2] == field[4] == field[6]) and field[4] != ' ':
            bot.send_message(chat_id=msg.from_user.id, text=f'GameOver {field[4]} WIN!')
            bot.send_message(chat_id=msg.from_user.id, text='/calc - Калькулятор \n /cross - Крестики/нолики \n /log - Логирование')
            return
    tmp = len(list(filter(lambda x: x == 'x' or x == 'o', field)))
    if tmp == 9:
        bot.send_message(chat_id=msg.from_user.id, text=f'GameOver deuce')
        bot.send_message(chat_id=msg.from_user.id, text='/calc - Калькулятор \n /cross - Крестики/нолики \n /log - Логирование')
    else:
        print_board(msg, field)
        turn = change_turn(turn)
        move(msg, field, turn)




#@bot.message_handler()

def print_board(msg, field):
    board = ''
    for i in range(0, 9, 3):
        j = i
        while j < i + 3:
            board += '| ' + field[j] + ' '
            j += 1
        board += '|\n' + '-' * 13 + '\n'
    board = board.rstrip('\n').rstrip('-').rstrip('\n')
    bot.send_message(chat_id=msg.from_user.id, text=board)




bot.infinity_polling()

