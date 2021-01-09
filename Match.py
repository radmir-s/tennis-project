from bs4 import BeautifulSoup
from os import listdir
import csv


def directory(folder):
    games_files_list = []
    for file in listdir(folder):
        if file[-4:] == 'html':
            games_files_list.append(file)

    return games_files_list


def match(file):
    with open(file) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    final_score = soup.find("div", class_="match-info").text.split()

    set_scores = []
    for point in soup.find_all('td', class_="match-history-score"):
        set_scores.append(point.text)

    last_game = 1
    while int(set_scores[last_game].split()[0]) + int(set_scores[last_game].split()[-1]) > 1:
        last_game += 1

    # Winner of each game
    first_set_scores = set_scores[:last_game]
    game_winners = [1 if first_set_scores[0][0] == '1' else 2]
    for i in range(last_game - 1):
        game_winners.append(1 if int(first_set_scores[i + 1][0]) > int(first_set_scores[i][0]) else 2)

    # Server is 1 or 2
    first_game = soup.find("tr", class_="odd fifteens_available")
    server = 1 if (set_scores[0].split()[-1] == '0') ^ (first_game.text.split()[-1] == 'SERVE') else 2

    # Plus one - server won, Minus one - server lost
    server_wins = [3 - x * 2 for x in game_winners] if server == 1 else [x * 2 - 3 for x in game_winners]

    games_by_points = []
    for point in soup.find_all('td', colspan="5"):
        games_by_points.append(point.text)
    first_set_games = games_by_points[:last_game]

    serves_in_games = []
    for game in first_set_games:
        serves_in_games.append(len(game.split()) + 1)

    first_set_server = [x * y for x, y in zip(serves_in_games, server_wins)]

    # Player names
    #    players = []
    #    for player in soup.find_all('a', class_="participant-imglink"):
    #        players.append(player.text)

    #    players = [name for name in players if len(name) > 2]

    #    server_name = players[server - 1]
    #    opponent_name = players[2 - server]

    #    winner = players[0] if final_score[0][0] > final_score[0][-1] else players[1]

    winner = 1 if final_score[0][0] > final_score[0][-1] else 2

    is_server_winner = 1 if winner == server else 0

    if 'retired' in final_score:
        return None
    if last_game < 6:
        return None
    if len(first_set_server) < 6:
        return None
    return [first_set_server, is_server_winner]


folder = 'C:/Users/sulta/PycharmProjects/Parser/Games Hard Top 34'


def match_stats(folder):
    match_stats = []
    for page in directory(folder):
        try:
            match_stats.append(match(folder + '/' + page))
        except Exception:
            pass
    return match_stats


match_stats = match_stats(folder)


def write_csv(match_stats):
    with open('match_stats.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['First set', 'Server wins?'])
        for match in match_stats:
            if match != None:
                writer.writerow(match)


write_csv(match_stats)
