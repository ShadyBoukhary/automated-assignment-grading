# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"(?i)(answer)\s*[=:][\s&$%#]*(\d+[.]?\d*|[\w\s][^\n]+)"

test_str = ("Answer = 1.0\n"
	"Answer=1.0\n"
	"answer = 1.0\n"
	"Answer =1.0\n"
	"Answer:1.0\n"
	"Answer : 1.0\n"
	"Answer :  1.0\n"
	"Answer: 1.0\n"
	"Answer :1.0\n"
	"Answer :   3234.98234\n"
	"aNswer : 53452\n"
	"answer = $1.0\n"
	"answer = $ 1.0\n"
	"answer = rshxhnggfg\n"
	"answer = rshxhnggfg fdf\n"
	"answer = sfsdf dsfkls dgjdf gjkdfg jkdfgkj 2345 23452 3\n"
	"answer = 1\n"
	"answer : 356.3\n\n\n"
	"Name: Christopher Alexis\n"
	"Course : CS 1044, Section 101, Spring 2019, Dr.Johnson\n"
	"Purpose : The purpose of this program is to ask the user how many of each\n"
	"ticket type will be purchased and then display an invoice that will show the \n"
	"subtotal of all tickets purchased, the tax charged, and the overall total.\n\n"
	"Please enter the number of P1, P2, P3, P4, P5, P6 tickets\n"
	"you would like respectively. After each entry please press enter.\n"
	"P1: 23\n"
	"P2: 65\n"
	"P3: 21\n"
	"P4: 94\n"
	"P5: 23\n"
	"P6: 43\n"
	"Subtotal :$9350.00\n"
	"Tax :$771.38\n"
	"answer :$10121.38")

matches = re.finditer(regex, test_str)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.

