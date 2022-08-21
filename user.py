class User:
    """
    A class used to represent a user in the system

    ...

    Attributes
    ----------
    username : str
        the user's name
    money : float
        the user's amount of money in the system

    Methods
    -------
    add_money(money_to_add)
        Adds the amount money_to_add to user's money

    take_money(money_to_take)
        Subtracts the amount money_to_take from user's money

    get_money()
        _money getter
    """

    def __init__(self, username, money):
        self.username = username
        self._money = money

    def add_money(self, money_to_add):
        """
        Adds the amount money_to_add to user's money

        Parameters
        ----------
        money_to_add : float
            The amount of money to add to user's money
        """
        self._money += money_to_add

    def take_money(self, money_to_take):
        """
        Subtracts the amount money_to_take from user's money if there is enough money

        Parameters
        ----------
        money_to_take : float
            The amount of money to subtract from user's money

        Raises
        -------
        Exception
            if user's money is lower than money_to_take
        """
        if self._money < money_to_take:
            msg = f'Cannot take more than what you have! {self.username} has got only {self._money}.'
            raise Exception(msg)
        else:
            self._money -= money_to_take

    def get_money(self):
        return self._money
