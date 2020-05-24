from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import asq

# Ignore SSL certificate errors
# ctx = ssl.create_default_context()
# ctx.check_hostname =  False
# ctx.verify_mode = ssl.CERT_NONE
#
# url = input('Enter Url - ')
# html = urlopen(url, context=ctx).read()
# soup = BeautifulSoup(html, "html.parser")
#
# # hero_list_skill_info = soup.find()
#
# print(soup)


from asq import query

## List of Query Initiators:
# query(iterable) 	         # Make a Queryable from any iterable
# integers(start, count) 	 # Make a Queryable sequence of consecutive integers
# repeat(value, count) 	     # Make a Queryable from a repeating value
# empty() 	                 # Make a Queryable from an empty sequence


students = [dict(firstname='Joe', lastname='Blogs', scores=[56, 23, 21, 89]),
            dict(firstname='John', lastname='Doe', scores=[34, 12, 92, 93]),
            dict(firstname='Jane', lastname='Doe', scores=[33, 94, 91, 13]),
            dict(firstname='Ola', lastname='Nordmann', scores=[98, 23, 98, 87]),
            dict(firstname='Kari', lastname='Nordmann', scores=[86, 37, 88, 87]),
            dict(firstname='Mario', lastname='Rossi', scores=[37, 95, 45, 18])]

print( query(students).where(lambda student: student['firstname'].startswith('J')) )

query_object = query(students).where(lambda student: student['firstname'].startswith('J'))
print(query_object.to_list())


## extract and compose student full names that start with J
print( query(students).where(lambda s: s['firstname'].startswith('J'))          # First find names that start with 'J'
                      .select(lambda s: s['firstname'] + ' ' + s['lastname'])   # Then select and concatenate (s)tudents first and last name
                      .to_list() )                                              # convert query object into a python structure
## ['Joe Blogs', 'John Doe', 'Jane Doe']



# QUERY NESTING
(query(students).order_by(lambda s: query(s['scores']).average())               # Order the query (s) by average of the scores
                .where(lambda student: student['firstname'].startswith('J'))    # For Students whose first name starts with 'J'
                .select(lambda s: s['firstname'] + ' ' + s['lastname'])         # Then get (s)tudents first and last name
                .to_list())                                                     # convert query output into python list



# LAMBDAS, to choose the selector
# SELECTOR, transforms all elements of sequence into a new form
numbers = [1, 67, 34, 23, 56, 34, 45]
print( query(numbers).select(lambda x: x**2).to_list() )



# FUNCTIONS, to choose selector
words = 'The quick brown fox jumped over the lazy dog'.split()
print(words)
# ['The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dog']
print( query(words).select(len).to_list() )
# [3, 5, 5, 3, 6, 4, 3, 4, 3]



# UNBOUND METHODS
# you can apply method of all objects of a type of class
words = ["the", "quick", "brown", "fox"]
print( query(words).select(str.upper).to_list() )   # uppercase all objects of class string
# ['THE', 'QUICK', 'BROWN', 'FOX']



# BOUND METHODS
# calling method linked to an instance of an object
numbers = [1, 67, 34, 23, 56, 34, 45]


class Multiplier(object):
    def __init__(self, factor=1):
        self.factor = factor


    def multiply(self, value):
        return self.factor * value


    def add(self, number1, number2):
        return number1 + number2



# storing Multiplier instance with factor value of 5
five_multiplier = Multiplier(factor= 5)
# storing method call of 'multiply' of the instance 'five_multiply'
times_by_five = five_multiplier.multiply
print( times_by_five )
# <bound method Multiplier.multiply of <__main__.Multiplier object at 0x0000000002F251D0>>

# calling .multiply method on each element in list and passing as value
print( query(numbers).select(times_by_five).to_list() )
# [5, 335, 170, 115, 280, 170, 225]


## BOUND METHODS W/TUPLES
number_tuples = [(1, 5), (6, 3), (4, 8), (9, 2), (7, 5)]
# instantiating object
add_numbers = Multiplier()
# storing instance method call
add_number_func = add_numbers.add
# create query object from list of tuples,
# apply function call to all elements of list,
# manually unpack tuple
# convert query object into list
print( query(number_tuples).select(lambda xy: add_number_func(number1= xy[0], number2= xy[1])).to_list() )



# SELECTOR FACTORIES

# Some selector patterns crop up very frequently and so asq provides some simple and concise selector factories for these cases. Selector factories are themselves functions which return the actual selector function which can be passed in turn to the query operator.

#     Selector factory 	Created selector function
#     k_(key) 	lambda x: x[key]
#     a_(name) 	lambda x: getattr(x, name)
#     m_(name, *args, **kwargs) 	lambda x: getattr(x, name)(*args, **kwargs)

iter()