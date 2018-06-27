import numpy as np
import matplotlib.pyplot as plt

import csv, os

plt.figure()
plt.title("Multi-grad steps performance on reacher env (continuous rewards)")

plt.xlabel("Grad steps")
plt.ylabel("Returns")
algos = ["ours","0_flr","0_metaitr","trpo"]

location_dir = "/home/rosen/maml_rl/data/local/R7DOF-EVAL/"

results = {}

for algo in algos:
    with open(location_dir+"summary_"+algo+".csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        i =0
        row = None
        grad_steps, means, stds = [], [], []
        for row in reader:
            i+=1
            if i == 1:
                mean_idx = row.index('AverageReturn')
                std_idx = row.index('ReturnStd')
            else:
                grad_steps.append(i-1)
                means.append(float(row[mean_idx]))
                stds.append(float(row[std_idx]))
        results[algo] = (grad_steps,np.array(means),np.array(stds))

algo = algos[0]

for i, algo in enumerate(algos):
    color = ['red','green','blue', 'purple'][i]
    plt.fill_between(results[algo][0], results[algo][1]- results[algo][2],results[algo][1]+ results[algo][2], alpha=0.1, color=color)
    plt.plot(results[algo][0], results[algo][1], 'o-', color=color, label=algo if algo != 'trpo' else 'maml+trpo')


plt.legend(loc="lower right")
plt.savefig(location_dir+"r7dof_chart.png")