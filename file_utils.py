import pickle

file_name = r'users\users.pickle'


def save_users_to_file(users):
    """
    Saves users dictionary to a binary file

    Parameters
    ----------
    users : dict
        The users dictionary (key: username, value: user_money)
    """
    with open(file_name, 'wb') as f:
        pickle.dump(users, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_users_from_file():
    """
    Loads and returns users dictionary from a binary file
    """
    with open(file_name, 'rb') as f:
        users = pickle.load(f)
    return users


if __name__ == '__main__':
    print(load_users_from_file())
