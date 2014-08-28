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

EXTERNAL_DETAILS = (
  # api.cc
  "INVOKE_ACCESSOR_GETTER_CALLBACK",
  "INVOKE_FUNCTION_CALLBACK",
  # execution.cc
  "INVOKE_INTERRUPT_CALLBACK",
  # global-handles.cc
  "POST_GC",
  # heap.cc
  "GC_PROLOGUE_CALLBACK",
  "GC_EPILOGUE_CALLBACK",
  # isolate.cc
  "REPORT_FAILED_ACCESS_CHECK",
  "NAMED_ACCESS_CALLBACK",
  "INDEXED_ACCESS_CALLBACK",
  # runtime.cc
  "ALLOW_CODEGEN_CALLBACK",
  # log.cc
  "API_FUNCTION",
  "API_GETTER",
  # arguments.cc
  "FUNCTION_CALLBACK",
  # arguments.h
  "INDEXED_PROPERTY_ENUMERATOR_CALLBACK",
  "ACCESSOR_GETTER_CALLBACK",
  "NAMED_PROPERTY_QUERY_CALLBACK",
  "NAMED_PROPERTY_DELETER_CALLBACK",
  "INDEXED_PROPERTY_GETTER_CALLBACK",
  "INDEXED_PROPERTY_QUERY_CALLBACK",
  "INDEXED_PROPERTY_DELETER_CALLBACK",
  "NAMED_PROPERTY_SETTER_CALLBACK",
  "INDEXED_PROPERTY_SETTER_CALLBACK",
  "ACCESSOR_SETTER_CALLBACK"
  )

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
    self.num_external = {key: [] for key in EXTERNAL_DETAILS}

  def plot(self):
    # Read events.
    #self.read_simple_events()
    #self.read_external_events()
    self.read_events()
    self.scale(self.scale_factor)
    
    # Set the plot size.
    grid_row = 2
    grid_fig_col = self.num_simple_events / 2
    grid_legend_col = 8
    grid_col = grid_fig_col + grid_legend_col
    fig = plt.figure(figsize = (grid_col, grid_row * 6))

    # Plot simple events.
    plt.subplot2grid((grid_row, grid_col), (0, 0), colspan = grid_fig_col)
    x = np.arange(self.num_simple_events)
    # Prepare colors.
    colors = self.get_colors(len(V8_STATES_PLOT))
    plt.stackplot(x, [self.data[key] for key in V8_STATES_PLOT], colors = colors)
    # Set the axis limits.
    plt.xlim(xmin = 0, xmax = self.num_simple_events - 1)
    plt.ylim(ymin = 0, ymax = self.sampling_period)
    # Draw legend.
    plt.subplot2grid((grid_row, grid_col), (0, grid_col - 1))
    total_ticks = self.num_simple_events * self.sampling_period
    plt.table(cellText = [[str(100 * sum(self.data[key]) / total_ticks) + ' %'] for key in reversed(V8_STATES_PLOT)],
              rowLabels = V8_STATES_PLOT[::-1],
              rowColours = colors[::-1],
              colLabels = ['Ticks'],
              loc = 'center')
    plt.xticks([])
    plt.yticks([])
    
    # Plot external events.
    plt.subplot2grid((grid_row, grid_col), (1, 0), colspan = grid_fig_col)
    x = np.arange(self.num_external_events)
    # Prepare colors.
    colors = self.get_colors(len(EXTERNAL_DETAILS))
    plt.stackplot(x, [self.data_external[key] for key in EXTERNAL_DETAILS], colors = colors)
    # Set the axis limits.
    plt.xlim(xmin = 0, xmax = self.num_external_events - 1)
    plt.ylim(ymin = 0, ymax = self.sampling_period)
    # Draw legend.
    plt.subplot2grid((grid_row, grid_col), (1, grid_col - 3), colspan = 3)
    total_ticks = 0
    for key in EXTERNAL_DETAILS:
      total_ticks += sum(self.data_external[key])
    plt.table(cellText = [[str(100 * sum(self.data_external[key]) / total_ticks) + ' %', str(sum(self.num_external[key]))] for key in reversed(EXTERNAL_DETAILS)],
              rowLabels = EXTERNAL_DETAILS[::-1],
              rowColours = colors[::-1],
              colLabels = ['Ticks', '# of Times'],
              loc = 'center')
    plt.xticks([])
    plt.yticks([])
    
    # Finally draw the plot.
    plt.tight_layout()
    plt.show()
    #plt.savefig('plot.png')

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
        if len(tokens) != 2 * len(EXTERNAL_DETAILS) + 1 or not line.startswith('VMTimerEventExternal'):
          failed_lines += 1
          continue
        self.num_external_events += 1
        for i in range(0, len(EXTERNAL_DETAILS)):
          key = EXTERNAL_DETAILS[i]
          if key in self.data_external:
            self.data_external[EXTERNAL_DETAILS[i]].append(int(tokens[2 * i + 1]))
            self.num_external[EXTERNAL_DETAILS[i]].append(int(tokens[2 * (i + 1)]))
    print str(self.num_external_events) + ' samples analyzed.'
    print str(failed_lines) + ' samples failed.'

  def read_events(self):
    failed_lines = 0
    with open(self.v8_log_file, 'r') as f:
      state = 0
      simple_line = ''
      for line in f:
        tokens = line.rstrip('\n').split(',')
        if state == 0:
          if not line.startswith('VMTimerEventSimple'):
            state = 0
          elif len(tokens) != 10: 
            failed_lines += 1
            state = 1
          else:
            simple_line = line
            state = 2
        elif state == 1:
          state = 0
        elif state == 2:
          if len(tokens) != 2 * len(EXTERNAL_DETAILS) + 1 or not line.startswith('VMTimerEventExternal'):
            failed_lines += 1
            state = 0
          else:
            simple_tokens = simple_line.rstrip('\n').split(',')
            self.sampling_period = int(simple_tokens[1])
            self.num_simple_events += 1
            for i in range(0, len(V8_STATES)):
              key = V8_STATES[i]
              if key in self.data:
                self.data[V8_STATES[i]].append(int(simple_tokens[i + 2]))
            self.num_external_events += 1
            for i in range(0, len(EXTERNAL_DETAILS)):
              key = EXTERNAL_DETAILS[i]
              if key in self.data_external:
                self.data_external[EXTERNAL_DETAILS[i]].append(int(tokens[2 * i + 1]))
                self.num_external[EXTERNAL_DETAILS[i]].append(int(tokens[2 * (i + 1)]))
            state = 0
    print str(self.num_simple_events + self.num_external_events) + ' samples analyzed.'
    print str(failed_lines) + ' samples failed.'

  def scale(self, factor):
    self.sampling_period *= factor
    # Scale simple events.
    self.num_simple_events /= factor
    for i in range(0, len(V8_STATES)):
      for j in range(0, self.num_simple_events):
        temp = 0
        for k in range(0, factor):
          temp += self.data[V8_STATES[i]][j * factor + k]
        self.data[V8_STATES[i]][j] = temp
      self.data[V8_STATES[i]] = self.data[V8_STATES[i]][:self.num_simple_events]

    # Scale external events.
    self.num_external_events /= factor
    for i in range(0, len(EXTERNAL_DETAILS)):
      for j in range(0, self.num_external_events):
        temp = 0
        temp_num = 0
        for k in range(0, factor):
          temp += self.data_external[EXTERNAL_DETAILS[i]][j * factor + k]
          temp_num += self.num_external[EXTERNAL_DETAILS[i]][j * factor + k]
        self.data_external[EXTERNAL_DETAILS[i]][j] = temp
        self.num_external[EXTERNAL_DETAILS[i]][j] = temp_num
      self.data_external[EXTERNAL_DETAILS[i]] = self.data_external[EXTERNAL_DETAILS[i]][:self.num_external_events]
      self.num_external[EXTERNAL_DETAILS[i]] = self.num_external[EXTERNAL_DETAILS[i]][:self.num_external_events]

    for i in range(0, self.num_simple_events):
      #print str(self.data['EXTERNAL'][i])
      sum = 0
      for j in range(0, len(EXTERNAL_DETAILS)):
        sum += self.data_external[EXTERNAL_DETAILS[j]][i]
      #print (str(sum))
      if sum != self.data['EXTERNAL'][i]:
        print 'FUCK'
        #print str(self.data['EXTERNAL'][i])
        #print (str(sum))
    #sys.exit(0)

  def get_colors(self, num):
    colors = []
    cm = plt.get_cmap('Set1')
    for i in range(num):
      colors.append(cm(float(i) / num))
    return colors


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