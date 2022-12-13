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
library.register_book(739200, 'Dom Quixote')
library.register_book(742122, 'Hamlet')
library.register_book(607815, 'Os Miseráveis')
library.register_book(112765, 'Odisseia')
library.register_book(296842, 'O Cortiço')
library.register_book(855413, 'A Revolução dos Bichos')
library.register_book(544907, 'Romeu e Julieta')
library.register_book(324478, 'Guerra e Paz')
library.register_book(118974, 'Orgulho e Preconceito')
library.register_book(679794, 'O Conto da Aia')
library.register_book(388214, 'Moby Dick')
library.register_book(765512, 'Édipo Rei')
library.register_book(300341, 'A Guerra dos Tronos')
library.register_book(999175, 'A Culpa é das Estrelas')



library.register_user('marcela', '1234')
library.register_user('matheus', '4321')
library.register_user('pablo', '1010')


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
library.return_book(1, 'marcela', '1234')
print(library.users.get('marcela'))
print(library.users)
print(library.bookshelf.getBook(153462))
print(library.loans.get(2))

library.bookshelf.InOrder()
print(library.users)
print(library.loans)





