import os

with open('data.txt', 'r') as f:
	content = f.read()

print(len(content))

file = open('newdata.txt', 'w')

c = 0


while(c < len(content)):
	print(str(c) + ' / ' + str(len(content)))
	try:
		if(content[c] == '\n' and content[c + 1] == '\n'):
			content = content[:c] + content[(c+1):]
			c -= 1
	except IndexError:
		break
	c += 1

content.replace('\'\'', '\"')

file.write(content)
file.close()
		

