import os
import sys

IC_LIST = ('load', 'store', 'keyed_load', 'keyed_store', 'binaryop', 'to_boolean')
IC_STATES = ('UNINITIALIZED', 'PREMONOMORPHIC', 'MONOMORPHIC', 'POLYMORPHIC', 'MEGAMORPHIC', 'GENERIC')

OCTANE_TOTAL_INSTS = {
  'box2d':519969543,
  'code-load':43975462,
  'crypto':278157110,
  'deltablue':14330799,
  'earley-boyer':163118067,
  'mandreel':5569496040,
  'navier-stokes':377376589,
  'pdfjs':502708610,
  'raytrace':89258366,
  'regexp':179137069,
  'richards':7465899,
  'splay':7879398
}

TOTAL_INSTS = {
  'octane':OCTANE_TOTAL_INSTS
}

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
        elif 'Average Distance' in line:
          ic_stat[ic_type][ic_state][2] = float(line.split(':')[1])
      elif state == 2:
        ic_stat[ic_type][ic_state].append(int(line.split(':')[1]))
        ic_stat[ic_type][ic_state].append(0)
        if ic_state == 'GENERIC':
          state = 0
        else:
          state = 1
  return ic_stat

if __name__ == '__main__':
  ic_stats = {}
  if os.path.isfile(sys.argv[1]):
    ic_stats[sys.argv[1]] = read_ic_stat(sys.argv[1])
  else:
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

  # Instruction counts
  for test in sorted(ic_stats):
    print '\n' + test
    total_insts = TOTAL_INSTS['octane'][test]
    print 'Total Insts: ' + str(total_insts)
    polymorphic_load = ic_stats[test]['load']['POLYMORPHIC'][0]
    polymorphic_load_distance = ic_stats[test]['load']['POLYMORPHIC'][2]
    megamorphic_load = ic_stats[test]['load']['MEGAMORPHIC'][0]
    generic_keyed_load = ic_stats[test]['keyed_load']['GENERIC'][0]
    print 'Polymorphic Load: ' + str(polymorphic_load)
    print 'Polymorphic Load Distance: ' + str(polymorphic_load_distance)
    print 'Megamorphic Load: ' + str(megamorphic_load)
    print 'Generic KeyedLoad: ' + str(generic_keyed_load)
    polymorphic_load_cost = 2 * (polymorphic_load_distance - 1)
    megamorphic_load_cost = 30
    generic_keyed_load_cost = 500
    maximum_reduction = int(polymorphic_load * polymorphic_load_cost + megamorphic_load * megamorphic_load_cost + generic_keyed_load * generic_keyed_load_cost)
    print 'Maximum Reduction: ' + str(maximum_reduction) + ' (' + str(round(100.0 * maximum_reduction / total_insts, 2)) + '%)'

  sys.exit(1)

  # Instruction counts
  for test in sorted(ic_stats):
    print '\n' + test
    total_insts = TOTAL_INSTS['octane'][test]
    print 'Total Insts: ' + str(total_insts)
    monomorphic_load = ic_stats[test]['load']['MONOMORPHIC'][0]
    polymorphic_load = ic_stats[test]['load']['POLYMORPHIC'][0]
    polymorphic_load_distance = ic_stats[test]['load']['POLYMORPHIC'][2]
    print 'Monomorphic Load: ' + str(monomorphic_load)
    print 'Polymorphic Load: ' + str(polymorphic_load)
    print 'Polymorphic Load Distance: ' + str(polymorphic_load_distance)
    monomorphic_load_ic_insts = monomorphic_load * 5
    polymorphic_load_ic_insts = int(polymorphic_load * (3 + 2 * polymorphic_load_distance))
    load_ic_insts = monomorphic_load_ic_insts + polymorphic_load_ic_insts
    print 'Monomorphic LoadIC instructions: ' + str(monomorphic_load_ic_insts)
    print 'Polymorphic LoadIC instructions: ' + str(polymorphic_load_ic_insts)
    print 'LoadIC instructions: ' + str(load_ic_insts) + ' (' + str(round(100.0 * load_ic_insts / total_insts, 2)) + '%)'
    maximum_reduction = int(polymorphic_load * 2 * (polymorphic_load_distance - 1))
    print 'Maximum Reduction: ' + str(maximum_reduction) + ' (' + str(round(100.0 * maximum_reduction / total_insts, 2)) + '%)'

  sys.exit(1)

  # CSV output
  for test in sorted(ic_stats):
    print '\n' + test
    print ',' + ','.join(IC_LIST)
    total = {}
    for ic_type in IC_LIST:
      temp_total = 0
      for ic_state in IC_STATES:
        temp_total += ic_stats[test][ic_type][ic_state][0]
      total[ic_type] = temp_total + 1
    for ic_state in IC_STATES:
      # Access
      str_buffer = ic_state + ' Access'
      for ic_type in IC_LIST:
        str_buffer += ',' + str(ic_stats[test][ic_type][ic_state][0])
      print str_buffer
      # Percentage
      str_buffer = ic_state + ' Percentage'
      for ic_type in IC_LIST:
        str_buffer += ',' + str(100 * ic_stats[test][ic_type][ic_state][0] / total[ic_type]) + '%'
      print str_buffer
      # Miss
      str_buffer = ic_state + ' Miss'
      for ic_type in IC_LIST:
        str_buffer += ',' + str(ic_stats[test][ic_type][ic_state][1])
      print str_buffer
      # Distance
      str_buffer = ic_state + ' Distance'
      for ic_type in IC_LIST:
        if len(ic_stats[test][ic_type][ic_state]) == 3:
          str_buffer += ',' + str(ic_stats[test][ic_type][ic_state][2])
        else:
          str_buffer += ',N/A'
      print str_buffer
  sys.exit(1)

  # Wiki markup output
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

