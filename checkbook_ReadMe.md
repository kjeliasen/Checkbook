# Python Project
## Command Line Checkbook Application

You will be creating a command line checkbook application that allows users to track their finances with a command line interface.

When run, the application should welcome the user, and prompt them for an action to take:

- view current balance
- add a debit (withdrawal)
- add a credit (deposit)
- exit

The application should persist between times that it is run, that is, if you run the application, add some credits, exit the application and run it again, you should still see the balance that you previously created. In order to do this, your application will need to store it's data in a text file. Consider creating a file where each line in the file represents a single transaction.

Here is an example of what using the program might look like:

`

    $ python checkbook.py

    ~~~ Welcome to your terminal checkbook! ~~~

    What would you like to do?

    1) view current balance
    2) record a debit (withdraw)
    3) record a credit (deposit)
    4) exit

    Your choice? 5
    Invalid choice: 5

    Your choice? 1

    Your current balance is $100.00.

    What would you like to do?

    1) view current balance
    2) record a debit (withdraw)
    3) record a credit (deposit)
    4) exit

    Your choice? 2

    How much is the debit? $50

    What would you like to do?

    1) view current balance
    2) record a debit (withdraw)
    3) record a credit (deposit)
    4) exit

    Your choice? 1

    Your current balance is $50.00.

    What would you like to do?

    1) view current balance
    2) record a debit (withdraw)
    3) record a credit (deposit)
    4) exit

    Your choice? 4

    Thanks, have a great day!
`

### Additional Features
Once you have finished the basic application (in no particular order),

- add a menu item that allows the user to view all historical transactions
assign categories to each transaction
- add a menu item to allow the user to view all the transactions in a given category
- provide the user with summary statistics about the transactions in each category
- keep track of the date and time that each transaction happened
- allow the user to view all the transactions for a given day
- make sure your list of previous transactions includes the timestamp for each
- allow the user to optionally provide a description for each transaction
- allow the user to search for keywords in the transaction descriptions, and show all the transactions that match the user's search term
- allow the user to modify past transactions
### Project Goals
- Working with a project specification
- Technical communication and collaboration
