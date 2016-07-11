with open('A.txt') as a:
	contentA = set(a.split)
    
with open('B.txt') as b:
	contentB = set(b)
    
print(contentA - contentB)
print(contentB)