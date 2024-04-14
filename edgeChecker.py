


def currentNodeIsReal(currentNodeTuple, edge):
	# Check if the current node is a real node and in the edge
	if isinstance(edge, tuple) and isinstance(edge[0], (tuple, str)):
		return currentNodeTuple == edge[0]
	return False

"""
def currentNodeIsIntermediate(currentNodeTuple, edge):
	# Check if the current node is an intermediate node and within the first tuple of the edge,
	# but compare only with the first or second element of this tuple
	if isinstance(edge, tuple) and isinstance(edge[0], (tuple)):
		currentNodeBase = currentNodeTuple[1].split()[0] if isinstance(currentNodeTuple[1], str) else currentNodeTuple[1]
		edgeNodeBase = edge[0][1].split()[0] if isinstance(edge[0][1], str) else edge[0][1]
		return currentNodeTuple[0] == edge[0][0] and currentNodeBase == edgeNodeBase
	return False
"""
def currentNodeIsIntermediate(currentNodeTuple, edge):
    # Check if the current node is an intermediate node and within the first tuple of the edge
    if isinstance(edge, tuple) and isinstance(edge[0], tuple):
        # Ensure that currentNodeTuple is a tuple with the expected structure
        if isinstance(currentNodeTuple, tuple):
            # Extract the base type (e.g., 'fit' from 'fit R') for comparison
            currentNodeBaseType = currentNodeTuple[1].split()[0] if isinstance(currentNodeTuple[1], str) else currentNodeTuple[1]
            edgeBaseType = edge[0][1].split()[0] if isinstance(edge[0][1], str) else edge[0][1]

            # Compare the base type and the node identifier (e.g., 'n')
            return currentNodeTuple[0] == edge[0][0] and currentNodeBaseType == edgeBaseType

    return False






def edgeChecker(currentNodeTuple, edge):
	# Determine if the edge should be processed based on the given checks
	return currentNodeIsReal(currentNodeTuple, edge) or currentNodeIsIntermediate(currentNodeTuple, edge)


def intermediateToIntermediateEdge(edge):
	# Check if the edge is an edge between two intermediate nodes
	return isinstance(edge, tuple) and isinstance(edge[0], tuple) and isinstance(edge[1], tuple)

def originalToIntermediateEdge(edge):
	# Check if the edge is an edge between an original node and an intermediate node
	return isinstance(edge[0], str) and isinstance(edge[1], tuple)

def intermediateToOriginalEdge(edge):
	# Check if the edge is an edge between an intermediate node and an original node
	return isinstance(edge[0], tuple) and isinstance(edge[1], str)

def backToDepotEdge(edge):
	# Check if the edge is an edge leading back towards the depot
	return isinstance(edge[1], (tuple, str)) and edge[1][-1] == '0'


def checkPreviouslyVisited(edge, newLabel):
	# Check if the end node in the edge is in the path already
	return isinstance(edge[1], (tuple, str)) and edge[1][-1] in newLabel.path

def edgeType(edge):
	return edge[0][1].split()[0]

def detailedPathType(label):
	if isinstance(label.detailedPath[-1], tuple):
		return label.detailedPath[-1][1].split()[0]
	
	

