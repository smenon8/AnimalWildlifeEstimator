# python-3
# Regression Capsule Class
# In the same lines as ClassifierCapsuleClass
from BaseCapsuleClass import BaseCapsule
class RegressionCapsule(BaseCapsule):
	def __init__(self,clfObj,methodName,splitPercent,train_x,train_y,test_x,test_y):
		BaseCapsule.__init__(self,clfObj,methodName,splitPercent,train_x,train_y,test_x,test_y)



    

