from bs4 import BeautifulSoup

with open('ATP Rankings - FlashScore.com.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

players_soup = soup.find_all("div", class_="rankingTable__player")

player_links = {}
for player in players_soup:
    player_links[player.a.text] = player.a['href']


class Player:
    def __init__(self, name):
        self.name = name
        self.link = player_links[name]
        self.results = self.link + '/results/'


DJO = Player("Djokovic Novak")

print(DJO.results)
