# python-3
# Author: Sreejith Menon (smenon8@uic.edu)

# Base class for all classification activities.

class BaseCapsule:
	def __init__(self,clfObj,methodName,splitPercent,train_x,train_y,test_x,test_y):
		self.clfObj = clfObj
		self.methodName = methodName
		self.splitPercent = splitPercent
		self.train_x = train_x
		self.train_y = train_y
		self.test_x = test_x
		self.test_y = test_y
		self.preds = None

	def setTestAttrib(self,clsAttribStr,value):
		w = []
		if clsAttribStr not in dir(self):
			try:
				raise Exception('Exception : Classifier Attribute %s Unknown' %clsAttribStr)
			except Exception as inst:
				print(inst.args)
				sys.exit()
		elif clsAttribStr not in {'test_x','test_y'}:
			with warnings.catch_warnings(record=True) as w:
				wrng = "Classifier corrupt, trying to setting non-testing data variables using the set method."
				self.warningMsg = [self.WarningMsg] + [wrng]
				print(wrng)
		else:
			setattr(self,clsAttribStr,value)

		if len(w) >= 1:
			return -1
		else:
			return 0


	def runClf(self):
		self.clfObj.fit(self.train_x,self.train_y)
		self.preds = list(self.clfObj.predict(self.test_x))
		