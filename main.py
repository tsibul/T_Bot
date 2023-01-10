from telebot import TeleBot, types
from functions import *
import csv
import os
os.chdir(os.path.dirname(__file__))
from xml.etree import ElementTree as ET



BOT_PATH ='t.me/gbl_8_191222_bot'


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def menu(msg: types.Message):
     bot.send_message(chat_id=msg.from_user.id, text=print_help())


@bot.message_handler(commands=['calc'])
def calc(msg: types.Message):
     bot.send_message(chat_id=msg.from_user.id, text='Введите выражение без пробелов')
     bot.register_next_step_handler(msg, calc_r)


def calc_r(msg: types.Message):
    string = msg.text
    bot.send_message(chat_id=msg.from_user.id, text=f'{string} = {calc_result(string)}')
    bot.send_message(chat_id=msg.from_user.id, text=f'calculation finished')
    bot.send_message(chat_id=msg.from_user.id, text=print_help())


@bot.message_handler(commands=['log'])
def answer(msg: types.Message):
     bot.send_message(chat_id=msg.from_user.id, text='Вывожу лог')


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
            bot.send_message(chat_id=msg.from_user.id, text=print_help())
            return
        elif field[i] == field[i + 3] == field[i + 6] and field[i] != ' ':
            bot.send_message(chat_id=msg.from_user.id, text=f'GameOver {field[i]} WIN!')
            bot.send_message(chat_id=msg.from_user.id, text=print_help())
            return
        elif (field[0] == field[4] == field[8] or field[2] == field[4] == field[6]) and field[4] != ' ':
            bot.send_message(chat_id=msg.from_user.id, text=f'GameOver {field[4]} WIN!')
            bot.send_message(chat_id=msg.from_user.id, text=print_help())
            return
    tmp = len(list(filter(lambda x: x == 'x' or x == 'o', field)))
    if tmp == 9:
        bot.send_message(chat_id=msg.from_user.id, text=f'GameOver deuce')
        bot.send_message(chat_id=msg.from_user.id, text=print_help())
    else:
        print_board(msg, field)
        turn = change_turn(turn)
        move(msg, field, turn)


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


@bot.message_handler(commands=['phonebook'])
def phonebook(msg):
    with open('input.csv', 'r', encoding='utf-8') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=';', skipinitialspace=False)
        phonebook = []
        for line, row in enumerate(file_reader):
            phonebook.append(Phone(row))
    start_phone_book(msg, phonebook)


def start_phone_book(msg, phonebook):
    bot.send_message(chat_id=msg.from_user.id, text=print_menu())
    bot.register_next_step_handler(msg, input_menu, phonebook=phonebook)


def input_menu(msg, phonebook):
    menu_item = msg.text
    if not menu_item.isdigit() or menu_item not in ['1', '2', '3', '8']:
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        start_phone_book(msg, phonebook)
    elif menu_item == '8':
        exit_app(msg, phonebook)
    elif menu_item == '1':
        edit_phone(msg, phonebook)
    elif menu_item == '2':
        exports(msg, phonebook)
    elif menu_item == '3':
        outputs(msg, phonebook)


def edit_phone(msg, phonebook):
    bot.send_message(chat_id=msg.from_user.id, text=print_edit())
    bot.register_next_step_handler(msg, input_edit, phonebook=phonebook)


def input_edit(msg, phonebook):
    edit_item = msg.text
    if not edit_item.isdigit() or edit_item not in ['1', '2', '3', '8']:
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        edit_phone(msg, phonebook)
    elif edit_item == '1':
        tmp = [str(len(phonebook) + 1), '', '', '', '']
        phone = Phone(tmp)
        bot.send_message(chat_id=msg.from_user.id, text='input surname')
        bot.register_next_step_handler(msg, new_surname, phonebook=phonebook, phone=phone)
    elif edit_item == '2':
        bot.send_message(chat_id=msg.from_user.id, text='input id to update')
        bot.register_next_step_handler(msg, update_phone(), phonebook=phonebook)
    elif edit_item == '3':
        bot.send_message(chat_id=msg.from_user.id, text='input id to delete')
        bot.register_next_step_handler(msg, delete_phone, phonebook=phonebook)
    elif edit_item == '8':
        start_phone_book(msg, phonebook)


def new_surname(msg, phonebook, phone):
    phone.surname = msg.text
    bot.send_message(chat_id=msg.from_user.id, text='input new name')
    bot.register_next_step_handler(msg, new_name, phonebook=phonebook, phone=phone)


def new_name(msg, phonebook, phone):
    phone.name = msg.text
    bot.send_message(chat_id=msg.from_user.id, text='input new phone')
    bot.register_next_step_handler(msg, new_phone, phonebook=phonebook, phone=phone)


def new_phone(msg, phonebook, phone):
    phone.phone = (msg.text).replace(' ', '')
    bot.send_message(chat_id=msg.from_user.id, text='input new comment')
    bot.register_next_step_handler(msg, new_comment, phonebook=phonebook, phone=phone)


def new_comment(msg, phonebook, phone):
    phone.phone_type = msg.text
    phonebook.append(phone)
    edit_phone(msg, phonebook)


def update_phone(msg, phonebook):
    ph_id = msg.text
    if not ph_id.isdigit():
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        edit_phone(msg, phonebook)
    elif int(ph_id) < 1 or int(ph_id) > len(phonebook):
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        edit_phone(msg, phonebook)
    else:
        for ph in phonebook:
            if ph.id == ph_id:
                bot.send_message(chat_id=msg.from_user.id, text=ph)
                phone = ph
                break
        bot.send_message(chat_id=msg.from_user.id, text='input new surname')
        bot.register_next_step_handler(msg, edit_surname, phonebook=phonebook, phone=phone)


def edit_surname(msg, phonebook, phone):
    phone.surname = msg.text
    bot.send_message(chat_id=msg.from_user.id, text='input new name')
    bot.register_next_step_handler(msg, edit_name, phonebook=phonebook, phone=phone)

def edit_name(msg, phonebook, phone):
    phone.name = msg.text
    bot.send_message(chat_id=msg.from_user.id, text='input new phone')
    bot.register_next_step_handler(msg, ed_phone, phonebook=phonebook, phone=phone)

def ed_phone(msg, phonebook, phone):
    phone.phone = (msg.text).replace(' ', '')
    bot.send_message(chat_id=msg.from_user.id, text='input new comment')
    bot.register_next_step_handler(msg, edit_comment, phonebook=phonebook, phone=phone)

def edit_comment(msg, phonebook, phone):
    phone.phone_type = msg.text
    input_edit(msg, phonebook)


def delete_phone(msg, phonebook):
    ph_id = msg.text
    if not ph_id.isdigit():
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        edit_phone(msg, phonebook)
    elif int(ph_id) < 1 or int(ph_id) > len(phonebook):
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        edit_phone(msg, phonebook)
    else:
        phonebook.pop(int(ph_id) - 1)
        edit_phone(msg, phonebook)


def exports(msg, phonebook):
    bot.send_message(chat_id=msg.from_user.id, text=print_exports())
    bot.register_next_step_handler(msg, exports_edit, phonebook=phonebook)


def exports_edit(msg, phonebook):
    export_item = msg.text
    if not export_item.isdigit() or export_item not in ['1', '2', '3', '8']:
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        exports(msg, phonebook)
    elif export_item == '1':
        bot.send_message(chat_id=msg.from_user.id, text='input file name')
        bot.register_next_step_handler(msg, export_csv, phonebook=phonebook)
    elif export_item == '2':
        bot.send_message(chat_id=msg.from_user.id, text='input file name')
        bot.register_next_step_handler(msg, export_xml, phonebook=phonebook)
    elif export_item == '3':
        bot.send_message(chat_id=msg.from_user.id, text='input file name')
        bot.register_next_step_handler(msg, export_html, phonebook=phonebook)
    elif export_item == '8':
        start_phone_book(msg, phonebook)


def export_csv(msg, phonebook):
    name_file = msg.text
    arr = arr_from_phonebook(phonebook)
    with open(f'{name_file}.csv', 'w', encoding='utf-8') as file:
        for text in arr:
            res_text = ";".join(text).lstrip(';')
            file.writelines(f'{res_text}; \n')
    exports(msg, phonebook)


def export_xml(msg, phonebook):
    name_file = msg.text
    arr = arr_from_phonebook(phonebook)
    Phone_Book = ET.Element('Phone_Book')
    for item in arr:
        user = ET.SubElement(Phone_Book, f'user')
        surname = ET.SubElement(user, 'id')
        surname.text = item[0]
        surname = ET.SubElement(user, 'surname')
        surname.text = item[2]
        name = ET.SubElement(user, 'name')
        name.text = item[1]
        telephone = ET.SubElement(user, 'telephone')
        telephone.text = item[3]
        comments = ET.SubElement(user, 'comments')
        comments.text = item[4]
    data = ET.tostring(Phone_Book, encoding='unicode')
    file = open(f'{name_file}.xml', 'w', encoding='utf-8')
    file.writelines(data)
    exports(msg, phonebook)


def export_html(msg, phonebook):
    name_file = msg.text + '.xml'
    arr = arr_from_phonebook(phonebook)
    with open(f'{name_file}.html', 'w', encoding='utf-8') as file:
        file.writelines(f'<!DOCTYPE html>\n')
        file.writelines(f'<html lang="ru">\n')
        file.writelines(f'\t<head>\n')
        file.writelines(f'\t\t<meta charset="utf-8">\n')
        file.writelines(f'\t\t<title>Phone Book</title>\n')
        file.writelines(f'\t<head>\n')
        file.writelines(f'\n')
        file.writelines(f'\t<body>\n')
        file.writelines(f'\t\t<h2>Phone Book</h2>\n')
        file.writelines(f'\t\t<table border="1" width="600">\n')
        file.writelines(f'\t\t\t<thead>\n')
        file.writelines(f'\t\t\t<tbody>\n')
        file.writelines(f'\t\t\t\t<tr>\n')
        file.writelines(f'\t\t\t\t\t<th>№</th>\n')
        file.writelines(f'\t\t\t\t\t<th>Фамилия</th>\n')
        file.writelines(f'\t\t\t\t\t<th>Имя</th>\n')
        file.writelines(f'\t\t\t\t\t<th>Телефон</th>\n')
        file.writelines(f'\t\t\t\t\t<th>Комментарий</th>\n')
        file.writelines(f'\t\t\t\t</tr>\n')
        file.writelines(f'\t\t\t</thead>\n')
        count = 1
        for text in arr:
            file.writelines(f'\t\t\t\t<tr>\n')
            file.writelines(f'\t\t\t\t\t<td>{count}</td> \n')
            for item in text:
                file.writelines(f'\t\t\t\t\t<td>{item}</td> \n')
            file.writelines(f'\t\t\t\t</tr>\n')
            count += 1
        file.writelines(f'\t\t\t</tbody>\n')
        file.writelines(f'\t\t</table>\n')
        file.writelines(f'\t</body>\n')
        file.writelines(f'</html>')
    exports(msg, phonebook)


def outputs(msg, phonebook):
    bot.send_message(chat_id=msg.from_user.id, text=print_outputs())
    bot.register_next_step_handler(msg, outputs_edit, phonebook=phonebook)


def outputs_edit(msg, phonebook):
    output_item = msg.text
    if not output_item.isdigit() or output_item not in ['1', '2', '3', '8']:
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        outputs(msg, phonebook)
    elif output_item == '1':
        show_all(msg, phonebook)
    elif output_item == '2':
        bot.send_message(chat_id=msg.from_user.id, text='input ID')
        bot.register_next_step_handler(msg, show_id, phonebook=phonebook)
    elif output_item == '3':
        bot.send_message(chat_id=msg.from_user.id, text='input search string')
        bot.register_next_step_handler(msg, show_by_filter, phonebook=phonebook)
    elif output_item == '8':
        start_phone_book(msg, phonebook)


def show_all(msg,phonebook):
    for ph in phonebook:
        bot.send_message(chat_id=msg.from_user.id, text=ph)
    outputs(msg, phonebook)


def show_id(msg, phonebook):
    ph_id = msg.text
    if not ph_id.isdigit():
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        outputs(msg, phonebook)
    elif int(ph_id) < 1 or int(ph_id) > len(phonebook):
        bot.send_message(chat_id=msg.from_user.id, text='incorrect input, try agan, please')
        outputs(msg, phonebook)
    else:
        for ph in phonebook:
            if ph.id == ph_id:
                bot.send_message(chat_id=msg.from_user.id, text=ph)
                break
        outputs(msg, phonebook)


def show_by_filter(msg,phonebook):
    ph_id = msg.text
    for ph in phonebook:
        if ph_id.lower() in str(ph).lower():
            phone = ph
            bot.send_message(chat_id=msg.from_user.id, text=phone)
    outputs(msg, phonebook)


def exit_app(msg, phonebook):
    arr = arr_from_phonebook(phonebook)
    with open(f'input.csv', 'w', encoding='utf-8') as file:
        for text in arr:
            res_text = ";".join(text).lstrip(';')
            file.writelines(f'{res_text}; \n')
    bot.send_message(chat_id=msg.from_user.id, text=print_help())



bot.infinity_polling()

