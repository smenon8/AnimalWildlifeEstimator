import math

def calc_data_entropy(attribute):

    frequency_ele = {}
    data_entropy = 0

    for ele in attribute:
        frequency_ele[ele] = frequency_ele.get(ele, 0) + 1

    for freq in frequency_ele.values():
        data_entropy += (-freq/len(attribute)) * math.log(freq/len(attribute), 2) 

    return data_entropy

def get_next_ele(attrib_list):
    for ele in attrib_list:
        yield ele

def info_gain(attribute, target_attribute):
    frequency_ele = {}
    subset_entropy = 0.0
    next_val = get_next_ele(attribute)
    for i in range(len(attribute)):
        ele = next(next_val)
        frequency_ele[ele] = frequency_ele.get(ele, 0) + 1


    for element in frequency_ele.keys():
        subset = []
        weight = frequency_ele[element] / sum(frequency_ele.values())

        # Partition the target attribute on the basis of attribute groups
        next_val = get_next_ele(attribute)
        for i in range(len(attribute)):
            if next(next_val) == element:
                subset.append(target_attribute[i])

        subset_entropy += calc_data_entropy(subset) * weight

    return (calc_data_entropy(target_attribute) - subset_entropy)
