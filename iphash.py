'''Author: Preeti Singh, Computer Science Department, Carnegie Mellon University)'''

'''The program does an IP lookup of the batch of the users who sent us their
clicks and replaces the IP s with some sort of a hash'''

'''Following is the code for Approach C described in the Documentation (ReadMe_Compete.txt)'''

''' I am assuming Awesome_hash() function is already provided in the function'''
 
'''For Testing run this file using input.txt, pre_ips.txt'''

'''----------------------******************---------------------------------'''

import sqlite3
import random
import string

def awesome_hash(somestr):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) \
	for _ in range(10))

'''Build Connection to SQLite'''
conn = sqlite3.connect('iptable.db')
c = conn.cursor()
'''From this built database select column having ip_address'''
c.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='ips'")
tabl = c.fetchone()


if tabl is None:
  print("New ip_table with corresponsing hash created\n")
  '''create table for previously seen ips'''
  c.execute('''CREATE TABLE ips (addr int, hash text)''')
  file = open('previp.txt')
  for line in file:
      s = line.split()
      ipfield = s[0].split('.')
      '''convert ips into an integer for optimisation'''
      ipnum = int(ipfield[0])*(1<<24) + int(ipfield[1])*(1<<16) +\
		int(ipfield[2])*(1<<8) + int(ipfield[3])
      c.execute('''INSERT INTO ips(addr, hash) VALUES(?,?)''', (ipnum, s[1]))
  file.close()

file = open('previp.txt', 'a')
input = open('input.txt')
outfile = open('output.txt', 'w')

'''find if the ip_address in input.txt already exists in database or not'''
for line in input:
    s = line.split()
    ipfield = s[0].split('.')
    ipnum = int(ipfield[0])*(1<<24) + int(ipfield[1])*(1<<16) +\
	    int(ipfield[2])*(1<<8) + int(ipfield[3])
    c.execute('SELECT * FROM ips WHERE addr=?', (ipnum,))
    data = c.fetchone()
    ''' call Awesome_hash() if the ip_address is new'''
    if data is None:
	hstr = awesome_hash(ipnum)
	c.execute('''INSERT INTO ips(addr, hash) VALUES(?,?)''', (ipnum, hstr))
	file.write(s[0] + ' ' + hstr + '\n')
	outfile.write(hstr + ' ' + s[1] + '\n')
    else:
	outfile.write(data[1] + ' ' + s[1] + '\n')
	
input.close()
outfile.close()

conn.commit()
conn.close()
