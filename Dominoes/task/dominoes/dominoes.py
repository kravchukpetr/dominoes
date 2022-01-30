# Write your code here
import random


def initialize_game():
    stock_pieces = []
    computer_pieces = []
    player_pieces = []
    domino_shake = []
    start_player = None
    items = [0, 1, 2, 3, 4, 5, 6]
    while start_player is None:
        domino = [[items[i], items[j]] for i in range(len(items)) for j in range(i, len(items))]
        for i in range(1, 15):
            stock_pieces.append(domino.pop(random.randrange(len(domino))))
            if i in range(1, 8):
                computer_pieces.append(domino.pop(random.randrange(len(domino))))
                player_pieces.append(domino.pop(random.randrange(len(domino))))

        max_double_comp = 0
        max_double_player = 0
        max_double_comp_list = [max(x) for x in computer_pieces if len(set(x)) == 1]
        if len(max_double_comp_list) > 0:
            max_double_comp = max(max_double_comp_list)
        max_double_player_list = [max(x) for x in player_pieces if len(set(x)) == 1]
        if len(max_double_player_list) > 0:
            max_double_player = max(max_double_player_list)
        if max_double_comp == max_double_player:
            continue
        if max_double_comp > max_double_player:
            start_player = 'player'
            computer_pieces.remove([max_double_comp, max_double_comp])
            domino_shake.append([max_double_comp, max_double_comp])
        else:
            start_player = 'computer'
            player_pieces.remove([max_double_player, max_double_player])
            domino_shake.append([max_double_player, max_double_player])
        return stock_pieces, computer_pieces, player_pieces, domino_shake, start_player


def print_initialize(stock_pieces, computer_pieces, player_pieces, domino_shake, start_player):
    print('Stock pieces: ', stock_pieces, sep='')
    print('Computer pieces: ', computer_pieces, sep='')
    print('Player pieces: ', player_pieces, sep='')
    print('Domino snake: ', domino_shake, sep='')
    print('Status: ', start_player, sep='')


def game_status(stock_pieces, computer_pieces, player_pieces, domino_shake, status, in_board_domino_shake):
    n_limit = 8
    sep_str = "..."
    print('=' * 70)
    print('Stock size:', len(stock_pieces))
    print('Computer pieces:', len(computer_pieces))
    print()
    is_printed_set = False
    if len(domino_shake) > 6:
        for idx, val in enumerate(domino_shake):
            if idx in [0, 1, 2, len(domino_shake)-1, len(domino_shake)-2, len(domino_shake)-3]:
                print(val, end="")
            elif not is_printed_set:
                print(sep_str, end="")
                is_printed_set = True
    else:
        for idx, val in enumerate(domino_shake):
            print(val, end="")
    print('\n')
    print('Your pieces:')

    for i in range(0, len(player_pieces)):
        print(i+1, ':', player_pieces[i], sep='')
    if len(computer_pieces) == 0:
        status = "computer_win"
    elif len(player_pieces) == 0:
        status = "player_win"
    elif domino_shake[0][0] == domino_shake[len(domino_shake)-1][1] and [j for i in domino_shake for j in i].count(domino_shake[0][0]) == n_limit:
        status = "draw"
    elif status == "computer" and len(list(set([j for i in computer_pieces for j in i]) & set(in_board_domino_shake))) == 0:
        status = "draw"
    elif status == "player" and len(list(set([j for i in player_pieces for j in i]) & set(in_board_domino_shake))) == 0:
        status = "draw"
    if status == "computer":
        print("\n", "Status: Computer is about to make a move. Press Enter to continue...", sep='')
    if status == "player":
        print("\n", "Status: It's your turn to make a move. Enter your command.", sep='')
    if status == "player_win":
        print("\n", "Status: The game is over. You won!", sep='')
    if status == "computer_win":
        print("\n", "Status: The game is over. The computer won!", sep='')
    if status == "draw":
        print("\n", "Status: The game is over. It's a draw!", sep='')
    return status


def make_turn(pieces, stock_pieces, domino_shake, input_num, in_board_domino_shake):

    if input_num == 0:
        extra_piece = stock_pieces.pop(random.choice(range(0, len(stock_pieces))))
        pieces.append(extra_piece)
    else:
        domino = pieces.pop(abs(input_num)-1)
        if input_num > 0:
            if in_board_domino_shake[1] == domino[0]:
                domino_shake.append(domino)
            else:
                domino_shake.append(domino[::-1])
        else:
            if in_board_domino_shake[0] == domino[1]:
                domino_shake.insert(0, domino)
            else:
                domino_shake.insert(0, domino[::-1])
    return pieces, stock_pieces, domino_shake


def check_input_val(input_num, in_pieces, in_len_stock_pieces, in_board_domino_shake):
    if input_num == 0 and in_len_stock_pieces == 0:
        check_correct_input = False
    elif input_num == 0 and in_len_stock_pieces != 0:
        check_correct_input = True
    elif input_num > 0 and (in_pieces[abs(input_num)-1][0] == in_board_domino_shake[1] or in_pieces[abs(input_num)-1][1] == in_board_domino_shake[1]):
        check_correct_input = True
    elif input_num < 0 and (in_pieces[abs(input_num)-1][0] == in_board_domino_shake[0] or in_pieces[abs(input_num)-1][1] == in_board_domino_shake[0]):
        check_correct_input = True
    else:
        check_correct_input = False
    return check_correct_input


def get_user_input(in_player_pieces, in_len_stock_pieces, in_board_domino_shake):
    user_correct_input = False
    while not user_correct_input:
        try:
            input_num = int(input())
            if input_num in range(-len(in_player_pieces), len(in_player_pieces)+1):
                user_correct_input = check_input_val(input_num, in_player_pieces, in_len_stock_pieces, in_board_domino_shake)
                if not user_correct_input:
                    print("Illegal move. Please try again.")
            else:
                print("Invalid input. Please try again.")
        except:
            print("Invalid input. Please try again.")
    return input_num


def get_computer_input(in_computer_pieces, len_stock_pieces, in_board_domino_shake, in_domino_shake):
    computer_correct_input = False
    comp_domino_rating = {}
    len_intersect_domino_and_computer = len(list(set([j for i in in_computer_pieces for j in i]) & set([j for i in in_domino_shake for j in i])))
    shake_and_computer_pieces = in_computer_pieces[::]
    shake_and_computer_pieces.extend(in_domino_shake)
    shake_and_comp_val = [j for i in shake_and_computer_pieces for j in i]
    count_values_dict = [{x: shake_and_comp_val.count(x)} for x in set(shake_and_comp_val)]
    for domino in in_computer_pieces:
        comp_domino_rating[str(domino)] = [list(x.values())[0] for x in count_values_dict if list(x.keys())[0] == domino[0]][0] + [list(x.values())[0] for x in count_values_dict if list(x.keys())[0] == domino[1]][0]
    while not computer_correct_input:
        # input_num = random.choice(range(-len(in_computer_pieces), len(in_computer_pieces)+1))
        if len_intersect_domino_and_computer > 0 and len(comp_domino_rating) > 0:
            max_domino_rating_key = max(comp_domino_rating, key=comp_domino_rating.get)
            input_num = in_computer_pieces.index(eval(max_domino_rating_key))+1
            del comp_domino_rating[max_domino_rating_key]
        else:
            input_num = 0
        computer_correct_input = check_input_val(input_num, in_computer_pieces, len_stock_pieces, in_board_domino_shake)

    return input_num


game_over = False
stock_pieces, computer_pieces, player_pieces, domino_shake, player_turn = initialize_game()
# print_initialize(stock_pieces, computer_pieces, player_pieces, domino_shake, start_player)
while not game_over:
    board_domino_shake = [domino_shake[0][0], domino_shake[len(domino_shake)-1][1]]
    player_turn = game_status(stock_pieces, computer_pieces, player_pieces, domino_shake, player_turn, board_domino_shake)
    len_stock_pieces = len(stock_pieces)
    if player_turn in ["player_win", "computer_win", "draw"]:
        game_over = True
    elif player_turn == "player":
        input_number = get_user_input(player_pieces, len_stock_pieces, board_domino_shake)
        player_pieces, stock_pieces, domino_shake = make_turn(player_pieces, stock_pieces, domino_shake, input_number, board_domino_shake)
        player_turn = 'computer'
    elif player_turn == "computer":
        input_cmd = input()
        if input_cmd == "":
            input_number = get_computer_input(computer_pieces, len_stock_pieces, board_domino_shake, domino_shake)
            computer_pieces, stock_pieces, domino_shake = make_turn(computer_pieces, stock_pieces, domino_shake, input_number, board_domino_shake)
            player_turn = 'player'
