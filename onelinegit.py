import sys
import os
message = ' '.join(sys.argv[1:])
command = 'git add .;git commit -m "'+message+'";git push origin master'
print(command)
os.system(command)
