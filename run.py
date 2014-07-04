# Built-in modules
import argparse
import subprocess
import os
import datetime
import sys
# Custom modules
import config
import which

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
  if args.sampling:
    v8_log = os.path.join(test_dir, args.v8_log)
    ret += ['--prof', '--prof_lazy', '--log_snapshot_positions', '--logfile', v8_log]
  # Prepare files.
  test_js = os.path.join(benchmark_suite_dir, test + '.js')
  if args.reload:
    warmup_file = os.path.join(test_dir, 'warmup.js')
    with open(warmup_file, 'w') as f:
      f.write('gc();\n')
      f.write('load("' + test_js + '");\n')
      f.write(args.sim_func + '();\n')
    for _ in range(args.warmup):
      ret += ['-f', warmup_file]
    profile_file = os.path.join(test_dir, 'profile.js')
    with open(profile_file, 'w') as f:
      f.write('gc();\n')
      f.write('load("' + test_js + '");\n')
      f.write('print("PROFILE BEGIN");\n')
      if args.pin:
        f.write('%EnterSimulation();\n')
        f.write('%BeginSimulation();\n')
      if args.sampling:
        f.write('%ProfilerResume();\n')
      if args.vm_time:
        f.write('%ResetVMTimer();\n')
      f.write(args.sim_func + '();\n')
      if args.pin:
        f.write('%EndSimulation();\n')
        f.write('%ExitSimulation();\n')
      if args.sampling:
        f.write('%ProfilerPause();\n')
      if args.vm_time:
        f.write('%PrintVMTimer();\n')
    for _ in range(args.profile):
      ret += ['-f', profile_file]
  else:
    #sys.exit('[ERROR] Simulation without --reload not yet supported.')
    profile_file = os.path.join(test_dir, 'profile.js')
    with open(profile_file, 'w') as f:
      f.write('gc();\n')
      f.write('load("' + test_js + '");\n')
      # Warmup
      for _ in range(args.warmup):
        f.write(args.sim_func + '();\n')
      f.write('gc();\n')
      f.write('print("PROFILE BEGIN");\n')
      if args.pin:
        f.write('%EnterSimulation();\n')
        f.write('%BeginSimulation();\n')
      if args.sampling:
        f.write('%ProfilerResume();\n')
      if args.vm_time:
        f.write('%ResetVMTimer();\n')
      f.write(args.sim_func + '();\n')
      if args.pin:
        f.write('%EndSimulation();\n')
        f.write('%ExitSimulation();\n')
      if args.sampling:
        f.write('%ProfilerPause();\n')
      if args.vm_time:
        f.write('%PrintVMTimer();\n')
    ret += ['-f', profile_file]
  return ret

# Create a command for subprocess.
def prepare_command(default_d8_args, benchmark_suite_dir, test, test_dir, args, config):
  command = []
  test_js = os.path.join(benchmark_suite_dir, test + '.js')
  d8_args = prepare_d8_args(default_d8_args, benchmark_suite_dir, test, test_dir, args)
  if args.pin:
    pintool_output = os.path.join(test_dir, 'pintool.out')
    command += [config.PIN] + config.PIN_ARGS + ['-t', config.PINTOOL] + config.PINTOOL_ARGS + ['-o', pintool_output, '--']
  command += [config.D8] + d8_args
  return command

# Argument parsing
parser = argparse.ArgumentParser(description='Run JavaScript simulation.')
parser.add_argument('--suite', dest='suite_name', type=str, required=True, help='benchmark suite name')
parser.add_argument('--pin', dest='pin', action='store_true', help='profile the dynamic instruction count using pin')
parser.add_argument('--sampling', dest='sampling', action='store_true', help='profile the execution time using the sampling profiler')
parser.add_argument('--vm-time', dest='vm_time', action='store_true', help='profile the execution time using the VM timer')
parser.add_argument('--v8-log', dest='v8_log', type=str, default='v8.log', help='the name of v8 log file')
parser.add_argument('--warmup', dest='warmup', type=int, default=3, help='the number of warmup iterations')
parser.add_argument('--profile', dest='profile', type=int, default=1, help='the number of profile iterations (recommended for a very short test)')
parser.add_argument('--repeat', dest='repeat', type=int, default=1, help='the number of repetition (recommended for a very short test)')
parser.add_argument('--reload', dest='reload', action='store_true', help='refresh the execution context between warmup iteration (i.e. mimic page reload in the browser)')
parser.add_argument('--keep-ic', dest='keep_ic', action='store_true', help='keep inline caches across page reloads (assumes --reload)')
parser.add_argument('--condor', dest='condor', action='store_true', help='run on condor')
parser.add_argument('--extra-v8-flags', dest='extra_v8_flags', type=str, default=None, help='extra v8 flags')
parser.add_argument('--sim-func', dest='sim_func', type=str, default='run_simulation', help='the name of the function to simulate')
args = parser.parse_args()
if not args.reload and args.keep_ic:
  sys.exit('[ERROR] --keep-ic cannot be set without --reload')
if args.condor:
  if which.which('condor') is None:
    sys.exit('[ERROR] condor is not found in the system.')

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
    # Process v8 log of sampling.
    if args.sampling:
      tick_processor_output = os.path.join(test_dir, 'sampling.out.' + str(i))
      with open(tick_processor_output, 'w') as f:
        subprocess.call([config.V8_TICK_PROCESSOR, '--snapshot-log=' + config.V8_SNAPSHOT_LOG, os.path.join(test_dir, args.v8_log)], stdout = f)
