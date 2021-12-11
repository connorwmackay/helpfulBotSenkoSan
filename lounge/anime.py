import requests
from bs4 import BeautifulSoup
import bs4
import re


def does_anime_exist(anime_name: str):
    """
    :param anime_name:
    :rtype: bool
    :return: Returns true / false depending on if the anime_name is an anime that exists.
    """
    req = requests.get("https://myanimelist.net/search/all?cat=all&q={0}".format(anime_name))
    soup: BeautifulSoup = BeautifulSoup(req.text, "lxml")
    articles = soup.find_all("article")

    for child in articles[0].descendants:
        if child.get_text().lower() == anime_name.lower(): # Direct Match
            return True

    return False


def find_closest_anime_matches(anime_name: str):
    """

    :param anime_name:
    :rtype: list
    :return: A list of the closest anime matches.
    """
    req = requests.get("https://myanimelist.net/search/all?cat=all&q={0}".format(anime_name))
    soup: BeautifulSoup = BeautifulSoup(req.text, "lxml")
    articles = soup.find_all("article")

    num_matches = 0
    match_list = []
    for child in articles[0].children:
        child_soup = BeautifulSoup(str(child.encode('utf-8')), "lxml")
        for sub_child in child_soup.children:
            if re.search("https://myanimelist.net/anime", str(sub_child.encode('utf-8'))):
                text = sub_child.get_text().lower()[16:]
                print(text)
                if re.search("watch video", text):
                    text = text.split("watch video")[0]
                else:
                    text = text.split("add\\")[0]

                match_list.append(text)
                num_matches += 1
            elif re.search("https://myanimelist.net/manga", str(sub_child.encode('utf-8'))):
                text = sub_child.get_text().lower()[16:]
                text = text.split('\nadd')[0]
                new_text = ""

                for c in text:
                    if c == '\\':
                        break
                    else:
                        new_text += c

                text = new_text

                match_list.append(text)
                num_matches += 1
            if num_matches >= 3:
                return match_list

    return match_list


def get_random_anime():
    """
    :rtype: str
    :return: Returns an random anime name.
    """
    pass