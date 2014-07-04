# Built-in modules
import os
import common
import operator
# Custom modules
import v8

def read_log(v8_log, ticks):
  total_ticks = 0
  tick_line = ''
  print_line = False
  with open(v8_log, 'r') as f:
    for line in f:
      if line.startswith('runtime-function'):
        type = int(line.rstrip('\n').split(',')[1])
        type_name = v8.getTypeName(type)
        ticks[type_name] += 1
        if print_line:
          #print line
          print_line = False
        #elif type != 0:
          #print tick_line
          #print line
      if line.startswith('tick'):
        total_ticks += 1
        type = int(line.split(',')[6])
        if type != 0:
          #print line
          print_line = True
        tick_line = str(line)
  return total_ticks

def do_analysis(input, output = None):
  print input

  # Prepare the container.
  keys = ['UsefulWork'] + ['IC_' + type_name for type_name in v8.getInlinedCacheCallNames()]
  ticks = {}
  total_ticks = 0
  for key in keys:
    ticks[key] = 0

  # Read the log.
  if os.path.isdir(input):
    for item in os.listdir(input):
      full_path = os.path.join(input, item)
      if os.path.isfile(full_path) and item.startswith('v8.log'):
        #print '    Reading ' + item
        total_ticks += read_log(full_path, ticks)
  elif os.path.isfile(input):
    total_ticks += read_log(input, ticks)

  # Check if the log is valid.
  if total_ticks != sum([ticks[key] for key in keys]):
    print '    [ERROR] # of log messages mismatch.'
    print '            runtime: ' + str(sum([ticks[key] for key in keys]))
    print '            total_ticks: ' + str(total_ticks)
    return
  elif total_ticks == 0:
    print '    [ERROR] No sample.'
    return

  # Report
  report = []
  for type in sorted(ticks.iteritems(), key=operator.itemgetter(1), reverse=True):
    report_str = type[0] + ": " + str(type[1]) + '(' + str(100 * type[1] / total_ticks) + '%)'
    report.append(report_str)
  if output is None:
    for report_str in report:
      print '    ' + report_str
  else:
    runtime_total = total_ticks - ticks['UsefulWork']
    print_str = '    IC_Runtime: ' + str(100 * runtime_total / total_ticks) + '% (' + str(runtime_total) + ')'
    print print_str
    with open(output, 'w') as f:
      for report_str in report:
        f.write(report_str + '\n')
