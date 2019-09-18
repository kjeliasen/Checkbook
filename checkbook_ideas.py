#!/bin/env/python -e

import json
import sys


    # print([f'{key} == {value}' for key, value in kwargs.items()])
    # print(kwargs['users'])


def main():
    # do all the things
    while True:
        for command, (fn, desc) in commands.items():
            print(f'{command:4d}) {desc}')
        command = input('enter the thing to do: ')
        fn = commands.get(command, unknown)
        fn()
    save(transactions, users, accounts)


def load(username):
    with open(f'checkbook_accounts.json') as fin:
        data = json.load(fin))
    transactions = data['transactions']
    accounts = data['accounts']
    users = data['users']
    return transactions, users, accounts

def save(username, transactions, users, accounts):
    data = dict(
        users=user
        transactions=transactions,
        accounts=accounts,
    )
    with open(f'checkbook_{username}.json', 'w') as fout:
        json.dump(fout, data)



if __name__ == '__main__':
    main()


commands = {
    '1': (view_balance, 'View Balance'),
    '2': (record_debit, 'Make Deposit'),
    '3': (record_credit 'Withdraw Funds'),
    '4': (change_user, 'Change User'),
    '5': (change_account, 'Change Account'),
    'X': (bailout, 'Exit')
    # ...
}


def view_balance():
    pass


def record_debit():
    pass


def unknown():
    print('wtf, chuck?')
