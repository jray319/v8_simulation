# Built-in modules
import sys
import os
import numpy as np
from matplotlib import pyplot as plt

V8_STATES = ('JS',
             'GC',
             'COMPILER',
             'IC_RUNTIME',
             'RUNTIME',
             'OTHER',
             'EXTERNAL',
             'IDLE')

V8_STATES_PLOT = ('IDLE', 'EXTERNAL', 'JS', 'IC_RUNTIME', 'RUNTIME', 'COMPILER', 'GC', 'OTHER')

class Plotter():
  def __init__(self, v8_log_file):
    self.v8_log_file = v8_log_file
    self.num_samples = 0
    self.sampling_period = 0
    self.data = {'IDLE': [],
                 'EXTERNAL': [],
                 'JS': [],
                 'IC_RUNTIME': [],
                 'RUNTIME': [],
                 'COMPILER': [],
                 'GC': [],
                 'OTHER': []}

  def plot(self):
    self.analyze_simple()
    self.scale(100)
    fig, ax = plt.subplots()
    fig.set_size_inches(self.num_samples / 2, 5)
    x = np.arange(self.num_samples)
    stack_collection = ax.stackplot(x,
                                    self.data['IDLE'],
                                    self.data['EXTERNAL'],
                                    self.data['JS'],
                                    self.data['IC_RUNTIME'],
                                    self.data['RUNTIME'],
                                    self.data['COMPILER'],
                                    self.data['GC'],
                                    self.data['OTHER'])
    # Set the axis limits.
    plt.xlim(xmin = 0, xmax = self.num_samples - 1)
    plt.ylim(ymin = 0, ymax = self.sampling_period)
    # Make room for the legend.
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
    # Draw the legend.
    legend_rects = [plt.Rectangle((0, 0), 1, 1, fc = s.get_facecolor()[0]) for s in reversed(stack_collection)]
    total_ticks = self.num_samples * self.sampling_period
    ax.legend(legend_rects,
              [state + ' (' + str(100 * sum(self.data[state]) / total_ticks) + '%)' for state in reversed(V8_STATES_PLOT)],
              loc = 'center left',
              bbox_to_anchor=(1, 0.5))
    # Finally draw the plot.
    #plt.tight_layout()
    plt.savefig('plot.png')

  def analyze(self):
    with open(self.v8_log_file, 'r') as f:
      i = 0
      test = 0
      for line in f:
        i += 1
        if 'VMTimerEvent' in line:
          self.num_samples += 1
          if test != 0:
            print str(i)
            sys.exit(0)
          test = 7
          continue
        elif '100% EXTERNAL' in line:
          for key in self.data:
            test -= 1
            if key == 'EXTERNAL':
              self.data[key].append(self.sampling_period)
            else:
              self.data[key].append(0)
          continue
        key = line.split(':')[0].strip(' ')
        if key in self.data:
          test -= 1
          ticks = int(line.split('ticks,')[1].split('ticks')[0])
          self.data[key].append(ticks)
        elif key == 'Total':
          ticks = int(line.split('ticks,')[1].split('ticks')[0])
          self.sampling_period = ticks
    print str(self.num_samples) + ' samples analyzed.'
    for key in self.data:
      print '    ' + key + ': ' + str(len(self.data[key])) + ' samples'

  def analyze_simple(self):
    failed_lines = 0
    with open(self.v8_log_file, 'r') as f:
      for line in f:
        tokens = line.split(',')
        if len(tokens) != 10:
          failed_lines += 1
          continue
        self.sampling_period = int(tokens[1])
        self.num_samples += 1
        for i in range(0, len(V8_STATES)):
          key = V8_STATES[i]
          if key in self.data:
            self.data[V8_STATES[i]].append(int(tokens[i + 2]))
    print str(self.num_samples) + ' samples analyzed.'
    print str(failed_lines) + ' samples failed.'

  def scale(self, factor):
    self.num_samples /= factor
    self.sampling_period *= factor
    for i in range(0, len(V8_STATES)):
      for j in range(0, self.num_samples):
        temp = 0
        for k in range(0, factor):
          temp += self.data[V8_STATES[i]][j * factor + k]
        self.data[V8_STATES[i]][j] = temp
      self.data[V8_STATES[i]] = self.data[V8_STATES[i]][:self.num_samples]



if __name__ == '__main__':
  # Test the command line arguments.
  if len(sys.argv) < 2:
    sys.exit('[ERROR] No log file.')
  elif not os.path.isfile(sys.argv[1]):
    sys.exit('[ERROR] Invalid input.')

  plotter = Plotter(sys.argv[1])
  plotter.plot()