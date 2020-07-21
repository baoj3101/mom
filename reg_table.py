import re
import argparse
import sys

DEBUG = False

def table (in_file):
    # read file in lines
    with open(in_file) as fh:
        lines = fh.readlines()

    table_dic = {}

    inInput = 0
    ver = ''
    regIdx = ''    

    for line in lines:
        if match := re.search('INPUT SECTION', line):
            inInput = 1

        if match := re.search('OUTPUT SECTION', line):
            break   # exit when see OUTPUT SECTION

        if match := re.search('SymNamePtr\s*=\s*(\w+)', line):    # left columns (V1, V2, etc)
            ver = match.group(1)
            if DEBUG:
                print (line, ver)      

        if match := re.search('PhysicalRegType\s*=\s*(\d+)', line):
            if match.group(1) == '0':
                regIdx = 'R'
            elif match.group(1) == '7':
                regIdx = 'I'   
            if DEBUG:
                print(line, regIdx)   

        if match := re.search('PhysicalRegIdx\s*=\s*(\d+)', line):    # ritght column (R0, R1, R2, etc)
            regIdx += match.group(1)
            if DEBUG:
                print (line, regIdx)

        if match := re.search('PhysicalSwizzles', line):  # .x .y .z .w
            v = ver
            r = regIdx
            x = line.split()
            attribute = x[-1]
            if attribute == '_':
                continue
        
            r += '.' + attribute
            if match := re.search('\[(\w)\]', line):
                v += '.' + match.group(1)
            
            if DEBUG:
                print(v)
                print(r)

            table_dic[v] = r    # input values into dictionary
        
        # if match := re.search('PhysicalSwizzles[(\w+)]\s*=\s(\w+)', line):
        #     if match.group(2) == 'w':
            if attribute == 'w':
                num = int(regIdx[1]) + 1
                regIdx = regIdx[0] + str(num)
    
    return table_dic


filename = sys.argv[1]

print(table(filename))
