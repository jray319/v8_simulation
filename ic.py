import os
import sys

IC_LIST = ('load', 'store', 'keyed_load', 'keyed_store', 'binaryop')#, 'to_boolean'}
IC_STATES = ('UNINITIALIZED', 'PREMONOMORPHIC', 'MONOMORPHIC', 'POLYMORPHIC', 'MEGAMORPHIC', 'GENERIC')

class IC:
  def __init__(self, test_name, log_file):
    self.test_name = test_name
    self.log_file = log_file

def contain_ic_state(line):
  for state in IC_STATES:
    if state in line:
      return True
  return False

def read_ic_stat(log_file):
  ic_stat = {}
  state = 0
  ic_type = ''
  ic_state = ''
  with open(log_file, 'r') as f:
    for line in f:
      if state == 0:
        if line.rstrip('\n') in IC_LIST:
          ic_type = line.rstrip('\n')
          ic_stat[ic_type] = {}
          state = 1
      elif state == 1:
        if contain_ic_state(line):
          ic_state = line.strip(' ').split(':')[0]
          ic_stat[ic_type][ic_state] = [int(line.split(':')[1])]
          state = 2
        elif 'MISS' in line:
          state = 0
        elif 'Average Distance' in line:
          ic_stat[ic_type][ic_state].append(float(line.split(':')[1]))
      elif state == 2:
        ic_stat[ic_type][ic_state].append(int(line.split(':')[1]))
        state = 1
  return ic_stat

if __name__ == '__main__':
  ic_stats = {}
  for root, dirs, _ in os.walk(sys.argv[1]):
    for dir in dirs:
      test_name = dir
      #print test_name
      test_path = os.path.join(root, dir)
      for _, _, files in os.walk(test_path):
        for file in files:
          if file.startswith('simulation'):
            #print '    ' + file
            log_file = os.path.join(test_path, file)
            ic_stats[test_name] = read_ic_stat(log_file)

  for test in sorted(ic_stats):
    print '\n' + test
    print '|| ||' + '||'.join(IC_LIST) + '||'
    total = {}
    for ic_type in IC_LIST:
      temp_total = 0
      for ic_state in IC_STATES:
        temp_total += ic_stats[test][ic_type][ic_state][0]
      total[ic_type] = temp_total + 1
    for ic_state in IC_STATES:
      str_buffer = '||' + ic_state
      for ic_type in IC_LIST:
        str_buffer += '|' + str(ic_stats[test][ic_type][ic_state][0]) + ' (M:' + str(ic_stats[test][ic_type][ic_state][1])
        if len(ic_stats[test][ic_type][ic_state]) == 3:
          str_buffer += '/D:' + str(ic_stats[test][ic_type][ic_state][2])
        str_buffer += ')'
      str_buffer += '|'
      print str_buffer
      str_buffer = '|| '
      for ic_type in IC_LIST:
        str_buffer += '|' + str(100 * ic_stats[test][ic_type][ic_state][0] / total[ic_type]) + '%'
      str_buffer += '|'
      print str_buffer

