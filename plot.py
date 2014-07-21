# Built-in modules
import sys
import os
import numpy as np
from matplotlib import pyplot as plt

class Plotter():
  def __init__(self, v8_log_file):
  	self.v8_log_file = v8_log_file
  	self.num_samples = 0
  	self.data = {'EXTERNAL': [],
  	             'JS': [],
  	             'IC_RUNTIME': [],
  	             'RUNTIME': [],
  	             'COMPILER': [],
  	             'GC': [],
  	             'OTHER': []}

  def plot(self):
  	print self.v8_log_file
  	self.analyze()
  	print self.num_samples
  	print self.data
  	fig, ax = plt.subplots()
  	x = np.arange(self.num_samples)
  	stack_collection = ax.stackplot(x,
  		                            self.data['EXTERNAL'],
  		                            self.data['JS'],
  		                            self.data['IC_RUNTIME'],
  		                            self.data['RUNTIME'],
  		                            self.data['COMPILER'],
  		                            self.data['GC'],
  		                            self.data['OTHER'])
  	# Set the axis limits.
  	plt.xlim(xmin = 0, xmax = self.num_samples - 1)
  	plt.ylim(ymin = 0)
  	# Make room for the legend.
  	box = ax.get_position()
  	ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
  	# Draw the legend.
  	legend_rects = [plt.Rectangle((0, 0), 1, 1, fc = s.get_facecolor()[0]) for s in reversed(stack_collection)]
  	ax.legend(legend_rects,
  		      reversed(['EXTERNAL', 'JS', 'IC_RUNTIME', 'RUNTIME', 'COMPILER', 'GC', 'OTHER']),
  		      loc = 'center left',
  		      bbox_to_anchor=(1, 0.5))
  	#plt.legend(bbox_to_anchor=(1.05, 1), loc = 2, borderaxespad=0.)
  	# Finally draw the plot.
  	plt.show()

  def analyze(self):
  	with open(self.v8_log_file, 'r') as f:
  	  for line in f:
  	  	if 'VMTimerEvent' in line:
  	  	  self.num_samples += 1
  	  	key = line.split(':')[0].strip(' ')
  	  	if key in self.data:
  	  	  ticks = int(line.split('ticks,')[1].split('ticks')[0])
  	  	  self.data[key].append(ticks)


if __name__ == '__main__':
  # Test the command line arguments.
  if len(sys.argv) < 2:
  	sys.exit('[ERROR] No log file.')
  elif not os.path.isfile(sys.argv[1]):
  	sys.exit('[ERROR] Invalid input.')

  plotter = Plotter(sys.argv[1])
  plotter.plot()