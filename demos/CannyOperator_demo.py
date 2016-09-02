import sys
sys.path.append('/home/kai/github-workspace/python-practice/CVlib')
import CannyOperator as Canny
test = Canny.CannyOperator('../resources/Man.png')
test.demo()
