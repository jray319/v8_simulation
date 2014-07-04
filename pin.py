# Built-in modules
import common
import operator
# Custom modules
import v8

def getRuntimeOverhead(check_insts):
  total = 0
  for type in check_insts:
    if type.isdigit() and v8.isRuntimeOverhead(type):
      total += check_insts[type]
  return total

def getTotalOverhead(check_insts):
  total = 0
  for type in check_insts:
    if type.isdigit():
      total += check_insts[type]
  return total

def sum_insts(insts):
  sum = 0
  for type in insts:
  	if type.isdigit():
  	  sum += insts[type]
  return sum

def do_analysis(pin_log, output = None):
  print pin_log

  # Read the log file.
  total_insts = common.getAttribute(pin_log, 'threadInsts(0)')
  check_events = common.getHistAttribute(pin_log, 'checkEvents')
  check_insts = common.getHistAttribute(pin_log, 'checkInsts')

  # Check if it counted instrutions.
  if total_insts is 0:
    print '    [ERROR] No instruction.'
    return

  check_insts_aggregated = {}
  for type in v8.getAggregatedTypeNames():
  	check_insts_aggregated[type] = {}

  for type in check_insts:
  	if type.isdigit():
  	  check_insts_aggregated[v8.getAggregatedTypeName(int(type))][type] = check_insts[type]
  check_insts_aggregated['UsefulWork']['0'] = total_insts - getTotalOverhead(check_insts)

  check_insts_aggregated_percentage = {}
  for type in v8.getAggregatedTypeNames():
  	check_insts_aggregated_percentage[type] = 100 * sum_insts(check_insts_aggregated[type]) / total_insts

  report = []
  for type in v8.getAggregatedTypeNames():
  	report_str = type + ': ' + str(sum_insts(check_insts_aggregated[type])) + ' (' + str(check_insts_aggregated_percentage[type]) + '%)'
        report.append(report_str)
  	for subtype in sorted(check_insts_aggregated[type].iteritems(), key=operator.itemgetter(1), reverse=True):
  	  report_str = '    ' + v8.getTypeName(int(subtype[0])) + ': ' + str(check_insts_aggregated[type][subtype[0]])
          report.append(report_str)
  if output is None:
    for report_str in report:
      print report_str
  else:
    print_str = '    IC_Runtime: ' + str(check_insts_aggregated_percentage['IC_Runtime']) + '%'
    print print_str
    with open(output, 'w') as f:
      for report_str in report:
        f.write(report_str + '\n')
