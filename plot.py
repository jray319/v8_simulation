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

EXTERNAL_DETAILS = ("InvokeAccessorGetterCallback", "InvokeFunctionCallback",
                    "FunctionCallbackArguments::Call", "WRITE_CALL_0", "WRITE_CALL_1", "WRITE_CALL_2", "WRITE_CALL_2_VOID",
                    "StackGuard::InvokeInterruptCallback",
                    "PostGarbageCollectionProcessing",
                    "Heap::PerformGarbageCollection_1", "Heap::PerformGarbageCollection_2",
                    "Isolate::ReportFailedAccessCheck", "Isolate::MayNamedAccess", "Isolate::MayIndexedAccess",
                    "CodeGenerationFromStringsAllowed")

V8_STATES_PLOT = ('IDLE', 'EXTERNAL', 'JS', 'IC_RUNTIME', 'RUNTIME', 'COMPILER', 'GC', 'OTHER')

class Plotter():
  def __init__(self, v8_log_file, scale_factor = 1):
    self.v8_log_file = v8_log_file
    self.scale_factor = int(scale_factor)
    self.num_simple_events = 0
    self.num_external_events = 0
    self.sampling_period = 0
    self.data = {'IDLE': [],
                 'EXTERNAL': [],
                 'JS': [],
                 'IC_RUNTIME': [],
                 'RUNTIME': [],
                 'COMPILER': [],
                 'GC': [],
                 'OTHER': []}
    self.data_external = {key: [] for key in EXTERNAL_DETAILS}

  def plot(self):
    self.read_simple_events()
    self.read_external_events()
    print self.data_external
    self.scale(self.scale_factor)
    # Set the plot size
    fig = plt.figure()
    grid_size_x = 2
    grid_size_y = self.num_simple_events / 2 + 4
    fig.set_size_inches(grid_size_y, grid_size_x * 5)
    #
    # Plot simple events
    #
    plt.subplot2grid((grid_size_x, grid_size_y), (0, 0), colspan = grid_size_y - 4)
    x = np.arange(self.num_simple_events)
    colors = plt.cm.BuPu(np.linspace(0, 0.5, len(V8_STATES_PLOT)))
    plt.stackplot(x, [self.data[key] for key in V8_STATES_PLOT], colors = colors)
    # Set the axis limits.
    plt.xlim(xmin = 0, xmax = self.num_simple_events - 1)
    plt.ylim(ymin = 0, ymax = self.sampling_period)
    # Legend
    plt.subplot2grid((grid_size_x, grid_size_y), (0, grid_size_y - 2), colspan = 2)
    plt.table(cellText = [[0] for key in V8_STATES_PLOT],
              rowLabels = V8_STATES_PLOT,
              rowColours = colors,
              colLabels = ['Ticks'],
              loc = 'center')
    plt.xticks([])
    plt.yticks([])
    #
    # Plot external events
    #
    plt.subplot2grid((grid_size_x, grid_size_y), (1, 0), colspan = grid_size_y - 4)
    x = np.arange(self.num_external_events)
    plt.stackplot(x, [self.data_external[key] for key in EXTERNAL_DETAILS])
    # Set the axis limits.
    plt.xlim(xmin = 0, xmax = self.num_external_events - 1)
    plt.ylim(ymin = 0, ymax = self.sampling_period)
    # Finally draw the plot.
    plt.tight_layout()
    plt.show()
    return
    # Make room for the legend.
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
    # Draw the legend.
    legend_rects = [plt.Rectangle((0, 0), 1, 1, fc = s.get_facecolor()[0]) for s in reversed(stack_collection)]
    total_ticks = self.num_simple_events * self.sampling_period
    ax.legend(legend_rects,
              [state + ' (' + str(100 * sum(self.data[state]) / total_ticks) + '%)' for state in reversed(V8_STATES_PLOT)],
              loc = 'center left',
              bbox_to_anchor=(1, 0.5))
    # Plot external events
    plt.subplot(1, 2, 2)
    fig.set_size_inches(self.num_simple_events / 2, 5)
    x = np.arange(self.num_simple_events)
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
    plt.xlim(xmin = 0, xmax = self.num_simple_events - 1)
    plt.ylim(ymin = 0, ymax = self.sampling_period)
    # Finally draw the plot.
    #plt.tight_layout()
    plt.savefig('plot.png')
    plt.show()

  def analyze(self):
    with open(self.v8_log_file, 'r') as f:
      i = 0
      test = 0
      for line in f:
        i += 1
        if 'VMTimerEvent' in line:
          self.num_simple_events += 1
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
    print str(self.num_simple_events) + ' samples analyzed.'
    for key in self.data:
      print '    ' + key + ': ' + str(len(self.data[key])) + ' samples'

  def read_simple_events(self):
    failed_lines = 0
    with open(self.v8_log_file, 'r') as f:
      for line in f:
        tokens = line.rstrip('\n').split(',')
        if len(tokens) != 10 or not line.startswith('VMTimerEventSimple'):
          failed_lines += 1
          continue
        self.sampling_period = int(tokens[1])
        self.num_simple_events += 1
        for i in range(0, len(V8_STATES)):
          key = V8_STATES[i]
          if key in self.data:
            self.data[V8_STATES[i]].append(int(tokens[i + 2]))
    print str(self.num_simple_events) + ' samples analyzed.'
    print str(failed_lines) + ' samples failed.'

  def read_external_events(self):
    failed_lines = 0
    with open(self.v8_log_file, 'r') as f:
      for line in f:
        tokens = line.rstrip('\n').split(',')
        if len(tokens) != 21 or not line.startswith('VMTimerEventExternal'):
          failed_lines += 1
          continue
        self.num_external_events += 1
        for i in range(0, len(EXTERNAL_DETAILS)):
          key = EXTERNAL_DETAILS[i]
          if key in self.data_external:
            self.data_external[EXTERNAL_DETAILS[i]].append(int(tokens[i + 1]))
    print str(self.num_external_events) + ' samples analyzed.'
    print str(failed_lines) + ' samples failed.'

  def scale(self, factor):
    self.num_simple_events /= factor
    self.sampling_period *= factor
    for i in range(0, len(V8_STATES)):
      for j in range(0, self.num_simple_events):
        temp = 0
        for k in range(0, factor):
          temp += self.data[V8_STATES[i]][j * factor + k]
        self.data[V8_STATES[i]][j] = temp
      self.data[V8_STATES[i]] = self.data[V8_STATES[i]][:self.num_simple_events]


if __name__ == '__main__':
  # Test the command line arguments.
  if len(sys.argv) < 2:
    sys.exit('[ERROR] No log file.')
  elif not os.path.isfile(sys.argv[1]):
    sys.exit('[ERROR] Invalid input.')

  if len(sys.argv) == 2:
    plotter = Plotter(sys.argv[1])
  elif len(sys.argv) == 3:
    plotter = Plotter(sys.argv[1], sys.argv[2])
  plotter.plot()