from bs4 import BeautifulSoup
import csv

with open('ATP Rankings - FlashScore.com.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

players_soup = soup.find_all("div", class_ ="rankingTable__player")

player_links={}
for player in players_soup:
    player_links[player.a.text] = player.a['href']

def csv_writer():
    with open('player_links.csv', 'w') as Players:
        Players = csv.writer(Players, delimiter=',')
        for index, player in enumerate(players_soup):
            Players.writerow([index + 1, player.a['href'], player.a.text])


