string = '../../js/..'
count = 0
for i in string:
    if(i.isalnum()==False):
        count+=1
    else:
        break
string = string[count:]
print(string)