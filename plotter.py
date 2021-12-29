#TODO: violin plots
import time
import matplotlib.pyplot as plt
import seaborn as sns
from protopost import protopost_client as ppcl

HOST = "http://localhost:8080"
RESULTS = lambda: ppcl(HOST)

sns.set_theme()
plt.ion()
fig = plt.figure()


while True:
  fig.clear()
  plt.tight_layout()
  # .clear()
  results = RESULTS()
  fig.suptitle(f"N={len(results)}")
  #bw=.2 for bumpier violins
  #TODO: make y axis range the same on all graphs
  # print(results)
  # results = results[:100]
  #assume all results have the same param/metric list
  params, metrics = [results[0][0].keys(), results[0][1].keys()]
  #for now, just plot params vs accuracy
  metric = "accuracy"
  first_ax = None
  for i, param in enumerate(params):
    ax = plt.subplot(1, len(params), i+1)
    ax.set_title(param)
    x = [s[0][param] for s in results]
    y = [s[1][metric] for s in results]
    ax2 = sns.violinplot(x=x, y=y, palette="Set2", scale="count", inner="quartile")
    if first_ax is None:
      first_ax = ax
    else:
      ax.sharey(first_ax)
      ax.set_yticklabels([])

  # plt.show()
  plt.draw()
  plt.pause(1)
  # time.sleep(1)
  # ax.clear()
