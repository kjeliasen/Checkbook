#!/bin/env/python -e

import json
import sys
import calendar as c
import datetime as dt
import time as t
import os



# Declare Global Variables
entries_file_load = 'checkbook_accounts.json'
entries_file_save = 'checkbook_accounts_saves.json'
#cur_user_id = '0'
#cur_account_id = '0'
#new_entries = []


class UserExitException(Exception):
    if Exception:
        print(f'Exit {__name__}')


def bug_note(func, verb='checking', **kwargs):
    print(f'DEBUG: {verb} fn({func})')
    if len(kwargs.items()):
        print([f'{key.upper()} == {value}' for key, value in kwargs.items()])


def star_line():
    txt = '*' * 80
    print(txt)


def load(file=entries_file_load):
    func = 'load'
    # bug_note(verb='starting', func=func)
    with open(file) as fin:
        data = json.load(fin)
    got_users = data['users']
    got_accounts = data['accounts']
    got_entries = data['entries']
    # bug_note(verb='ending', func=func)
    print('DEBUG - Loaded file {}'.format(file))
    return got_users, got_accounts, got_entries


def save(users, accounts, entries, file=entries_file_save):
    func = 'save'    
    bug_note(verb='starting', func=func)
    data = {
        'users': users,
        'accounts': accounts,
        'entries': entries
    }
    with open(file, 'w') as fout:
        json.dump(data, fout, indent=2)
    bug_note(verb='ending', func=func)
    print('DEBUG - Saved file {}'.format(file))
    load(file)
    return True


def get_cur_user_info(context, users, **kwargs):
    func = 'get_cur_user_info'    
    # bug_note(verb='starting', func=func)
    for user in users:
        if user['user_id'] == context['current_user_id']:
            current_user_info = user
            context['current_user_info'] = current_user_info
            # bug_note(verb='happily ending', func=func, user=user, current_user_info=context['current_user_info'])
            return True
    current_user_info = {
        'user_id': '0',
        'first_name': 'NO USER',
        'last_name': 'SELECTED'
    }
    context['current_user_info'] = current_user_info
    bug_note(verb='unhappily ending', func=func, current_user_info=context['current_user_info'])
    return False


def get_cur_account_info(context, accounts, **kwargs):
    func = 'get_cur_account_info'    
    # bug_note(verb='starting', func=func)
    for account in accounts:
        if account['account_id'] == context['current_account_id']:
            current_account_info = account
            context['current_account_info'] = account
            # bug_note(verb='happily ending', func=func, current_account_info=context['current_account_info'])
            return True
    current_account_info = {
        'acct_id': '0',
        'acct_ref_name': 'NO ACCOUNT SELECTED'
    }
    bug_note(verb='unhappliy ending', func=func, current_account_info=context['current_account_info'])
    return False


def get_cur_user_accounts(context, accounts, **kwargs):
    func = 'get_cur_user_accounts'    
    # bug_note(verb='looping', func=func)
    # print(type(accounts))
    current_users_accounts = [account for account in accounts if account['account_id'] == context['current_user_id']]
    context['current_users_accounts'] = current_users_accounts
    # bug_note(verb='ending', func=func, current_users_accounts=current_users_accounts)
    return True


def get_cur_account_entries(context, entries, **kwargs):
    func = 'get_cur_account_entries'    
    bug_note(verb='looping', func=func)
    current_entries = [entry for entry in entries if entry['account_id'] == context['current_account_id']]
    context['current_entries'] = current_entries
    bug_note(verb='ending', func=func, current_entries=context['current_entries'])
    

def cl_view_balance(context, entries, **kwargs):
    func = 'cl_view_balance'    
    bug_note(verb='starting', func=func)
    txt = ''
    # do some of the things
    star_line()
    print('{:*^80s}'.format('  Viewing Balance  '))
    star_line()
    current_entries = context['current_entries']
    # print(current_entries)
    balance = sum([float(entry['amount']) for entry in current_entries])
    num_entries = len(current_entries)
#    print('\n\n')
    print('\n\n{:*<5}{:5}Account {} has a current balance of ${:.2f}.\n{:*<5}{:5}({:d} entries)\n\n'.format(
        txt, txt, str(context['current_account_id']), balance, txt, txt, num_entries
    ))
    bug_note(verb='ending', func=func)
    

def cl_record_debit(context, entries, **kwargs):
    func = 'cl_record_debit'    
    bug_note(verb='starting', func=func)
    # do some of the things
    print((' ' * 10) + 'Recording Debit')
    input_entry(context=context, entries=entries, dci='d')
    bug_note(verb='ending', func=func)
    

def cl_record_credit(context, entries,  **kwargs):
    func = 'cl_record_credit'    
    bug_note(verb='starting', func=func)
    # do some of the things
    print((' ' * 10) + 'Recording Credit')
    bug_note(verb='ending', func=func)
    

def cl_change_user(context, users, accounts, **kwargs):
    func = 'cl_change_user'    
    #bug_note(verb='starting', func=func)
    print((' ' * 10) + 'Changing User')
    # do some of the things
    context['current_user_id'] = users[0]['user_id']
    get_cur_user_info(context, users)
    get_cur_user_accounts(context, accounts)
    # bug_note(verb='ending', func=func, user_id = context['current_user_id'])
    

def cl_change_account(context, accounts, entries, **kwargs):
    func = 'cl_change_account'    
    #bug_note(verb='starting', func=func)
    # do some of the things
    print((' ' * 10) + 'Changing Account')
    context['current_account_id'] = accounts[0]['account_id']
    get_cur_account_info(context, accounts)
    get_cur_account_entries(context, entries)
    # bug_note(verb='ending', func=func, account_id = context['current_account_id'])
    

def cl_get_users_info(context, users, **kwargs):
    func = 'cl_get_users_info'    
    bug_note(verb='starting', func=func)
    # do some of the things
    print(users)
    bug_note(verb='ending', func=func)
    

def cl_get_accounts_info(context, accounts, **kwargs):
    func = 'cl_get_accounts_info'    
    bug_note(verb='starting', func=func)
    # do some of the things
    print(accounts)
    bug_note(verb='ending', func=func)
    # return context
    

def cl_get_entries_info(context, **kwargs):
    func = 'cl_get_entries_info'    
    bug_note(verb='starting', func=func)
    # do some of the things
    print(entries)
    bug_note(verb='ending', func=func)
    # return context
    

def cl_dictionary_info(context, **kwargs):
    func = 'cl_dictionary_info'    
    bug_note(verb='starting', func=func)
    # do some of the things
    print(users, accounts, entries)
    bug_note(verb='ending', func=func)
    # return context
    

def cl_save_file(context, users, accounts, entries, **kwargs):
    func = 'cl_save_file'    
    bug_note(verb='starting', func=func)
    # do some of the things
    save(users, accounts, entries, entries_file_save)
    bug_note(verb='ending', func=func)
    # return context
    

def cl_gtfo(context, **kwargs):
    func = 'cl_gtfo'    
    bug_note(verb='starting', func=func)
    star_line()
    print('User selected \'exit\'')
    star_line()
    raise UserExitException


def unknown(**kwargs):
    func = 'unknown'    
    bug_note(verb='encountering', func=func)
    print('wtf, chuck?')


def update_user_variables(user_id):
    func = 'update_user_variables'    
    bug_note(verb='starting', func=func)
    user_info = {}
    for account in accounts:
        if account['user_id'] == cur_user_id:
            bug_note(verb='ending', func=func)
            user_info = account
            break
    bug_note(verb='ending', func=func)
    return user_info


def input_entry(context, entries, dci, **kwargs):
    edit = True
    entry_sign = -1 if dci=='c' else 1
    entry_type = 'withdrawal' if dci=='c' else 'deposit'
    date_def = dt.date.today()
    def_entry = {
    "trans_id": t.time(),
    "user_id": context['current_user_id'],
    "account_id": context['current_account_id'],
    "date_recorded": date_def,
    "amount": 0,
    "description": '',
    "amount_available": 0,
    "amount_reserved": 0,
    "date_posted": date_def,
    "offset_acct_id": ""
    }
    editable_fields = [
        'amount', 'description', 'date_posted'
    ]
    print(date_def)
    print(def_entry)
    while edit:
        
        user_amount = input(f'Enter the {entry_type} amount: $')
        user_description = input('Enter the {entry_type} description: ')
        target_amount = ''.join([char for char in user_amount if char in '0123456789.'])
        num_decimals = sum([1 for char in target_amount if char == '.'])



def init_command_list():
    func = 'init_command_list'    
    # bug_note(verb='starting', func=func)
    setcommands = {
        '1': (cl_view_balance, 'View Balance', True),
        '2': (cl_record_debit, 'Make Deposit', True),
        '3': (cl_record_credit, 'Withdraw Funds', True),
        '4': (cl_change_user, 'Change User', True),
        '5': (cl_change_account, 'Change Account', True),
        'C': (cl_get_users_info, 'Check Users Data', False),
        'A': (cl_get_accounts_info, 'Check Accounts Data', False),
        'T': (cl_get_entries_info, 'Check Entries Data', False),
        'D': (cl_dictionary_info, 'Check Dictionary Data', False),
        'S': (cl_save_file, 'Save File', False),
        'X': (cl_gtfo, 'Exit', True)
        # ...
    }
    # bug_note(verb='ending', func=func)
    return setcommands

def init_context():
    func = 'init_context'    
    # bug_note(verb='starting', func=func)
    setcontext = {
        'current_user_id': False,
        'current_account_id': False,
        'data_dirty': False,
        'current_user_info': {},
        'current_users_accounts': [],
        'current_account_info': {},
        'current_entries': [],
    } 
    # bug_note(verb='ending', func=func)
    return setcontext              


def main():
    func = 'main'    
    # bug_note(verb='starting', func=func)
    commands = init_command_list()
    context = init_context()
    users, accounts, entries = load(entries_file_load)
    do_command = False
    # cur_user_accounts = 

    try:
    # do all the things
        print('\n\n')
        while True:
            if not context['current_user_id']:
                #print('DEBUG no current user')
                do_command = '4'
            else:
                star_line()
                #print('DEBUG found current user')
                #cur_user_info = get_cur_user_info(context['current_user_id'], users)
                current_user_info = context['current_user_info']
                #print(current_user_info)
                print('Current user is {} - {} {}'.format(current_user_info['user_id'], 
                    current_user_info['first_name'], current_user_info['last_name']))
                #print(cur_user_info)
                if not context['current_account_id']:
                    #print('DEBUG no current account')
                    do_command = '5'
                else:
                    #print('DEBUG found current account')
                    #cur_user_info = get_cur_user_info(context['current_user_id'], users)
                    current_account_info = context['current_account_info']
                    #print(current_account_info)
                    print('Current account is {} - {} labeled \'{}\''.format(current_account_info['account_id'], 
                        current_account_info['account_type'], current_account_info['account_ref_name']))
                    #print(cur_user_info)                
            if not do_command:
                star_line()
                print('\n\n')
                for command, (fn, desc, show) in commands.items():
                    if show:
                        print(f'{command:>20s}) {desc}')
                print('\n')
                star_line()
                do_command = input('Enter the thing to do: ')
                print('\n\n')
            fn = commands.get(do_command, (unknown, "Unknown"))
            print(f'DEBUG: Selected fn == {fn[1]}')
            fn = fn[0]
            fn(context=context, users=users, accounts=accounts, entries=entries)
            do_command = False
            bug_note(verb='reiterating', func=func)
            #bug_note(verb='reiterating', func=func, current_user_info=context['current_user_info'], current_account_info=context['current_account_info'])
            
    except Exception as e:
        print('EXCEPTION RAISED')
        print(e)
        # print(context)

    bug_note(verb='ending', func=func)
        

if __name__ == '__main__':
    # print(os.getcwd())
    main()

