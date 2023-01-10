from telebot import TeleBot, types

def split_string(string):
    string = string.replace('+', ' + ')
    string = string.replace('-', ' - ')
    string = string.replace('*', ' * ')
    string = string.replace('/', ' / ')
    string = string.replace('(', ' ( ')
    string = string.replace(')', ' ) ')
    return string.split()


def calc_parse(digit_lst):
    new_list = []
    try:
        for i in range(len(digit_lst)):
            if digit_lst[i] != '+' and digit_lst[i] != '-' and digit_lst[i] != '*' and digit_lst[i] != '/' and \
                digit_lst[i] != ')' and digit_lst[i] != '(' and i > 0:
                digit_lst[i] = float(digit_lst[i])
                if digit_lst[i-1] == '+':
                    new_list.append(digit_lst[i])
                elif digit_lst[i-1] == '-':
                    new_list.append(digit_lst[i] * -1)
                elif digit_lst[i-1] == '*':
                    new_list[-1] = digit_lst[i] * new_list[-1]
                elif digit_lst[i-1] == '/':
                    new_list[-1] = new_list[-1] / digit_lst[i]
            elif digit_lst[i] != '+' and digit_lst[i] != '-' and digit_lst[i] != '*' and digit_lst[i] != '/' and \
                    digit_lst[i] != ')' and digit_lst[i] != '(' and i == 0:
                digit_lst[i] = float(digit_lst[i])
                new_list.append(digit_lst[i])
        return sum(new_list)
    except:
        return 'error'


def calc_result(string2):
    count = 0

    while '(' in string2:
        string3 = string2
        try:
            for i in range(len(string2)):
                if string2[i] == '(':
                    count += 1
                    begin = i
                elif string2[i] == ')':
                    count -= 1
                    end = i
                    digit_lst2 = split_string(string2[begin + 1:end])
                    string3 = string3.replace(string2[begin:end + 1], str(calc_parse(digit_lst2)))
            string2 = string3
        except:
            return 'error'
    digit_lst3 = split_string(string2)
    return calc_parse(digit_lst3)


def check_result(field):
    for i in range(3):
        if field[i * 3] == field[i * 3 + 1] == field[i * 3 + 2] and field[i * 3] != ' ':
            return field[i * 3]
        elif field[i] == field[i + 3] == field[i + 6] and field[i] != ' ':
            return field[i]
        elif (field[0] == field[4] == field[8] or field[2] == field[4] == field[6]) and field[4] != ' ':
            return field[4]
    return None


def change_turn(turn):
    if turn == 'x':
        turn = 'o'
    else:
        turn = 'x'
    return turn

