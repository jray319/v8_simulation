# Built-in modules
import sys
import os
# Custom modules
import pin

if(len(sys.argv) > 1):
  if os.path.isfile(sys.argv[1]):
    pin.do_analysis(sys.argv[1])
  elif os.path.isdir(sys.argv[1]):
    for root, dirs, files in os.walk(sys.argv[1]):
      for file in files:
        #if file.endswith('.pin') or file.startswith('pin.out'):
        #  print file
        #  os.remove(os.path.join(root, file))
        if file.startswith('pintool'):
          pin.do_analysis(os.path.join(root, file), os.path.join(root, 'pin.out'))
  else:
    sys.exit('[ERROR] Invalid input.')
else:
  pin.do_analysis('pin.out')
