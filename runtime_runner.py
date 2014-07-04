# Built-in modules
import sys
import os
# Custom modules
import runtime

if(len(sys.argv) > 1):
  root_path = sys.argv[1]
  if os.path.isdir(root_path):
    for item in os.listdir(root_path):
      full_path = os.path.join(root_path, item)
      if os.path.isdir(full_path):
        #runtime.do_analysis(full_path)
        runtime.do_analysis(full_path, os.path.join(root_path, 'v8.out'))
  else:
    runtime.do_analysis(root_path)
else:
  pin.do_analysis('[ERROR] Input missing.')
