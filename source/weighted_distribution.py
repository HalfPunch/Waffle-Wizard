from typing import Union


def weighted_distribution(weights: list, attribute_lists: list) -> list:
	"""
	:param weights: list of integer of float weights [w1, w2, w3]
	:param attribute_lists: list of attribute LISTS of integer of float values (len(attribute_list) == len(weight), and
	every row has the same amount of columns). If weights have 2 params (x, y) and we have 3 weights [w1, w2, w3],
	then attribute_list must look like [[x1, x2, x3], [y1, y2, y3]]
	:return: list summarised weight and equalised parameters
	"""
	if len(weights) != len(attribute_lists):
		raise ValueError("Lists have different lengths!")
	weighted_attributes = [0.0 for _ in range(len(attribute_lists[0]) + 1)]
	weighted_attributes[0] = sum(weights)
	if weighted_attributes[0] == 0:
		raise ValueError("All weights are ZERO")
	weight_portion_multipliers = list(map(lambda x: x / weighted_attributes[0], weights))
	for weight_id in range(len(weights)):
		for attribute_id in range(len(attribute_lists)):
			weighted_attributes[attribute_id + 1] += (
					attribute_lists[attribute_id][weight_id] * weight_portion_multipliers[weight_id])
	return weighted_attributes


