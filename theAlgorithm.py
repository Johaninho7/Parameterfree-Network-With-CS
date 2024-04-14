import label, copy, arcClass, time, parameterfreeNetwork, copy, isFeasible, dominate, pprint, edgeChecker


# Parameters
maxElapsed_R = 13
maxTimeDrive_B = 4.5
maxTimeDrive_R = 9
minTimeBreak = 0.75
minTimeBreakFirst = 0.25
minTimeBreakSecond = 0.5
minTimeRest = 11
minTimeRestFirst = 3
minTimeRestSecond = 9
timeDay = 24

def algorithm(paraNetwork):
	numIntermediateNodes = len(paraNetwork.intermediate_nodes)
	numNormalNodes = len(paraNetwork.originalNetwork.nodes)
	numNodes = numIntermediateNodes + numNormalNodes
	
	# Initialise list of labels with the first label, the depot, having index 0
	labels = [label.Label(paraNetwork._getDepot(), numNormalNodes)]
	# Initialise an iterator to keep track of which label is currently being processed
	iterator = 0
	# Intrduce a counter which counts the number of dominated labels for stats
	numDominated = 0
	#newLabel = labels[0]


	while iterator < len(labels):
		currentLabel = labels[iterator]
		tempLabel = currentLabel
		currentNodeTuple = currentLabel.path[-1]
		interNodeTuple = currentLabel.detailedPath[-1]
		edgesFromNode = {edge: data for edge, data in paraNetwork.edges.items() if edge[0] == interNodeTuple} #if edge[0] == currentNodeTuple or edge[0] == interNodeTuple}
		#edgesFromNode = {
		#	edge: data
		#	for edge, data in paraNetwork.edges.items() if (edge[0][0] == interNodeTuple[0] if isinstance(interNodeTuple, tuple) else edge[0][0] == interNodeTuple) and (len(edge[0]) > 1 and len(interNodeTuple) > 1 and edge[0][1].split()[0] == interNodeTuple[1].split()[0] if isinstance(interNodeTuple, tuple) and len(interNodeTuple) > 1 else True)
		#}

		labels.sort(key = lambda x: x.time)

		# Processing label if the current one is not done
		if (labels[iterator].done == False):
			# Iterate over edges starting from the current node
			for edge, edgeData in edgesFromNode.items():
				# Check if currentNodeTuple is in the edge
				if edgeChecker.edgeChecker(interNodeTuple, edge):

					# Check if edge destination is in already in the path
					if edgeChecker.checkPreviouslyVisited(edge, tempLabel):
						continue
					
					# Edge from an original node to an intermediate node
					if edgeChecker.originalToIntermediateEdge(edge):
						resourceExtension = edgeData['REF']
						# Starting on original node on currentLabel
						if isinstance(currentLabel.detailedPath[-1], str):
							if 'fit' in edge[1] and resourceExtension == paraNetwork._fstart_nm:
								nextTuple = edge[1]
								if callable(resourceExtension):
									# fstart_nm
									time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeTuple, nextTuple))
									dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
									newLabel = copy.deepcopy(currentLabel)
									resourceExtension(newLabel, time_nm, dist_nm)
									# Add next node to detailed path
									newLabel.detailedPath.append(nextTuple)

							elif 'dull' in edge[1] and resourceExtension == paraNetwork._fstart_nm:
								nextTuple = edge[1]
								resourceExtension = edgeData['REF']
								if callable(resourceExtension):
									# fstart_nm
									time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeTuple, nextTuple))
									dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
									newLabel = copy.deepcopy(currentLabel)
									resourceExtension(newLabel, time_nm, dist_nm)
									# Add next node to detailed path
									newLabel.detailedPath.append(nextTuple)
							# Starting from original node on newLabel
							elif (isinstance(newLabel.detailedPath[-1], str)):
								if 'fit' in edge[1] and resourceExtension == paraNetwork._fstart_nm:
									nextTuple = edge[1]
									if callable(resourceExtension):
										# fstart_nm
										time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeTuple, nextTuple))
										dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
										newLabel = copy.deepcopy(tempLabel)
										resourceExtension(newLabel, time_nm, dist_nm)
										# Add next node to detailed path
										newLabel.detailedPath.append(nextTuple)

								elif 'dull' in edge[1] and resourceExtension == paraNetwork._fstart_nm:
									nextTuple = edge[1]
									resourceExtension = edgeData['REF']
									if callable(resourceExtension):
										# fstart_nm
										time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeTuple, nextTuple))
										dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
										newLabel = copy.deepcopy(tempLabel)
										resourceExtension(newLabel, time_nm, dist_nm)
										# Add next node to detailed path
										newLabel.detailedPath.append(nextTuple)							
						# Calculate delta after fstart sets timeToNext and distanceToNext
						delta = paraNetwork.delta_l(newLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)

					# Edge from an intermediate node to another intermediate node
					elif edgeChecker.intermediateToIntermediateEdge(edge):
						# Check for connectivity between intermediate nodes, first node which came from an original, then node which came from intermediate
						if (edge[0][0] == tempLabel.detailedPath[-1][0] and edge[0][-1] == tempLabel.detailedPath[-1][-1] and edgeChecker.edgeType(edge) == edgeChecker.detailedPathType(tempLabel) and tempLabel.timeToNext > 0):
						#if (edge[0][0] == currentLabel.detailedPath[-1][0] and edge[0][-1] == currentLabel.detailedPath[-1][-1] and edgeChecker.edgeType(edge) == edgeChecker.detailedPathType(currentLabel) and currentLabel.timeToNext > 0):
							nextTuple = edge[1]
							resourceExtension = edgeData['REF']
							newLabel = copy.deepcopy(tempLabel)
							delta = paraNetwork.delta_l(tempLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
							if 'fit' in edge[0] and resourceExtension == paraNetwork._fdrive_delta:
								if callable(resourceExtension):
									# fdrive_delta)
									resourceExtension(newLabel, delta)
									# Add next node to detailed
									newLabel.detailedPath.append(nextTuple)
							elif 'dull'	in edge[0] and resourceExtension == paraNetwork._frest_delta:
								if callable(resourceExtension):
									# frest_delta
									resourceExtension(newLabel)
									# Add next node to detailed path
									newLabel.detailedPath.append(nextTuple)
							# In a dull intermedaite node, checking frest_delta and fbreak_delta REF
							elif 'dull' in edge[0] and resourceExtension == paraNetwork._fbreak_delta:
								if callable(resourceExtension):
									# fbreak_delta
									resourceExtension(newLabel)
									# Add next node to detailed path
									newLabel.detailedPath.append(nextTuple)

					# Edge from an intermediate node to an original node
					elif edgeChecker.intermediateToOriginalEdge(edge):
						resourceExtension = edgeData['REF']
						if 'fit' in edgeChecker.edgeType(edge) and 'fit' in tempLabel.detailedPath[-1] and resourceExtension == paraNetwork._fvisit_nm and tempLabel.timeToNext == 0:
							newLabel = copy.deepcopy(tempLabel)
							# Access and call the REF method
							if callable(resourceExtension):
								# fvisit_nm
								nextTuple = edge[1]
								TWS_m, TWE_m = paraNetwork.originalNetwork.getTimeWindows(nextTuple)
								ST_m = paraNetwork.originalNetwork.getServiceTime(nextTuple)
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								resourceExtension(newLabel, TWS_m, TWE_m, ST_m, nextTuple, dist_nm)
								newLabel.elem[int(nextTuple)] += 1
								# Add next node to detailed path
								newLabel.detailedPath.append(nextTuple)


						elif 'dull' in edgeChecker.edgeType(edge) and 'dull' in tempLabel.detailedPath[-1] and resourceExtension == paraNetwork._fvisit_nm and tempLabel.timeToNext == 0:
							if callable(resourceExtension):
								newLabel = copy.deepcopy(tempLabel)
								# fvisit_nm
								nextTuple = edge[1]
								TWS_m, TWE_m = paraNetwork.originalNetwork.getTimeWindows(nextTuple)
								ST_m = paraNetwork.originalNetwork.getServiceTime(nextTuple)
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								resourceExtension(newLabel, TWS_m, TWE_m, ST_m, nextTuple, dist_nm)
								newLabel.elem[int(nextTuple)] += 1
								# Add next node to detailed path
								newLabel.detailedPath.append(nextTuple)
				
					# Check feasiblity of new label and if it can be dominated
					if isFeasible.isFeasible(newLabel) and newLabel not in labels:
						labels.append(newLabel)
						
						# Check dominance
						dominated = dominate.dominate(labels)
						numDominated += len(dominated)

						# Setting done = True for all dominated labels to avoid expanding these again
						for i in dominated:
							labels[i].done = True
		
		iterator += 1
		currentLabel.done = True
	print(f"\nNumber of dominated labels: {numDominated}")
	print(f"\nNumber of labels: {len(labels)}")
	#print(f"Label list: {labels}")


	return labels

