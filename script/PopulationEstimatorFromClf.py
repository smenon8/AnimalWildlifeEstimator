# python-3

# Population Estimator Implementation on predicted shared dataset. 
# Author: Sreejith Menon (smenon8@uic.edu)
# Script creation date: Sept 30, 2016


import MarkRecapHelper as MR
import pandas as pd
import json
import ClassiferHelperAPI as CH
import importlib
importlib.reload(CH)

def trainTestClf(train_data_fl,test_data_fl,clf,attribType,infoGainFl=None):
	# Create training data
	allAttribs = CH.genAllAttribs(train_data_fl,attribType,infoGainFl)
	train_data= CH.getMasterData(train_data_fl)
	
	print("Number of attributes : %i" %len(allAttribs))
	
	# Create testing data
	test_data= CH.getMasterData(test_data_fl)
	testObj = CH.createDataFlDict(test_data,allAttribs,0.8,'Test')

	testDf =  pd.DataFrame(testObj).transpose()
	attributes = testDf.columns[:len(allAttribs)]
	testDataFeatures = testDf[allAttribs]

	# Build classifier
	clfObj = CH.buildBinClassifier(train_data,allAttribs,0.0,80,clf)

	# Set testing data and run classifier
	clfObj.setTestAttrib('test_x',testDataFeatures)
	clfObj.runClf(computeMetrics=False)

	prediction_results = {list(clfObj.test_x.index)[i] : clfObj.preds[i] for i in range(len(clfObj.test_x.index))}    

	return clfObj, prediction_results

def estimatePopulation(clfObj,prediction_results,inExifFl,inGidAidMapFl,inAidFtrFl):
	df = pd.DataFrame(prediction_results,index=['share']).transpose().reset_index()
	df.columns = ['GID','share']
	df.to_csv("/tmp/PredictionResults.csv",index=False)

	days = {'2015-03-01' : 1,
        '2015-03-02' : 2 }

	# Entire population estimate (includes giraffes and zebras)
	nidMarkRecapSet = MR.genNidMarkRecapDict(inExifFl,
					inGidAidMapFl,
					inAidFtrFl,
					"/tmp/PredictionResults.csv",
					days,
					shareData='classifier')
	marks_all,recaptures_all,population_all = MR.applyMarkRecap(nidMarkRecapSet)
	print("Population of all animals = %f" %population_all)

	nidMarkRecapSet = MR.genNidMarkRecapDict(inExifFl,
					inGidAidMapFl,
					inAidFtrFl,
					"/tmp/PredictionResults.csv",
					days,
					filterBySpecies='zebra_plains',
					shareData='classifier')
	marks_z,recaptures_z,population_z = MR.applyMarkRecap(nidMarkRecapSet)
	print("Population of zebras = %f" %population_z)

	nidMarkRecapSet = MR.genNidMarkRecapDict(inExifFl,
					inGidAidMapFl,
					inAidFtrFl,
					"/tmp/PredictionResults.csv",
					days,
					filterBySpecies='giraffe_masai',
					shareData='classifier')
	marks_g,recaptures_g,population_g = MR.applyMarkRecap(nidMarkRecapSet)
	print("Population of giraffes = %f" %population_g)

	return {'all' : population_all , 
			'zebras' : population_z , 'giraffes' : population_g, 
			'shared_images_count' : int(sum(clfObj.preds))}


def __main__():
	clfTypes = ['bayesian','logistic','svm','dtree','random_forests']
	attribTypes = ['sparse','non_sparse','non_zero','abv_mean']

	estimates = []
	for clf in clfTypes:
	    for attribType in attribTypes:
	        print("Classifier : %s" %clf)
	        print("Attribute selection method : %s" %attribType)
	        clfObj,predResults = trainTestClf("../FinalResults/ImgShrRnkListWithTags.csv",
                     "../data/full_gid_aid_ftr_agg.csv",
                     clf,
                     attribType,
                     "../data/infoGainsExpt2.csv")
	        thisObjhead = {'Classifier' : clf , 'Attribute' : attribType}
	        thisObj = estimatePopulation(clfObj,predResults,
	        				"../data/imgs_exif_data_full.json",
							"../data/full_gid_aid_map.json",
							"../data/full_aid_features.json")

	        estimates.append({**thisObjhead,**thisObj})
	        print()
	        print()

	with open("/tmp/populationEstimates.json","w") as jsonFl:
		json.dump(estimates,jsonFl,indent=4)

if __name__ == "__main__":
	__main__()