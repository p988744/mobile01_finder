import time

for i in range(1,100):
	fw = open('playground.txt','w')
	fw.write(str(i)+'\n')
	time.sleep(0.1)
	fw.close()