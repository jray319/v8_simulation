# Built-in modules
import argparse
import subprocess
import os
import datetime
import sys
import operator
# Custom modules
import config
import which
#import vm_timer

def prepare_d8_args_new(default_args, benchmark_suite_dir, test, test_dir, args):
  ret = []
  # Prepare flags.
  ret += default_args
  if args.extra_v8_flags != None:
    ret += args.extra_v8_flags.split(' ')
  if args.vm_timer:
    v8_log = os.path.join(test_dir, args.v8_log)
    #ret += ['--log-vm-timer', '--log-lazy', '--logfile', v8_log]
    ret += ['--vm-timer']
  if args.count_ic:
    ret += ['--nocrankshaft', '--count-ic-native', '--vm-state-detail-ic-runtime']
  # Prepare files.
  base_js = os.path.join(benchmark_suite_dir, 'iacoma_base.js')
  test_js = []
  for root, dirs, files in os.walk(benchmark_suite_dir):
    for f in files:
      if f.startswith(test):
        test_js.append(os.path.join(benchmark_suite_dir, f))
  #print test_js
  #test_js = [os.path.join(benchmark_suite_dir, test + '.js')]

  if True:
    profile_file = os.path.join(test_dir, 'profile.js')
    with open(profile_file, 'w') as f:
      f.write('gc();\n')
      
      if os.path.isfile(base_js):
        f.write('load("' + base_js + '");\n')
      for tf in test_js:
        f.write('load("' + tf + '");\n') 
      f.write('if(typeof ' + args.setup_func + ' != "undefined") ' + args.setup_func + '();\n')

      # Warmup
      for _ in range(args.warmup):
        f.write(args.sim_func + '();\n')
      
      f.write('gc();\n')
      
      f.write('print("PROFILE BEGIN");\n')
      f.write('var start_clock_tick = %GetClockTick();\n')
      
      if args.pin:
        f.write('%EnterSimulation();\n')
        f.write('%BeginSimulation();\n')
      if args.vm_timer:
        f.write('%ResetVMTimer();\n')
        #f.write('%StartLogger();\n')
      
      for _ in (range(args.profile)):
        f.write(args.sim_func + '();\n')
      
      if args.pin:
        f.write('%EndSimulation();\n')
        f.write('%ExitSimulation();\n')
      if args.vm_timer:
        f.write('%PrintVMTimer();\n')

      f.write('var elapsed_clock_ticks = %GetClockTick() - start_clock_tick;\n')
      f.write('print("Elapsed Clock Ticks: " + elapsed_clock_ticks);\n')
      
      f.write('if(typeof ' + args.teardown_func + ' != "undefined") ' + args.teardown_func + '();\n')
    ret += ['-f', profile_file]
  return ret

# Prepare the arguments for D8.
# Create wrapper files for the simulation.
def prepare_d8_args(default_args, benchmark_suite_dir, test, test_dir, args):
  ret = []
  # Prepare flags.
  ret += default_args
  if args.extra_v8_flags != None:
    ret += args.extra_v8_flags.split(' ')
  if args.reload:
    ret.append('--new-context')
    if not args.keep_ic:
      ret.append('--send-idle-notification')
    ret += ['--prof', '--prof_lazy', '--log_snapshot_positions', '--logfile', v8_log]
  if args.vm_timer:
    v8_log = os.path.join(test_dir, args.v8_log)
    ret += ['--log-vm-timer', '--log-lazy', '--logfile', v8_log]
  # Prepare files.
  base_js = os.path.join(benchmark_suite_dir, 'iacoma_base.js')
  test_js = os.path.join(benchmark_suite_dir, test + '.js')
  if args.reload:
    warmup_file = os.path.join(test_dir, 'warmup.js')
    with open(warmup_file, 'w') as f:
      f.write('gc();\n')
      if os.path.isfile(base_js):
        f.write('load("' + base_js + '");\n')
      f.write('load("' + test_js + '");\n')
      f.write('if(typeof ' + args.setup_func + ' != "undefined") ' + args.setup_func + '();\n')
      f.write(args.sim_func + '();\n')
      f.write('if(typeof ' + args.teardown_func + ' != "undefined") ' + args.teardown_func + '();\n')
    for _ in range(args.warmup):
      ret += ['-f', warmup_file]
    profile_file = os.path.join(test_dir, 'profile.js')
    with open(profile_file, 'w') as f:
      f.write('gc();\n')
      if os.path.isfile(base_js):
        f.write('load("' + base_js + '");\n')
      f.write('load("' + test_js + '");\n')
      f.write('if(typeof ' + args.setup_func + ' != "undefined") ' + args.setup_func + '();\n')
      f.write('print("PROFILE BEGIN");\n')
      if args.pin:
        f.write('%EnterSimulation();\n')
        f.write('%BeginSimulation();\n')
      if args.vm_timer:
        f.write('%ResetVMTimer();\n')
        f.write('%StartLogger();\n')
      f.write(args.sim_func + '();\n')
      if args.pin:
        f.write('%EndSimulation();\n')
        f.write('%ExitSimulation();\n')
      if args.vm_timer:
        f.write('%PrintVMTimer();\n')
      f.write('if(typeof ' + args.teardown_func + ' != "undefined") ' + args.teardown_func + '();\n')
    for _ in range(args.profile):
      ret += ['-f', profile_file]
  else:
    #sys.exit('[ERROR] Simulation without --reload not yet supported.')
    profile_file = os.path.join(test_dir, 'profile.js')
    with open(profile_file, 'w') as f:
      f.write('gc();\n')
      if os.path.isfile(base_js):
        f.write('load("' + base_js + '");\n')
      f.write('load("' + test_js + '");\n')
      f.write('if(typeof ' + args.setup_func + ' != "undefined") ' + args.setup_func + '();\n')
      # Warmup
      for _ in range(args.warmup):
        f.write(args.sim_func + '();\n')
      f.write('gc();\n')
      f.write('print("PROFILE BEGIN");\n')
      if args.pin:
        f.write('%EnterSimulation();\n')
        f.write('%BeginSimulation();\n')
      if args.vm_timer:
        f.write('%ResetVMTimer();\n')
        f.write('%StartLogger();\n')
      f.write(args.sim_func + '();\n')
      if args.pin:
        f.write('%EndSimulation();\n')
        f.write('%ExitSimulation();\n')
      if args.vm_timer:
        f.write('%PrintVMTimer();\n')
      f.write('if(typeof ' + args.teardown_func + ' != "undefined") ' + args.teardown_func + '();\n')
    ret += ['-f', profile_file]
  return ret

# Create a command for subprocess.
def prepare_command(default_d8_args, benchmark_suite_dir, test, test_dir, args, config):
  command = []
  test_js = os.path.join(benchmark_suite_dir, test + '.js')
  #d8_args = prepare_d8_args(default_d8_args, benchmark_suite_dir, test, test_dir, args)
  d8_args = prepare_d8_args_new(default_d8_args, benchmark_suite_dir, test, test_dir, args)
  if args.pin:
    pintool_output = os.path.join(test_dir, 'pintool.out')
    command += [config.PIN] + config.PIN_ARGS + ['-t', config.PINTOOL] + config.PINTOOL_ARGS + ['-o', pintool_output, '--']
  command += [config.D8] + d8_args
  return command

# Argument parsing
parser = argparse.ArgumentParser(description='Run JavaScript simulation.')
parser.add_argument('--suite', dest='suite_name', type=str, required=True, help='benchmark suite name')
parser.add_argument('--pin', dest='pin', action='store_true', help='profile the dynamic instruction count using pin')
parser.add_argument('--vm-timer', dest='vm_timer', action='store_true', help='profile the execution time using the VM timer')
parser.add_argument('--count-ic', dest='count_ic', action='store_true', help='count ic accesses')
parser.add_argument('--v8-log', dest='v8_log', type=str, default='v8.log', help='the name of v8 log file')
parser.add_argument('--warmup', dest='warmup', type=int, default=3, help='the number of warmup iterations')
parser.add_argument('--profile', dest='profile', type=int, default=1, help='the number of profile iterations (recommended for a very short test)')
parser.add_argument('--repeat', dest='repeat', type=int, default=1, help='the number of repetition (recommended for a very short test)')
parser.add_argument('--reload', dest='reload', action='store_true', help='refresh the execution context between warmup iteration (i.e. mimic page reload in the browser)')
parser.add_argument('--keep-ic', dest='keep_ic', action='store_true', help='keep inline caches across page reloads (assumes --reload)')
parser.add_argument('--condor', dest='condor', action='store_true', help='run on condor')
parser.add_argument('--extra-v8-flags', dest='extra_v8_flags', type=str, default=None, help='extra v8 flags')
parser.add_argument('--sim-func', dest='sim_func', type=str, default='run_simulation', help='the name of the function to simulate')
parser.add_argument('--setup_func', dest='setup_func', type=str, default='setup_func', help='the name of the function for setup before the simulation')
parser.add_argument('--teardown_func', dest='teardown_func', type=str, default='teardown_func', help='the name of the function for teardown after the simulation')
args = parser.parse_args()
if not args.reload and args.keep_ic:
  sys.exit('[ERROR] --keep-ic cannot be set without --reload')
if args.condor:
  if which.which('condor') is None:
    sys.exit('[ERROR] condor is not found in the system.')

# Get full suite name.
if args.suite_name == 'jsbench':
  args.suite_name = 'jsbench-2012.1'
elif args.suite_name == 'sunspider':
  args.suite_name = 'sunspider-0.9.1'

# Set simulation function name correctly.
if 'sunspider' in args.suite_name:
  args.sim_func = 'runBenchmark'
elif 'octane' in args.suite_name:
  args.sim_func = 'run_func'

print args.suite_name

# Locate tests to run.
tests = []
benchmark_suite_dir = os.path.join('./benchmarks', args.suite_name)
benchmark_list_file = os.path.join(benchmark_suite_dir, 'LIST')
if not os.path.isfile(benchmark_list_file):
  sys.exit('[ERROR] LIST file missing.')
with open(benchmark_list_file, 'r') as benchmark_list:
  for line in benchmark_list:
    tests.append(line.rstrip('\n'))
#tests = ['amazon-chrome']
print tests

# Set up the directory to store results.
try:
  os.makedirs('./results')
except OSError:
  pass

# Create a directory for benchmark.
timestamp = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
result_dir = os.path.join('./results', args.suite_name + "_" + timestamp)
try:
  os.makedirs(result_dir)
except OSError:
  sys.exit('[ERROR] Output directory name conflicts.')

# Run tests.
v8_log_original = args.v8_log
vm_timer_output = {}
for test in tests:
  # Create a subdirectory for each test.
  test_dir = os.path.join(result_dir, test)
  try:
    os.makedirs(test_dir)
  except OSError:
    pass

  # Run simulation.
  for i in range(args.repeat):
    simulation_output = os.path.join(test_dir, 'simulation.out.' + str(i))
    args.v8_log = v8_log_original + '.' + str(i)
    with open(simulation_output, 'w') as f:
      command = prepare_command(config.D8_ARGS, benchmark_suite_dir, test, test_dir, args, config)
      if i == 0:
        print command
      subprocess.call(command, stdout = f)
    #if args.vm_timer and i == args.repeat - 1:
    #  vm_timer_output[test] = vm_timer.read_vm_timer_output(simulation_output)

#print '||Name||JS||GC||COMPILER||IC_RUNTIME||RUNTIME||OTHER||EXTERNAL||IDLE||'
#avg = [0] * 8
#for test in vm_timer_output:
#  print '||' + test + '|' + '|'.join(map(lambda x: str(x) + '%', vm_timer_output[test])) + '|'
#  avg = map(operator.add, avg, vm_timer_output[test])
#print '||average|' + '|'.join(map(lambda x: str(x / len(vm_timer_output)) + '%', avg)) + '|'
