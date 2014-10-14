# Built-in modules
import sys
import os

def read_vm_timer_output(output_file):
  ret = []
  with open(output_file, 'r') as f:
  	for line in f:
  	  if line.startswith('    ') and not line.startswith('     '):
  	  	ret.append(int(line.split('(')[1].split('%')[0]))
  return ret