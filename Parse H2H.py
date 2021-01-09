from bs4 import BeautifulSoup
import csv
from os import listdir


def directory(folder):
    games_files_list = []
    for file in listdir(folder):
        if file[-4:] == 'html':
            games_files_list.append(file)

    return games_files_list


def list_of_games(page_of_h2h):
    with open(page_of_h2h, encoding="utf8") as html_file:
        soup = BeautifulSoup(html_file, 'lxml')

    games_soup_even = soup.find_all("tr", class_="highlight even")
    games_soup_odd = soup.find_all("tr", class_="highlight odd")

    game_links = []
    for game in games_soup_even:
        game_links.append('https://www.flashscore.com/match/' + game.attrs['onclick'][-28:-20] + '/#point-by-point;1')
    for game in games_soup_odd:
        game_links.append('https://www.flashscore.com/match/' + game.attrs['onclick'][-28:-20] + '/#point-by-point;1')

    return game_links


folder = 'C:/Users/sulta/PycharmProjects/Parser/H2H Top 34'

game_links = []
for page in directory(folder):
    game_links += list_of_games(folder + '/' + page)

game_links = list(set(game_links))


def write_csv(game_links):
    with open('game_links.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for game in game_links:
            writer.writerow([game])


write_csv(game_links)
