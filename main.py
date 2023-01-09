from telebot import TeleBot, types
from functions import *


TOKEN = '5924570455:AAE4JkWLXeaDuwGyLxvg5Cmg8ikE47BSJ'
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
def calc(msg: types.Message):
     field = [' '] * 9
     turn = 'X'
     chck = None
     print_board(msg, field)
     while chck is None and ' ' in field:
          move(msg, turn, field)
          print_board(msg, field)
          chck = check_result(field)
          if turn == 'X':
               turn = 'O'
          else:
               turn = 'X'
     end_game = 'deuce'
     if chck is not None:
          end_game = chck + ' WIN!'
     bot.send_message(chat_id=msg.from_user.id, text=f'GameOver {end_game}')
     bot.send_message(chat_id=msg.from_user.id, text='/calc - Калькулятор \n /cross - Крестики/нолики \n /log - Логирование')


def move(msg, sign, field):
    bot.send_message(chat_id=msg.from_user.id, text=f'turn {sign}')
    row = 0
    while (row < 1 or row > 3) or ' ' not in field[row * 3 - 3: row * 3]:
         bot.send_message(chat_id=msg.from_user.id, text='input row number (from top)')
         bot.register_next_step_handler(msg, inp_move)
         row = inp_move(msg)
    pos = 0
    while pos < 1 or pos > 3 or field[row * 3 - 3 + pos - 1] != ' ':
         bot.send_message(chat_id=msg.from_user.id, text='input position number (from left)')
         pos = bot.register_next_step_handler(msg, lambda x: x)
    field[row * 3 - 4 + pos] = sign

def inp_move(msg):
     row = int(msg.text)


def print_board(msg, field):
    hor_divider = '+---' * 3 + '+'
    for i in range(0, 9, 3):
        j = i
        hor_line = ''
        while j < i + 3:
            hor_line += '| ' + field[j] + ' '
            j += 1
        hor_line += '|'
        bot.send_message(chat_id=msg.from_user.id, text=hor_divider)
        bot.send_message(chat_id=msg.from_user.id, text=hor_line)
    bot.send_message(chat_id=msg.from_user.id, text=hor_divider)




bot.polling()

'''
@bot.message_handler()
def answer(msg: types.Message):
     text = msg.text
     if text == '+':
          bot.register_next_step_handler(msg, answer1)
          bot.send_message(chat_id=msg.from_user.id, text='Введите слагаемые')
     elif text == '-':
          bot.register_next_step_handler(msg, answer2)
          bot.send_message(chat_id=msg.from_user.id, text='Введите уменьшаемое и вычитаемое')
     else:
          bot.send_message(chat_id=msg.from_user.id, text='Вы прислали: ' + msg.text +
                                                          ', а должны были арифметическое действие')


def answer1(msg):
     a, b = map(int, msg.text.split())
     bot.send_message(chat_id=msg.from_user.id, text=f'Результат сложения {a + b}')


def answer2(msg):
     a, b = map(int, msg.text.split())
     bot.send_message(chat_id=msg.from_user.id, text=f'Результат вычитания {a - b}')



def log(update: Update, context: CallbackContext):
 file = open('db.csv', 'a')
 file.write(f'{update.effective_user.first_name},{update.effective_user.id}, {update.message.text}\n')
 file.close()
 
'''