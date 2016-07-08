from sklearn.metrics import classification_report,accuracy_score,f1_score,precision_score,recall_score,roc_auc_score,mean_absolute_error, mean_squared_error,zero_one_loss,roc_curve

# write logic to calculate ROC curve

class ClassifierCapsule:
    def __init__(self,clfObj,methodName,splitPercent,train_x,train_y,test_x,test_y):
        self.clfObj = clfObj
        self.methodName = methodName
        self.splitPercent = splitPercent
        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y
        self.preds = None
        self.predProbabs = None
        self.predScores = None
        self.accScore = None
        self.f1Score = None
        self.precision = None
        self.recall = None
        self.auc = None
        self.abserr = None
        self.sqerr = None 
        self.zerooneloss = None
        self.roccurve = None


    def runClf(self):
        self.clfObj.fit(self.train_x,self.train_y)
        self.preds = list(self.clfObj.predict(self.test_x))
        self.predProbabs = self.clfObj.predict_proba(self.test_x)[:,1]
        self.evalClassifierPerf()

    def evalClassifierPerf(self):
        self.accScore = accuracy_score(self.test_y,self.preds)
        self.f1Score = f1_score(self.test_y,self.preds)
        self.precision = precision_score(self.test_y,self.preds)
        self.recall = recall_score(self.test_y,self.preds)
        self.auc = roc_auc_score(self.test_y,self.predProbabs) # intakes predicition probabilities
        self.abserr = mean_absolute_error(self.test_y,self.preds)
        self.sqerr = mean_squared_error(self.test_y,self.preds)
        self.zerooneloss = zero_one_loss(self.test_y,self.preds)

    def __str__(self):
        keys = ['splitPercent', 'accScore', 'abserr', 'zerooneloss','f1Score', 'precision', 'auc', 'sqerr', 'methodName', 'accScore', 'recall']

        printableDict = {key : self.__dict__[key] for key in keys}

        return str(printableDict)