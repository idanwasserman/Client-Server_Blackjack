class User:

    def __init__(self, username, money):
        self.username = username
        self.money = money

    def add_money(self, money_to_add):
        self.money += money_to_add

    def take_money(self, money_to_take):
        if self.money < money_to_take:
            msg = f'Cannot take more than what you have! {self.username} has got only {self.money}.'
            raise Exception(msg)
        else:
            self.money -= money_to_take

    def get_money(self):
        return self.money
