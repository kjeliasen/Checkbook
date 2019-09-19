#!/usr/bin/env/ python3 -e

import json
import sys
import calendar as c
import datetime as dt
import time as t
import os



# Declare Global Variables
entries_file_load = 'checkbook_accounts.json'
entries_file_save = 'checkbook_accounts.json'
#cur_user_id = '0'
#cur_account_id = '0'
#new_entries = []
txt = '' # fill text for string format


def bug_note(func, verb='checking', **kwargs):
    print(f'DEBUG: {verb} fn({func})')
    if len(kwargs.items()):
        print([f'{key.upper()} == {value}' for key, value in kwargs.items()])


def init_command_list():
    func = 'init_command_list'    
    # bug_note(verb='starting', func=func)
    return {
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


def init_context():
    func = 'init_context'    
    # bug_note(verb='initing', func=func)
    return {
        'current_user_id': False,
        'current_account_id': False,
        'data_dirty': False,
        'current_user_info': {},
        'current_users_accounts': [],
        'current_account_info': {},
        'current_entries': [],
    } 


def init_new_entry(context, date_def):
    func = 'init_context'    
    # bug_note(verb='initing', func=func)
    return {
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
    

class UserExitException(Exception):
    func = 'UserExitException'    
    bug_note(verb='starting', func=func)
    if Exception:
        print(f'Exit {__name__}')


def star_line():
    txt = '*' * 80
    print(txt)


def star_wall(wrap_str=txt):
    if len(wrap_str) > 60:
        print(wrap_str)
    else:
        print(f'{txt:*<3s}{txt:<7s}{wrap_str:<60s}{txt:<7s}{txt:*<3s}')


def star_beg():
    star_line()
    star_wall()


def star_end():
    star_wall()
    star_line()


def star_buffer():
    la = f'{txt:*<3s}{txt:<74s}{txt:*<3s}'
    lb = f'{txt:*<80s}'
    return la + '\n' + lb + '\n' + la


def star_box(*args):
    star_beg()
    for arg in args:
        starg = str(arg)
        if len(starg) > 60:
            print(starg)
        else:
            star_wall(f'{starg:<60s}')
    star_end()

def load(file=entries_file_load):
    func = 'load'
    # bug_note(verb='starting', func=func)
    with open(file) as fin:
        data = json.load(fin)
    got_users = data['users']
    got_accounts = data['accounts']
    got_entries = data['entries']
    # bug_note(verb='ending', func=func)
    print('DEBUG - Loaded file {file}')
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
    print(f'DEBUG - Saved file {file}')
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
    # bug_note(verb='looping', func=func)
    context['current_entries'] = [entry for entry in entries if entry['account_id'] == context['current_account_id']]
    # bug_note(verb='ending', func=func, current_entries=context['current_entries'])
    

def get_cur_account_balance(context, **kwargs):
    # func = 'get_cur_account_balance'
    # bug_note(verb='starting', func=func)
    return sum([float(entry['amount']) for entry in context['current_entries']])


def get_cur_account_entry_count(context, **kwargs):
    # func = 'get_cur_account_entry_count'
    # bug_note(verb='starting', func=func)
    return len(context['current_entries'])


def pause_it():
    star_box('{:^60s}'.format('press enter to continue'))
    meh = input('')


def input_entry(context, entries, dci, **kwargs):
    func = 'input_entry'
    bug_note(verb='starting', func=func)
    print('DEBUG: set Edit')
    edit = True
    print('DEBUG: set entry sign')
    entry_sign = -1 if dci=='c' else 1
    print('DEBUG: set entry type')
    entry_type = 'withdrawal' if dci=='c' else 'deposit'
    print('DEBUG: set today')
    date_def = dt.date.today()
    print('DEBUG: set new entry')
    new_entry = init_new_entry(context, date_def)
    print('DEBUG: set editable fields')
    editable_fields = ['amount', 'description', 'date_posted']
    pick = False

    while edit:
        print('DEBUG while edit')
        edit_items = [item for item in new_entry.items() if item[0] in editable_fields]
        print('DEBUG Check pick', pick)
        if not pick:
            star_beg()
            star_wall()
            
            for item in new_entry.items():
                star_wall(f'{txt:>10s}  {item[0]} = {item[1]}')
            
            star_wall(star_buffer())
            
            for index, item in enumerate(edit_items):
                star_wall(f'{index:>10d}) {item[0]} = {item[1]}')
            
            for index, item in [['c','Complete'], ['x', 'eXcape']]:
                star_wall(f'{index:>10s}) {item}')
            
            star_wall()
            star_end()
            pick = input('Pick an item to update: ')
            print('\n\n')
        if pick == '0':
            user_amount = input(f'Enter the {entry_type} amount: $')
            new_entry['amount'] = float(user_amount) * entry_sign
            pick = False
        elif pick == '1':
            user_description = input('Enter the {entry_type} description: ')
            new_entry['description'] = user_description
            pick = False
        elif pick == '2':
            user_date = input('Enter the date in format YYYY-MM-YY: ')
            new_entry['date_posted'] = user_date
            pick = False
        elif pick.lower() == 'c':
            for item in new_entry.items():
                new_entry[item[0]] = str(item[1])
            entries.append(new_entry)
            save(kwargs['users'], kwargs['accounts'], entries)
            get_cur_account_entries(context, entries)
            edit = False

        elif pick.lower() == 'x':
            edit = False
        else:
            print('DEBUG else')
            pick = False

        #target_amount = ''.join([char for char in user_amount if char in '0123456789.'])
        #num_decimals = sum([1 for char in target_amount if char == '.'])


def cl_view_balance(context, entries, **kwargs):
    func = 'cl_view_balance'    
    bug_note(verb='starting', func=func)
    # do some of the things
    # star_box('{:*^60s}'.format('  Viewing Balance  '))
    # print(current_entries)
#    print('\n\n')
    #print('\n\n{:*<5}{:5}Account {} has a current balance of ${:.2f}.\n{:*<5}{:5}({:d} entries)\n\n'.format(
    #    txt, txt, str(context['current_account_id']), balance, txt, txt, num_entries
    #))
    acct_text = str(context['current_account_id'])
    balance = get_cur_account_balance(context)
    bal_text = f'Account {acct_text} has a current balance of ${balance:.2f}.'
    num_entries = get_cur_account_entry_count(context)
    entries_text = f'{num_entries:d} total entries'
    star_box('{:*^60s}'.format('  Viewing Balance  '),star_buffer(),f'{bal_text:<60s}','',f'{entries_text:<60s}')
    bug_note(verb='ending', func=func)
    pause_it()
    

def cl_record_debit(context, entries, users, accounts, **kwargs):
    func = 'cl_record_debit'    
    bug_note(verb='starting', func=func)
    # do some of the things
    print((' ' * 10) + 'Recording Debit')
    input_entry(context=context, dci='d', entries=entries, users=users, accounts=accounts)
    bug_note(verb='ending', func=func)
    

def cl_record_credit(context, entries, users, accounts,  **kwargs):
    func = 'cl_record_credit'    
    bug_note(verb='starting', func=func)
    # do some of the things
    print((' ' * 10) + 'Recording Credit')
    input_entry(context=context, dci='c', entries=entries, users=users, accounts=accounts)
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
                #print('DEBUG found current user')
                #cur_user_info = get_cur_user_info(context['current_user_id'], users)
                current_user_info = context['current_user_info']
                #print(current_user_info)
                user_text=('Current user is {} - {} {}'.format(current_user_info['user_id'], 
                    current_user_info['first_name'], current_user_info['last_name']))
                #print(cur_user_info)
                if not context['current_account_id']:
                    #print('DEBUG no current account')
                    do_command = '5'
                    star_box(user_text)
                else:
                    #print('DEBUG found current account')
                    #cur_user_info = get_cur_user_info(context['current_user_id'], users)
                    current_account_info = context['current_account_info']
                    #print(current_account_info)
                    account_text = ('Current account is {} - {} accunt labeled \'{}\''.format(current_account_info['account_id'], 
                        current_account_info['account_type'], current_account_info['account_ref_name']))
                    #print(cur_user_info)      
                    star_box(user_text,account_text)      
            if not do_command:
                star_beg()
                for command, (fn, desc, show) in commands.items():
                    if show:
                        star_wall(f'{command:>10s}) {desc}')
                star_end()
                do_command = input('Enter the thing to do: ')
                print('\n\n')
            fn = commands.get(do_command.upper(), (unknown, "Unknown"))
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

