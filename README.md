# steemmonsters-transfer
A short script that provides the possibility to transfer bunches of cards from one account to another.

Various checks are executed before the transfer is made, but there is no final approval you need to give. So please be careful when you are using this.

## Usage : 
python3.6 transfer.py "fromaccountname" "toaccountname" "cards"

"fromaccountname" and "toaccountname" are the accounts you want to send cards from or to

"cards" specifies what cards you want to send, possible values here are 

- the colors of the splinters, so blue, red, black, green, white, gold(dragon) and neutral
- all, for simply transferring all cards

checks executed:

- are the cards on the market and therefore can not be transferred
- is the account name you are sending to existing on the steem blockchain

Example: python3.6 transfer jedigeiss bearded-benjamin all

This would transfer all cards from the account jedigeiss to the account bearded-benjamin

## Prerequisites:

You got to have beem installed on your computer or server, else this tool wont work. Additionally you also need to have the posting keys added to the beem wallet, this is possible by uttering the **command beempy addkey**


For questions you can find me on discord
