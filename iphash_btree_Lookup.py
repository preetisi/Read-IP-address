'''Author: Preeti singh, Carnegie Mellon University

Following file contains the Pseudo code for Aproach A) 

--------------------------------------*************************************--------------------------------'''

import iphash_btree

def iphash_lookup():

	'''read the input file'''
		f = open ('input.txt');
	'''use "contains()" function of the iphash_btree to find whether the stored \
	file represented by Btree contains the 
	ip_address given in the new input file'''
		file = open('previp.txt')
  		for line in file:
      			s = line.split()
      			ipfield = s[0].split('.')
      			'''convert ips into an integer for optimisation'''
      			ipnum = int(ipfield[0])*(1<<24) + int(ipfield[1])*(1<<16) +\
			int(ipfield[2])*(1<<8) + int(ipfield[3])
			
	
	'''If not found in the new input file then use "Awesome_hash()" function \
	to convert the ip_address of the new entry into hash_code'''
	 		if the ip address in input file is not in prev_ips: 
				hstr = awesome_hash(ipnum)
			
			file.write(s[0] + ' ' + hstr + '\n')
			outfile.write(hstr + ' ' + s[1] + '\n')
    			
			else:
				outfile.write(data[1] + ' ' + s[1] + '\n')
	'''use "bulkloading()" function of iphash_btree to insert all those new ipaddress which are not present'''
 	# This code will be very much similar to iphash.py. Here we are using our own implementation of 
	# B-tree rather than using SQLite. Although this would not effect the runtime significantly	
	
