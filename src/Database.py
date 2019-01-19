# coding: utf8

import random


class Database(object):

    AGENTS_NAMES_FILE = "../../resources/AgentsName.txt"
    ITEMS_NAMES_FILE = "../../resources/ItemsName.txt"

    def __init__(self):
        self.agents_names = set()
        self.items_names = set()

        self.load_agents_names()
        self.load_items_names()

    def get_random_agents_names(self, number):
        return set(random.sample(self.agents_names, number))

    def get_random_items_names(self, number):
        return set(random.sample(self.items_names, number))

    def load_agents_names(self):
        with open(Database.AGENTS_NAMES_FILE) as f:
            data = f.readlines()

        for line in data:
            self.agents_names.add(line[:-1])

    def load_items_names(self):
        with open(Database.ITEMS_NAMES_FILE) as f:
            data = f.readlines()

        for line in data:
            self.items_names.add(line[:-1])
