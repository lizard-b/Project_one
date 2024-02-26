board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
board_size = 3


def board_out():
    print('_' * 4 * board_size)
    for i in range(board_size):
        print('', board[i*3], '|', board[1 + i*3],
              '|', board[2 + i*3], '|')
        print(('_' * 3 + '|') * 3)


def game_phase(option, char):
    if option > 9 or option < 1 or board[option-1] in ('X', 'O'):
        return False
    board[option-1] = char
    return True


def win_check():
    win = False
    win_comb = [(0, 1, 2), (3, 4, 5),
                (6, 7, 8), (0, 3, 6),
                (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6)]
    for poi in win_comb:
        if (board[poi[0]] == board[poi[1]] and
                board[poi[1]] == board[poi[2]]):
            win = board[poi[0]]
    return win


def game_process():
    current_player = 'X'
    step = 1
    board_out()

    while step < 10 and win_check() is False:
        option = input('Ход игрока ' + current_player +
                       '. Введите номер поля (0 - закончить игру): ')
        if option == '0':
            break
        if game_phase(int(option), current_player):
            print('Выбор сделан.')
            if current_player == 'X':
                current_player = 'O'
            else:
                current_player = 'X'
            board_out()
            step += 1
        else:
            print('Ошибка, поле уже занято, выберите другое.')
    if step == 10:
        print('Игра закончилась ничьей.')
    else:
        print('Игрок ', win_check(), ' выиграл. Поздравляем!')


print('Классическая игра в крестики-нолики.')
game_process()
