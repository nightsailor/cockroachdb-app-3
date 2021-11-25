from math import floor
import os
import random
import uuid
import urllib.parse

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from models import Account

seen_account_ids = []

def create_accounts(session, num):
    print("Creating new accounts...")
    new_accounts = []
    while num > 0:
        account_id = uuid.uuid4()
        account_balance = floor(random.random()*1_000_000)
        new_accounts.append(Account(id=account_id, balance=account_balance))
        seen_account_ids.append(account_id)
        print("Created new account with id {0} and balance {1}.".format(
            account_id, account_balance))
        num = num - 1
    session.add_all(new_accounts)


def transfer_funds_randomly(session, one, two):
    source = session.query(Account).filter(Account.id == one).first()
    dest = session.query(Account).filter(Account.id == two).first()
    print("Random account balances:\nAccount {0}: {1}\nAccount {2}: {3}".format(
        one, source.balance, two, dest.balance))

    amount = floor(source.balance/2)
    print("Transferring {0} from account {1} to account {2}...".format(
        amount, one, two))

    # Check balance of the first account.
    if source.balance < amount:
        raise "Insufficient funds in account {0}".format(one)
    else:
        source.balance -= amount
        dest.balance += amount

    print("Transfer complete.\nNew balances:\nAccount {0}: {1}\nAccount {2}: {3}".format(
        one, source.balance, two, dest.balance))


def delete_accounts(session, num):
    print("Deleting existing accounts...")
    delete_ids = []
    while num > 0:
        delete_id = random.choice(seen_account_ids)
        delete_ids.append(delete_id)
        seen_account_ids.remove(delete_id)
        num = num - 1

    accounts = session.query(Account).filter(Account.id.in_(delete_ids)).all()

    for account in accounts:
        print("Deleted account {0}.".format(account.id))
        session.delete(account)


def main():
    conn_string = config('CONNECTION_STRING', default='guess_me')
    try:
        db_uri = os.path.expandvars(conn_string)
        db_uri = urllib.parse.unquote(db_uri)
        psycopg_uri = db_uri.replace('postgresql://', 'cockroachdb://').replace('26257?', '26257/bank?')

        engine = create_engine(psycopg_uri)
    except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

    run_transaction(sessionmaker(bind=engine),
                    lambda s: create_accounts(s, 10))

    from_id = random.choice(seen_account_ids)
    to_id = random.choice([id for id in seen_account_ids if id != from_id])

    run_transaction(sessionmaker(bind=engine),
                    lambda s: transfer_funds_randomly(s, from_id, to_id))

    run_transaction(sessionmaker(bind=engine), lambda s: delete_accounts(s, 5))


if __name__ == '__main__':
    main()
