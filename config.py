import os

V8_ROOT = os.path.join('/home/jray319/Workspace/v8_jiho/')
#V8_ROOT = os.path.join('/home/jray319/Workspace/v8_wonsun/')
D8 = os.path.join(V8_ROOT, 'out/ia32.release/d8')
D8_ARGS = ['--allow-natives-syntax', '--expose_gc', '--nocrankshaft']
D8_ARGS += ['--init_new_space_size=65536', '--max_new_space_size=65536']
D8_ARGS += ['--object_literal_max_key=1000', '--fast_properties_max_key=1000']
D8_ARGS += ['--nocollect_maps', '--noflush_code', '--nocleanup_code_caches_at_gc', '--trace_gc']
D8_ARGS += ['--sticky-ic-runtime-vm-state']
V8_SNAPSHOT_LOG = os.path.join(V8_ROOT, 'out/ia32.release/obj.target/v8_snapshot/geni/snapshot.log')
V8_TICK_PROCESSOR = os.path.join(V8_ROOT, 'tools/linux-tick-processor')
# PIN
PIN = '/home/jray319/Workspace/pin-2.12-53271-gcc.4.4.7-ia32_intel64-linux/pin'
PIN_ARGS = ['-limit_code_cache', '268435456']
PINTOOL = '/home/jray319/Workspace/icount_check_insts.so'
PINTOOL_ARGS = ['-sim_marks', '-profile_checks']
