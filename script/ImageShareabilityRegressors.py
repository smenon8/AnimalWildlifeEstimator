# python-3
# Author Name : Sreejith Menon (smenon8@uic.edu)
import ClassiferHelperAPI as CH
import numpy as np
import pandas as pd
import plotly.plotly as py
from collections import Counter
import csv
import plotly.graph_objs as go
import RegressionCapsuleClass as RgrCls

def plot(rgrObj,arr,arr_min,title,flNm,range,errorBar = True):
    trace1 = go.Scatter(
        x = list(rgrObj.preds),
        y = list(rgrObj.test_y),
        error_y = dict(
            type='data',
            symmetric = False,
            array = arr,
            arrayminus = arr_min,
            visible=errorBar
        ),
        mode = 'markers'
    )

    layout= go.Layout(
        title= title,
        xaxis= dict(
            title= 'Predicted Share Rate',
            ticklen= 5,
            zeroline= False,
            gridwidth= 2,
            range=[-5,110]
        ),
        yaxis=dict(
            title= 'Actual Share rate',
            ticklen= 5,
            gridwidth= 2,
            #range=range
        )
    )
    
    data = [trace1]

    fig = dict(data=data,layout=layout)
    a = py.iplot(fig,filename=flNm)
    
    return a

def runRgr(methodName,attribType):
    if attribType == "beauty":
        inpData = pd.DataFrame.from_csv("../data/BeautyFtrVector_GZC.csv")
        inpData.reindex(np.random.permutation(inpData.index))
        y = inpData['Proportion']
        inpData.drop(['Proportion'],1,inplace=True)
        train_x, test_x, train_y, test_y = CH.train_test_split(inpData, y, test_size = 0.4)
        rgr = CH.getLearningAlgo(methodName,{'fit_intercept':True})
    
        rgrObj = RgrCls.RegressionCapsule(rgr,methodName,0.8,train_x,train_y,test_x,test_y)
        
    else:
        train_data_fl = "../FinalResults/ImgShrRnkListWithTags.csv"
        infoGainFl = "../data/infoGainsExpt2.csv"
        allAttribs = CH.genAllAttribs(train_data_fl,attribType,infoGainFl)

        rgrObj = CH.buildRegrMod(train_data_fl,allAttribs,0.6,methodName,kwargs={'fit_intercept':True})
    
    rgrObj.runRgr(computeMetrics=True,removeOutliers=True)
    
    x = [i for i in range(len(rgrObj.preds))]
    errors = [list(rgrObj.test_y)[i] - list(rgrObj.preds)[i] for i in range(len(rgrObj.preds))]
    arr = [-1 * errors[i] if errors[i] < 0 else 0 for i in range(len(errors)) ]
    arr_min = [errors[i] if errors[i] > 0 else 0 for i in range(len(errors)) ]
    return rgrObj,arr,arr_min

def plotWithErrBars(attribTypes, rgrAlgoTypes):
	embedCodes = []
	for attrib in attribTypes:
	    code = []
	    for alg in rgrAlgoTypes:
	        rgrObj, arr,arr_min = runRgr(alg,attrib)
	        title = "%s regression results using %s attributes" %(alg,attrib)
	        flNm = "%s_regession_%s_attributes_%s" %(alg,attrib,str(True))
	        a = plot(rgrObj,arr,arr_min,title,flNm,[-100,200],errorBar = True)
	        code.append(a.embed_code)    
	    embedCodes.append(code)

	for code in embedCodes:
		print(code)
		print()

def plotWithoutErrBars(attribTypes, rgrAlgoTypes):
	embedCodes = []
	for attrib in attribTypes:
	    code = []
	    for alg in rgrAlgoTypes:
	        rgrObj, _, _ = runRgr(alg,attrib)
	        print("Absolute error for %s using %s : %f" %(alg,attrib,rgrObj.abserr))
	        print("Mean Squared error for %s using %s : %f" %(alg,attrib,rgrObj.sqerr))
	        title = "%s regression results using %s attributes" %(alg,attrib)
	        flNm = "%s_regession_%s_attributes_%s" %(alg,attrib,str(False))
	        a = plot(rgrObj,[],[],title,flNm,[-10,110],errorBar = False)
	        code.append(a.embed_code)
	    embedCodes.append(code)

	for code in embedCodes:
		print(code)
		print()

def plotResiduals(attribTypes, rgrAlgoTypes):
	embedCodes = []
	for attrib in attribTypes:
		code = []
		for alg in rgrAlgoTypes:
			rgrObj, _, _ = runRgr(alg,attrib)
			x_data = rgrObj.preds
			y_data = rgrObj.residues
			title = "%s regression residues using %s attributes" %(alg,attrib)
			flNm = "%s_regession_%s_attributes_%s" %(alg,attrib,"residues")
			# Create a trace
			trace = go.Scatter(
			    x = x_data,
			    y = y_data,
			    mode = 'markers'
			)
			layout= go.Layout(
		        title= title,
		        xaxis= dict(
		            title= 'Predicted Share Rate',
		            ticklen= 5
		        ),
		        yaxis=dict(
		            title= 'Residues',
		            ticklen= 5
		        )
		    )

			data = [trace]

			# Plot and embed in ipython notebook!
			fig = dict(data=data,layout=layout)
			a = py.iplot(fig,filename=flNm)
			
			code.append(a.embed_code)    
		
		embedCodes.append(code)

	for code in embedCodes:
		print(code)
		print()


def __main__():
	# attribTypes = ['sparse', 'non_sparse', 'non_zero', 'abv_mean']
	attribTypes = ['beauty']
	rgrAlgoTypes = ['linear', 'ridge', 'lasso', 'elastic_net', 'svr', 'linear_svr', 'dtree_regressor']

	# plotWithErrBars(attribTypes, rgrAlgoTypes)
	# print("\n\n\n\n\n")
	# plotWithoutErrBars(attribTypes, rgrAlgoTypes)

	plotResiduals(attribTypes, rgrAlgoTypes)
if __name__ == "__main__":
	__main__()