import sys
sys.path.append('./src')

from library import Library

library = Library()

library.register_book(153462, '1984')
library.register_book(756745, 'O Pequeno Príncipe')
library.register_book(165666, 'Marley & Eu')
library.register_book(978678, 'Senhor dos Anéis')
library.register_book(145323, 'Jogos Vorazes')
library.register_book(343442, 'Harry Potter')

library.register_user('marcela', '1234')
library.register_user('matheus', '4321')
library.register_user('pablo', '1010')

library.bookshelf.InOrder()
print(library.users)
print(library.loans)

print(library.login('marcela', '1234'))
print(library.login('marcela', '12345'))

print(library.check_book(153462))
print(library.check_book(153461))

print(library.check_available(153462))

library.loan_book(153462, 'marcela', '1234')
print(library.check_loan_info(1, 'marcela', '1234'))
library.loan_book(756745, 'marcela', '1234')
print(library.check_loan_info(2, 'marcela', '1234'))
library.renew_loan(2, 'marcela', '1234')
library.return_book(2, 'marcela', '1234')
print(library.loans)




