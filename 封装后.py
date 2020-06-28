#!/usr/bin/env python
# -*- coding: utf-8 -*-

#@Time: 2020/6/26 11:03
#@Project: ML
#@Author: 孤小绵羊

# Apriori算法

"""

由于Apriori算法假定项集中的项是按字典序排序的，而集合本身是无序的，所以我们在必要时需要进行set和list的转换；

由于要使用字典（support_data）记录项集的支持度，需要用项集作为key，而可变集合无法作为字典的key，因此在合适时机应将项集转为固定集合frozenset。

支持度

置信度



"""


class apriori_algorithm:

	# 算法初始化

	def __init__(self, minSupport, dataSet):

		self.minSupport = minSupport  # 最小支持度

		self.dataSet = dataSet  # 数据集

	# 加载数据集

	def loaddata(self):

		return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

	# 生成单个物品的项集列表

	def generateC1(self, dataSet):

		C1 = []  # 用于存放生成的单个物品的项集列表

		# 遍历数据集

		for data in dataSet:

			for item in data:

				if [item] not in C1:
					C1.append([item])

		C1.sort()

		return C1

	# 遍历数据集，和Ck对比，计数

	def generateLk_by_Ck(self, dataSet, Ck, minSupport, support_data):

		"""

		   Generate Lk by executing a delete policy from Ck.

		   Args:

			   data_set: 数据集

			   Ck: A set which contains all all frequent candidate k-itemsets.

			   min_support: The minimum support.

			   support_data: A dictionary. The key is frequent itemset and the value is support.

		   Returns:

			   Lk: A set which contains all all frequent k-itemsets.

		   """

		D = map(set, dataSet)

		C = map(frozenset, Ck)

		C1 = list(C)  # 关于map对象的遍历，在内循环中遍历完最后一个元素后，再次访问时会放回空列表，所以外循环第二次进入的时候是空的，需要将其转为list处理

		countData = dict()

		for d in D:  # set遍历

			for c in C1:

				if c.issubset(d):  # 子集判断，并非元素判断

					if c not in countData.keys():  # 将集合作为字典的键使用,c为[]型

						countData[c] = 1



					else:

						countData[c] += 1

		numItems = float(len(list(dataSet)))

		returnList = []

		supportData = dict()

		# 遍历前面得到的计数字典

		for key in countData:

			support = countData[key] / numItems

			if support >= minSupport:
				returnList.insert(0, key)  # insert() 函数用于将指定对象插入列表的指定位置

				support_data[key] = support

		return returnList

	def generate_L(self, dataSet, k, min_support):

		"""

		   Generate all frequent itemsets.

		   Args:

			   data_set:数据集

			   k: 频繁项集中含有的最多的元素

			   min_support: 最小支持度

		   Returns:

			   L: 出现的所有频繁项集

			   support_data: 每个频繁项集对应的支持度

		   """

		support_data = {}

		C1 = self.generateC1(dataSet)

		L1 = self.generateLk_by_Ck(dataSet, C1, min_support, support_data)

		Lksub1 = L1.copy()

		L = []

		L.append(Lksub1)

		for i in range(2, k + 1):
			Ci = self.generateCK(Lksub1, i)

			Li = self.generateLk_by_Ck(dataSet, Ci, min_support, support_data)

			Lksub1 = Li.copy()

			L.append(Lksub1)

		return L, support_data

	# generateCK 候选频繁项集产生   参数 Lk频繁项集，k:项集元素个数

	def generateCK(self, Lk, k):

		Ck = set()

		len_Lk = len(list(Lk))

		list_Lk = list(Lk)

		for i in range(len_Lk):

			for j in range(1, len_Lk):

				l1 = list(list_Lk[i])

				l2 = list(list_Lk[j])

				l1.sort()

				l2.sort()

				if l1[0:k - 2] == l2[0:k - 2]:

					Ck_item = list_Lk[i] | list_Lk[j]

					if self.isCk(Ck_item, list_Lk):
						Ck.add(Ck_item)

				# Ck.add(Ck_item)

		return Ck

	# 频繁项集判断

	def isCk(self, Ck_item, list_Lk):

		for item in Ck_item:

			sub_Ck = Ck_item - frozenset([item])

			if sub_Ck not in list_Lk:
				return False

		return True

	# 生成关联规则

	def generate_big_rules(self, L, support_data, min_conf):

		"""

		Generate big rules from frequent itemsets.

		Args:

			L: 所有频繁项集的列表

			support_data: 每个频繁项集对应的支持度

			min_conf: 最小可信度
		"""

		big_rule_list = []
		sub_set_list = []
		for i in range(0, len(L)):
			for freq_set in L[i]:
				for sub_set in sub_set_list:
					if sub_set.issubset(freq_set):
						conf = support_data[freq_set] / support_data[freq_set - sub_set]
						big_rule = (freq_set - sub_set, sub_set, conf)
						if conf >= min_conf and big_rule not in big_rule_list:
							print(freq_set - sub_set, " => ", sub_set, "conf: ", conf)
							big_rule_list.append(big_rule)
				sub_set_list.append(freq_set)
		return big_rule_list

if __name__ == '__main__':
	minS = 0.5
	dataSet = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
	apriori = apriori_algorithm(minSupport=minS, dataSet=dataSet)
	L, support_data = apriori.generate_L(dataSet, 3, minS)
	big_rule_list = apriori.generate_big_rules(L, support_data, 0.7)
