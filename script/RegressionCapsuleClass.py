# python-3
# Regression Capsule Class
# In the same lines as ClassifierCapsuleClass
from sklearn.metrics import mean_absolute_error, mean_squared_error
from BaseCapsuleClass import BaseCapsule

class RegressionCapsule(BaseCapsule):
	def __init__(self,clfObj,methodName,splitPercent,train_x,train_y,test_x,test_y):
		BaseCapsule.__init__(self,clfObj,methodName,splitPercent,train_x,train_y,test_x,test_y)

	def evalClassifierPerf(self):
		self.abserr = mean_absolute_error(self.test_y,self.preds)
		self.sqerr = mean_squared_error(self.test_y,self.preds)

	def removeOutliers(self):
		idxs = [i for i in range(len(self.preds)) if self.preds[i] > 100 or self.preds[i] < 0]
		self.test_x.drop(self.test_x.index[idxs], inplace=True)
		self.test_y.drop(self.test_y.index[idxs], inplace=True)
		for i in self.preds:
			if i > 100 or i < 0:
				self.preds.remove(i)

	def runClf(self,computeMetrics=True,removeOutliers=True):
		BaseCapsule.runClf(self)
		
		if removeOutliers:
			self.removeOutliers()

		if computeMetrics:
			return self.evalClassifierPerf()
		else:
			return 0


    

