_author_ = 'Ioannis';
'''
print();


previousResults = [0];
index = 0;
base = 4;
power = 0;

f = open("O.txt", mode='w');

while True:
    try:
        result = math.pow(base, power);
        if(index==len(previousResults)):
            previousResults.append(result);
        elif(previousResults[index]<result):
            previousResults[index] = result;
        power=power+1;
    except OverflowError:
        print(base, " : ", power, " : ", previousResults[index]);
        s = (base, " : ", power, " : ", previousResults[index])
        f.write(str(s));
        base=base+1;
        power = 10
    if base > 2000:
        break;
        
f.close();'''