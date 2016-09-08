import math

def dataEntropy(attribute):
    import math
    frequencyEle = {}
    dataEntropy = 0

    for ele in attribute:
        frequencyEle[ele] = frequencyEle.get(ele,0) + 1

    for freq in frequencyEle.values():
        dataEntropy += (-freq/len(attribute)) * math.log(freq/len(attribute), 2) 

    return dataEntropy

def getNextEle(attribList):
    for ele in attribList:
        yield ele

def infoGain(attribute,targetAttribute):
    frequencyEle = {}
    subsetEntropy = 0.0
    nextVal = getNextEle(attribute)
    for i in range(len(attribute)):
        ele = next(nextVal)
        frequencyEle[ele] = frequencyEle.get(ele,0) + 1
    

    for element in frequencyEle.keys():
        subset = []
        weight = frequencyEle[element] / sum(frequencyEle.values())
        
        # Partition the target attribute on the basis of attribute groups
        nextVal = getNextEle(attribute)
        for i in range(len(attribute)):
            if next(nextVal) == element:
                subset.append(targetAttribute[i])

        subsetEntropy += dataEntropy(subset) * weight
        
    return (dataEntropy(targetAttribute) - subsetEntropy)