from __future__ import print_function
import re


fh = open("IN_view_SF_ACCOUNT.txt")
writeOut = open("OUT_view_SF_ACCOUNT.txt", 'w+')

#Define main regex
p = re.compile('\"[^ ]+\"')

for line in fh :
    words = line.split()

    #Check for busted table name using one-off regex substitution
    #for names wrapped as such: '"sf_contact"'
    #Write out to file and continue with next iteration of loop
    if len(words) > 1 and words[0] == "sql_table_name:" :
        fixed = re.sub('\"', '', words[1].upper())
        fixed = fixed.strip('\'')
        print (p.sub(fixed, line, count=1), end='', file=writeOut,)
        continue

    #Only parse LookML lines that begin with sql
    if len(words) > 1 and words[0] == "sql:" :
        #If the sql line _doesn't_ contain a quotation mark, it's OK.
        if "\"" not in line :
            print (line, end='', file=writeOut,)
            continue

        #Then search for all quote instances that need fixing
        hits = p.findall(line)

        #If only one element in hits list, substitue & write out
        if len(hits) == 1 :
            fixed = hits[0].strip('\"').upper()
            print (p.sub(fixed, line, count=1), end='', file=writeOut,)
        #Otherwise more than one hit, so make multiple substitutions
        else :
            tmp = ""
            for hit in hits :
                fixed = hit.strip('\"').upper()
                line = p.sub(fixed, line, count=1)
                tmp = line
            print (tmp, end='', file=writeOut,)
    #If line doesn't begin with sql, then just print to file
    else :
        print (line, end='', file=writeOut,)

print ("Yeah, dog! Wrote: ", writeOut)
fh.close()
writeOut.close()
