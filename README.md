	  ____                _   __  __                                              
	 |  _ \ ___  __ _  __| | |  \/  | ___                                         
	 | |_) / _ \/ _` |/ _` | | |\/| |/ _ \                                        
	 |  _ <  __/ (_| | (_| | | |  | |  __/                                        
	 |_|_\_\___|\__,_|\__,_| |_|  |_|\___|                   _                    
	 |  _ \ ___  __| | ___  ___   / ___|___  _ __ ___  _ __ | | _____  ____ _ ___ 
	 | |_) / _ \/ _` |/ _ \/ __| | |   / _ \| '_ ` _ \| '_ \| |/ _ \ \/ / _` / __|
	 |  _ <  __/ (_| |  __/\__ \ | |__| (_) | | | | | | |_) | |  __/>  < (_| \__ \
	 |_|_\_\___|\__,_|\___||___/  \____\___/|_| |_| |_| .__/|_|\___/_/\_\__,_|___/
	 |  _ \ __ _ _ __| |_  |___ \                     |_|                         
	 | |_) / _` | '__| __|   __) |                                                
	 |  __/ (_| | |  | |_   / __/                                                 
	 |_|   \__,_|_|   \__| |_____|                                           
         

# Part 2 - Simulating Cascade-based attacks on complex networks
In many realistic situations the flow of physical quantities in the network, as characterized
by the loads on nodes, is important. This project simulates the Motter-Lai model which
shows that intentional attacks can lead to a cascade of overload failures, and can cause serious
damage to a network. This model shows that the heterogeneity of real-world networks makes
them particularly vulnerable to attacks in that a large scale cascade may be triggered by
disabling a single key node.
	

# Getting Started
First clone the repository into a local directory:

	git clone https://github.com/moraispgsi/redes-complexas.git
	
	
	
## Installation: 

	The simulation uses networkX and python3.6.3 in 64bits:
	 • https://www.python.org/downloads/release/python-363/

	NOTE: The **64 bit** version is important because the 32 bit version can only use 2GB of RAM and some of the simulations might need more than that.

	Make sure the python version is 3.6.3 or other version that allows to install the following libraries.

	Install the networkx library
		> python -m pip install networkx
	Install the numpy library
		> python -m pip install numpy
	Install the matplotlib library
		> python -m pip install matplotlib

		
		
# Structure
	Code
		- data		# Folder where the results of the simulations are saved
		- networks	# Folder where the generated networks are saved
		• generate.py   # Generates networks in the networks folder
		• simulate.py   # Runs the simulation of the algorithm
		• plot.py 	# Plots the graph of the results of the simulation
		• info.py 	# Shows the info of a graph in GEXF format

		

# Generating a network:
		
	The generate.py file generates a network in one of the 4 following modes:

	• "experiment1" - Generates a network using the first experiment shown in the report with N nodes
		The mode must be 'experiment1'.
		Input Parameters:
			mode (str) - Mode of network generation - **Required**
		    n (int) – Number of nodes - **Required**
		    m (int) – Number of edges to attach from a new node to existing nodes - **Required**
			filename (str) - Name of the file of the network generated, without extension - **Required**
		
		Ouput:
			network file in the directory networks
			
		Usage: 
			> python generate.py experiment1 [n] [m] [filename]
		
		Example:
			> python generate.py experiment1 1000 2 experiment1_1000
			
			
	• "experiment2" - Generates a network using the second experiment shown in the report with N+1 nodes
		The mode must be 'experiment2'.
		Input Parameters:
			mode (str) - Mode of network generation - **Required**
		    n (int) – Number of nodes - **Required**
		    m (int) – Number of edges to attach from a new node to existing nodes - **Required**
			filename (str) - Name of the file of the network generated, without extension - **Required**
			
		Ouput:
			network file in the directory networks
			
		Usage: 
			> python generate.py experiment2 [n] [m] [filename]
			
		Example:
			> python generate.py experiment2 1000 2 experiment2_1000

			
	• "experiment3" - Generates a network using the third experiment shown in the report with N nodes and the 
		The mode must be 'experiment3'.
		Input Parameters:
			mode (str) - Mode of network generation - **Required**
		    n (int) – Number of nodes - **Required**
		    m (int) – Number of edges to attach from a new node to existing nodes - **Required**
			filename (str) - Name of the file of the network generated, without extension - **Required**
			
		Ouput:
			Network file in the directory networks
			The generated network file will be created in the "networks" folder.
			The generated network file is in the format .gexf .
			The generated network file can be opened in gephi in order to get a visual representation of it.
	
		Usage: 
			> python generate.py experiment3 [n] [m] [filename]

		Example:
			> python generate.py experiment3 1000 2 experiment3_1000
			
		
	• "homogeneous" - Generates a random homogeneous network with N nodes and D the degree of each node
		The mode must be 'homogeneous'.
		Input Parameters:	
			mode (str) - Mode of network generation - **Required**
			n (integer) – The number of nodes. The value of n * d must be even - **Required**
		    d (int) – The degree of each node - **Required**
			filename (str) - Name of the file of the network generated, without extension - **Required**
			
		Usage: 
			> python generate.py homogeneous [n] [d] [filename]
		
		Example:
			> python generate.py homogeneous 1000 3 homogeneous_1000
			

	
# Simulating a network:

	The simulate.py file executes the simulation of the algorithm with a given network. The simulation looks for the name of the file 
	inside the networks folder. The simulation consist in attacking the network with the 3 different strategies with different tolerances.
	The tolerances go from 0 to 1, at each step the tolerance increments 0.1. 
	
	Strategies used to attack the network:
		• Random
		• Highest Degree
		• Highest Load
		
	Input:
		Name of the network file, without extension. - **Required**
	
	Output:
		3 files in the directory data, one for each strategy attack. Each file contains multiple lines, each line contains the result of a simulation
		with alfa tolerance over each node. 
		Each line contains:
			• The tolerance
			• The total number of nodes of the graph after the simulation
			• The total number of nodes of the largest connected component before the simulation
			• The total number of nodes of the largest connected component after the simulation 
			• The ration of nodes of the largest connected componenet before and after the simulation; Used quantify the damaged caused by a
				cascade failure.
			
		Example of one line:
			{'tolerance': 0.0, 'graph-size': 246, 'N': 1000, 'N_prime': 33, 'G': 0.033}
		
	Usage:
		> python simulation.py [name-of-the-network]
	
	Example: 
		> python simulation.py experiment2_1000
	

	
# Plotting the network:
	
	The plot.py plots the sizes of the largest connected componenets of each attack from each tolerance. 
	Is possible to plot only the results of the simulations of 1 network or to plot the results of of the simulations of 2 networks in a unique figure.
	
	Input:
		f1 (str) - base file name of the results of one network simulation - **Required**
		f2 (str) - base file name of the results of the second network simulation - Optional
		
	Output:
		PNG file containing the plot of the results and it is on the graphics directory.
		
	Usage:
		> python plot.py [f1] (f2)
		
	Example:
		> python plot.py experiment1_1000
		> python plot.py experiment1_1000 experiment1_2000
	

# Information of the network:


# Contributing
	TODO:
	
	
# Authors
	- Ricardo Morais - (link github)
	- Artur Esteves - (link github)
	
# License
	This project is licensed under the MIT License - see the LICENSE.md file for details
	

# Acknowledgments
	TODO: This work was based on the paper ... 
