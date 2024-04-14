

import csv

class Network:
	def __init__(self, filepath, cityArcs):
		self.filepath = filepath
		self.cityArcs = cityArcs
		self.nodes = {}  # To store node data, including the depot
		
		self.parse()
		self.arcs = self._generateArcs()



	def parse(self):
		with open(self.filepath, 'r') as file:
			reader = csv.reader(file)
			section = None
			isFirstVehicleRow = True

			for row in reader:
				if not row:  # Skip empty lines
					continue

				if row[0].startswith('VehicleId'):
					section = 'vehicles'
					continue
				elif row[0].startswith('NodeId'):
					section = 'nodes'
					continue

				if section == 'vehicles' and isFirstVehicleRow:
					self._parseDepotRow(row)
					isFirstVehicleRow = False
				elif section == 'nodes':
					self._parseNodeRow(row)

	def _parseDepotRow(self, row):
		vehicle_id, location, location_id = row
		self.nodes[vehicle_id] = {
			'location': location,
			'locationId': int(location_id),
			'timeWindowStart': 0,
			'timeWindowEnd': float('inf'),
			'serviceTime': 0.0,
			'nodeType': 'city'
		}

	def _parseNodeRow(self, row):
		node_id, location, location_id, start, end, _, _, _, serviceTime = row
		self.nodes[node_id] = {
			'location': location,
			'locationId': int(location_id),
			'timeWindowStart': int(start),
			'timeWindowEnd': int(end),
			'serviceTime': float(serviceTime),
			'nodeType': 'city'
		}


	def _generateArcs(self):
		print("Generating arcs...")
		arcs = []

		if not self.nodes:
			return arcs

		current_location_id = -1

		for startNode, startNodeData in self.nodes.items():
			startCity = startNodeData['location']
			if startCity in self.cityArcs:
				startArc = self.cityArcs[startCity]
				for endCity, time in startArc.times.items():
					endNode = None
					# Find the nodeId for endCity in self.nodes
					for node_id, node_data in self.nodes.items():
						if node_data['location'] == endCity:
							endNode = node_id
							break

					if endNode is not None:

						# Add a direct arc from start to end node
						arcs.append((startNode, endNode))
						# If distance between cities is more than 50 km
						if (time * 70) > 50:
							# Calculate number of charging stations needed
							num_cs = (time * 70) // 50
							if (time * 70) % 50 != 0:
								num_cs += 1  # Add one more CS if there's a remainder

							# Insert charging station nodes at intervals of 50 km
							prev_node = startNode
							for i in range(num_cs):
								cs_location_id = current_location_id - i
								cs_node_id = f"CS_{startNode}_{endNode}_{i}"
								self.nodes[cs_node_id] = {
									'location': f'Charging Station {i} between {startCity} and {endCity}',
									'locationId': cs_location_id,
									'timeWindowStart': 0,
									'timeWindowEnd': float('inf'),
									'serviceTime': 0.0,
									'nodeType': 'CS'
								}

								# Add an arc from start node to this charging station
								arcs.append((startNode, cs_node_id))
								
								#Add an arc from the previous CS to this CS
								arcs.append((prev_node, cs_node_id))
								prev_node = cs_node_id
				
							# Add arc from last CS to end node
							arcs.append((prev_node, endNode))
							current_location_id -= num_cs  # Update current location id
	
		return arcs


	"""
	def _generateArcs(self):
		print("Generating arcs...")
		arcs = []
		if not self.nodes:
			#print("No nodes data available.")
			return arcs∏

		for nodeId, nodeData in self.nodes.items():
			#print(f"Processing node: {nodeId}")
			city = nodeData['location']
			if city in self.cityArcs:
				#print(f"City found in cityArcs: {city}")
				arc = self.cityArcs[city]
				for otherCity in arc.distances:
					#print(f"Found potential connection from {city} to {otherCity}")

					# Find the nodeId for otherCity in self.nodes
					otherCityNodeId = None
					for otherNodeId, otherNodeData in self.nodes.items():
						if otherNodeData['location'] == otherCity:
							otherCityNodeId = otherNodeId
							break

					if otherCityNodeId is not None:
						arcs.append((nodeId, otherCityNodeId))
						#print(f"Generated arc: {nodeId} to {otherCityNodeId}")


		return arcs
	"""

	
	def getOriginalFromNodeId(self, nodeId):
		# Check if it's an intermediate node
		if isinstance(nodeId, tuple):
			# Check if the first element is a state string 'fit', 'dull'
			if isinstance(nodeId[0], str):
				# Return the original node ID
				return nodeId[1]
			# Else the first element is the original node ID
			else:
				return nodeId[0]
		return nodeId

	def getOriginalToNodeId(self, nodeId):
		# Check if it's an intermediate node
		if isinstance(nodeId, tuple):
			# Check if the second element is a state string 'fit', 'dull'
			if isinstance(nodeId[1], str):
				# Return the original end node ID
				return nodeId[-1]
			# Else the second element is the original node ID
			else:
				return nodeId[-1]
		# Else the node ID is the original node ID
		return nodeId

	def getDistance(self, fromNodeID, toNodeID):
		# Extract original node IDs
		fromOriginalNodeID = self.getOriginalFromNodeId(fromNodeID)
		toOriginalNodeID = self.getOriginalToNodeId(toNodeID)

		fromCity = self.nodes.get(fromOriginalNodeID, {}).get('location')
		toCity = self.nodes.get(toOriginalNodeID, {}).get('location')

		if fromCity == 'Artificial' or toCity == 'Artificial':
			return 0

		if fromCity is None or toCity is None:
			# Handle intermediate nodes
			if isinstance(fromNodeID, tuple) and isinstance(toNodeID, tuple):
				# Extract original cities for intermediate nodes
				fromCity = self.nodes.get(fromOriginalNodeID, {}).get('location')
				toCity = self.nodes.get(toOriginalNodeID, {}).get('location')
			else:
				print(f"Error: One of the cities for Node IDs {fromNodeID} or {toNodeID} is not found.")
				return None


		# Access the 'distance' dictionary of the City object
		fromCityObject = self.cityArcs.get(fromCity)
		if fromCityObject is not None:
			distance = fromCityObject.distances.get(toCity)
			print(f"Distance from {fromCity} to {toCity}: {distance}")
			return distance
		else:
			print(f"Error: City data for {fromCity} not found.")
			return None


	def getTime(self, fromNodeID, toNodeID):
		# Extract original node IDs
		fromOriginalNodeID = self.getOriginalFromNodeId(fromNodeID)
		toOriginalNodeID = self.getOriginalToNodeId(toNodeID)

		fromCity = self.nodes.get(fromOriginalNodeID, {}).get('location')
		toCity = self.nodes.get(toOriginalNodeID, {}).get('location')
		# Additional debug print
		print(f"Retrieving time from {fromCity} (Node {fromOriginalNodeID}) to {toCity} (Node {toOriginalNodeID})")

		if fromCity == 'Artificial' or toCity == 'Artificial':
			return 0
			
		if fromCity is None or toCity is None:
			# Handle intermediate nodes
			if isinstance(fromNodeID, tuple) and isinstance(toNodeID, tuple):
				# Extract original cities for intermediate nodes
				fromCity = self.nodes.get(fromOriginalNodeID, {}).get('location')
				toCity = self.nodes.get(toOriginalNodeID, {}).get('location')
			else:
				print(f"Error: One of the cities for Node IDs {fromNodeID} or {toNodeID} is not found.")
				return None

		fromCityObject = self.cityArcs.get(fromCity)
		if fromCityObject is not None:
			time = fromCityObject.times.get(toCity)
			if time is not None:
				print(f"Time from {fromCity}, NodeId {fromOriginalNodeID}, to {toCity}, NodeId {toOriginalNodeID}: {time}")
				return time
			else:
				print(f"Time data not found for route from {fromCity}, NodeId {fromOriginalNodeID}, to {toCity}, NodeId {toOriginalNodeID}.")
		else:
			print(f"Error: City data for {fromCity}, NodeId {fromOriginalNodeID}, not found.")

		return None

	def getTimeWindows(self, toNodeID):
		# Extract original node IDs
		toOriginalNodeID = self.getOriginalToNodeId(toNodeID)

		TWS_m = self.nodes.get(toOriginalNodeID, {}).get('timeWindowStart')
		TWE_m = self.nodes.get(toOriginalNodeID, {}).get('timeWindowEnd')
		return TWS_m, TWE_m

	def getServiceTime(self, toNodeID):
		# Extract original node IDs
		toOriginalNodeID = self.getOriginalToNodeId(toNodeID)

		return self.nodes.get(toOriginalNodeID, {}).get('serviceTime')



	def getNodes(self):
		return self.nodes


