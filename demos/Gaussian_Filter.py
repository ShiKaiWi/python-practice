import sys
sys.path.append('/home/kai/github-workspace/python-practice/CVlib')

import GaussianFilter as GF

test = GF.GaussianFilter('../resources/Man.png',sigma=2,windsize=11)
test.demo()
