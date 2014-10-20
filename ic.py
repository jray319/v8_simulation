import os
import sys

IC_LIST = ('load', 'store', 'keyed_load', 'keyed_store', 'binaryop', 'to_boolean')
IC_STATES = ('UNINITIALIZED', 'PREMONOMORPHIC', 'MONOMORPHIC', 'POLYMORPHIC', 'MEGAMORPHIC', 'GENERIC')

SUNSPIDER_TOTAL_INSTS = {
  'crypto-sha1':36021802,
  'bitops-bits-in-byte':41752401,
  '3d-morph':372468869,
  'date-format-tofte':39090683,
  'math-partial-sums':140430260,
  'access-fannkuch':115712242,
  'string-validate-input':85224487,
  'bitops-nsieve-bits':106812690,
  'string-base64':60425059,
  'access-nsieve':38901723,
  'string-tagcloud':70347807,
  'regexp-dna':32112100,
  'string-fasta':67683614,
  'controlflow-recursive':20978020,
  'bitops-3bit-bits-in-byte':37405535,
  'string-unpack-code':109651134,
  'access-nbody':95735020,
  '3d-cube':84003777,
  '3d-raytrace':68172193,
  'access-binary-trees':19992412,
  'math-cordic':80397057,
  'date-format-xparb':35254923,
  'math-spectral-norm':41319763,
  'crypto-md5':35136396,
  'crypto-aes':44286978,
  'bitops-bitwise-and':35034133
}

JSBENCH_TOTAL_INSTS = {
  'google-chrome':555777970,
  'yahoo-opera':319045273,
  'google-opera':740145348,
  'facebook-chrome':830551708,
  'amazon-chrome':239888700,
  'twitter-webkit':605111265,
  'yahoo-firefox':318873332,
  'google-firefox':713000375,
  'amazon-opera':250534326
}

OCTANE_TOTAL_INSTS = {
  'deltablue':14327490,
  'navier-stokes':377379864,
  'pdfjs':502459780,
  'mandreel':5569411020,
  'zlib':22105988104,
  'gbemu':901821164,
  'regexp':179117988,
  'crypto':278157843,
  'earley-boyer':163118461,
  'raytrace':89254940,
  'splay':7869264,
  'box2d':519985961,
  'code-load':43986521,
  'richards':7466074,
  'typescript':4893777142
}

TOTAL_INSTS = {
  'sunspider':SUNSPIDER_TOTAL_INSTS,
  'jsbench':JSBENCH_TOTAL_INSTS,
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

  suite_name = 'jsbench'
  str_buffer = '||Test||'
  str_buffer += '||'.join(['Total Insts', \
                           'Monomorphic', 'Polymorphic', 'Megamorphic', 'Generic', 'Total IC' \
                          ])
  str_buffer += '|'
  print str_buffer
  for test in sorted(ic_stats):
    monomorphic_total = ic_stats[test]['load']['MONOMORPHIC'][0] \
                      + ic_stats[test]['store']['MONOMORPHIC'][0] \
                      + ic_stats[test]['keyed_load']['MONOMORPHIC'][0] \
                      + ic_stats[test]['keyed_store']['MONOMORPHIC'][0]
    polymorphic_total = ic_stats[test]['load']['POLYMORPHIC'][0] \
                      + ic_stats[test]['store']['POLYMORPHIC'][0]
    megamorphic_total = ic_stats[test]['load']['MEGAMORPHIC'][0] \
                      + ic_stats[test]['store']['MEGAMORPHIC'][0]
    generic_total = ic_stats[test]['keyed_load']['GENERIC'][0] \
                  + ic_stats[test]['keyed_store']['GENERIC'][0]

    monomorphic_cost = 5
    polymorphic_cost = 3 + 2 * ic_stats[test]['load']['POLYMORPHIC'][2]
    megamorphic_cost = 30
    generic_cost = 300

    monomorphic_cost_total = monomorphic_cost * monomorphic_total
    polymorphic_cost_total = int(polymorphic_cost * polymorphic_total)
    megamorphic_cost_total = megamorphic_cost * megamorphic_total
    generic_cost_total = generic_cost * generic_total

    cost_total = monomorphic_cost_total + polymorphic_cost_total + megamorphic_cost_total + generic_cost_total

    '''str_buffer = '||' + test + '|'
    str_buffer += '|'.join(map(str, ['N/A', \
                                     monomorphic_cost_total, \
                                     polymorphic_cost_total, \
                                     megamorphic_cost_total, \
                                     generic_cost_total, \
                                     cost_total]))
    str_buffer += '|'
    print str_buffer
    sys.exit(1)'''

    total_insts = TOTAL_INSTS[suite_name][test]

    monomorphic_cost_total_percent = str(round(100.0 * monomorphic_cost_total / total_insts, 2)) + '%'
    polymorphic_cost_total_percent = str(round(100.0 * polymorphic_cost_total / total_insts, 2)) + '%'
    megamorphic_cost_total_percent = str(round(100.0 * megamorphic_cost_total / total_insts, 2)) + '%'
    generic_cost_total_percent = str(round(100.0 * generic_cost_total / total_insts, 2)) + '%'

    cost_total_percent = str(round(100.0 * cost_total / total_insts, 2)) + '%'

    str_buffer = '||' + test + '|'
    str_buffer += '|'.join(map(str, [total_insts, \
                                     monomorphic_cost_total_percent, \
                                     polymorphic_cost_total_percent, \
                                     megamorphic_cost_total_percent, \
                                     generic_cost_total_percent, \
                                     cost_total_percent]))
    str_buffer += '|'
    print str_buffer
    
    
    #print str(5 * 100 * monomorphic_total / TOTAL_INSTS[suite_name][test])

  sys.exit(1)

  suite_name = 'octane'
  str_buffer = '||Test||'
  str_buffer += '||'.join(['Total Insts', \
                           'Mono Load', 'Poly Load', 'Mega Load', \
                           'Mono Store', 'Poly Store', 'Mega Store', \
                           'Mono KLoad', 'Generic KLoad', \
                           'Mono KStore', 'Generic KStore'])
  str_buffer += '|'
  print str_buffer
  for test in sorted(ic_stats):
    str_buffer = '||' + test + '|'
    str_buffer += '|'.join(map(str, [TOTAL_INSTS[suite_name][test], \
    #str_buffer += '|'.join(map(str, ['N/A', \
                                     ic_stats[test]['load']['MONOMORPHIC'][0], ic_stats[test]['load']['POLYMORPHIC'][0], ic_stats[test]['load']['MEGAMORPHIC'][0], \
                                     ic_stats[test]['store']['MONOMORPHIC'][0], ic_stats[test]['store']['POLYMORPHIC'][0], ic_stats[test]['store']['MEGAMORPHIC'][0], \
                                     ic_stats[test]['keyed_load']['MONOMORPHIC'][0], ic_stats[test]['keyed_load']['GENERIC'][0], \
                                     ic_stats[test]['keyed_store']['MONOMORPHIC'][0], ic_stats[test]['keyed_store']['GENERIC'][0] \
                                    ]))
    str_buffer += '|'
    print str_buffer
    
    #monomorphic_total = ic_stats[test]['load']['MONOMORPHIC'][0] + ic_stats[test]['store']['MONOMORPHIC'][0] + ic_stats[test]['keyed_load']['MONOMORPHIC'][0] + ic_stats[test]['keyed_store']['MONOMORPHIC'][0]
    #print str(5 * 100 * monomorphic_total / TOTAL_INSTS[suite_name][test])

  sys.exit(1)

  suite_name = 'octane'
  #suite_name = 'sunspider'
  #suite_name = 'jsbench'
  # Instruction counts
  for test in sorted(ic_stats):
    print '\n' + test
    total_insts = TOTAL_INSTS[suite_name][test]
    print 'Total Insts: ' + str(total_insts)
    polymorphic_load = ic_stats[test]['load']['POLYMORPHIC'][0]
    polymorphic_load_distance = ic_stats[test]['load']['POLYMORPHIC'][2]
    polymorphic_store = ic_stats[test]['store']['POLYMORPHIC'][0]
    polymorphic_store_distance = ic_stats[test]['store']['POLYMORPHIC'][2]
    megamorphic_load = ic_stats[test]['load']['MEGAMORPHIC'][0]
    megamorphic_store = ic_stats[test]['store']['MEGAMORPHIC'][0]
    generic_keyed_load = ic_stats[test]['keyed_load']['GENERIC'][0]
    generic_keyed_store = ic_stats[test]['keyed_store']['GENERIC'][0]
    print 'Polymorphic Load: ' + str(polymorphic_load)
    print '    Polymorphic Load Distance: ' + str(polymorphic_load_distance)
    print 'Polymorphic Store: ' + str(polymorphic_store)
    print '    Polymorphic Store Distance: ' + str(polymorphic_store_distance)
    print 'Megamorphic Load: ' + str(megamorphic_load)
    print 'Megamorphic Store: ' + str(megamorphic_store)
    print 'Generic KeyedLoad: ' + str(generic_keyed_load)
    print 'Generic KeyedStore: ' + str(generic_keyed_store)
    polymorphic_load_cost = 2 * (polymorphic_load_distance - 1)
    polymorphic_store_cost = 2 * (polymorphic_store_distance - 1)
    megamorphic_load_cost = 30
    megamorphic_store_cost = 30
    generic_keyed_load_cost = 300
    generic_keyed_store_cost = 400
    maximum_reduction = int(polymorphic_load * polymorphic_load_cost \
                          + polymorphic_store * polymorphic_store_cost \
                          + megamorphic_load * megamorphic_load_cost \
                          + megamorphic_store * megamorphic_store_cost \
                          + generic_keyed_load * generic_keyed_load_cost
                          + generic_keyed_store * generic_keyed_store_cost)
    print 'Maximum Reduction: ' + str(maximum_reduction) + ' (' + str(round(100.0 * maximum_reduction / total_insts, 2)) + '%)'

  sys.exit(1)

  # Instruction counts
  for test in sorted(ic_stats):
    print '\n' + test
    total_insts = TOTAL_INSTS[suite_name][test]
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

