class User:

    def __init__(self, username, money):
        self.username = username
        self._money = money

    def add_money(self, money_to_add):
        self._money += money_to_add

    def take_money(self, money_to_take):
        if self._money < money_to_take:
            msg = f'Cannot take more than what you have! {self.username} has got only {self._money}.'
            raise Exception(msg)
        else:
            self._money -= money_to_take

    def get_money(self):
        return self._money
