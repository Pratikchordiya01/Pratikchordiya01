import matplotlib.pyplot as plt
import csv
import datetime as dt

dtime = dt.time()
now = dt.datetime.now()
now.isoformat()
x = []
y = []
z = []
with open('stallgraph.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[1]))
        y.append(int(row[2]))
        z.append(int(row[0]))
plt.plot(x,y, label='Loaded from file!')
plt.plot(x,z, label='Loaded from file!')
plt.xlabel('x')
plt.ylabel('y-stall')
plt.title('Interesting Graph\nCheck it out')
plt.savefig(f'{now}.png')
plt.legend()
#plt.show()
