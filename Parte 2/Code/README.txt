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
                                    
Installation: 

	The simulation uses networkX and python3.6.3 in 64bits:
	 • https://www.python.org/downloads/release/python-363/

	NOTE: The 64 bit version is important because the 32 bit version can only use 2GB of RAM and some of the simulations might need more than that.

	Make sure the python version is 3.6.3

	Install the networkx library
		> python -m pip install networkx
	Install the numpy library
		> python -m pip install numpy
	Install the matplotlib library
		> python -m pip install matplotlib

Structure
	○ code
		○ data			#Result of the generation
		○ networks		#Folder where the generated networks are saved
			○ attempt1  
			○ attempt2
			○ attempt3
		• generate.py   # Generates networks in the networks folder
		• simulate.py   # Runs the simulation of the algorithm
		• plot.py 	    # Plots the graph of the results of the simulation
		• info.py 		# Shows the info of a graph in GEXF format


Generating a network:

	The generate.py file generates a network in one of 4 modes:
	• "attempt1" - Generates a network using the first attempt shown in the report with N nodes
		Parameters:	
		    n (int) – Number of nodes
		    m (int) – Number of edges to attach from a new node to existing nodes
		Usage: > python generate.py homogeneous 1000 2

	• "attempt2" - Generates a network using the second attempt shown in the report with N+1 nodes
		Parameters:	
		    n (int) – Number of nodes
		    m (int) – Number of edges to attach from a new node to existing nodes
		Usage: > python generate.py homogeneous 1000 2

	• "attempt3" - Generates a network using the third attempt shown in the report with N nodes and the 
		Parameters:	
		    n (int) – Number of nodes
		    m (int) – Number of edges to attach from a new node to existing nodes
		Usage: > python generate.py homogeneous 1000 2

	• "homogeneous" - Generates a random homogeneous network with N nodes and D the degree of each node
		Parameters:	
			n (integer) – The number of nodes. The value of n * d must be even.
		    d (int) – The degree of each node.
		Usage: > python generate.py homogeneous 1000 3

	The generated file will be created in the "networks" folder.
	The generated network file can be opened in gephi in order to see a visual representation of it.


Simulating a network:

	The simulate.py file executes the simulation of the algorithm with a given network. The simulation looks for the name of the file inside the networks folder.

	Usage:
	> python3 simulation.py name-of-the-network all 

	The result will be output to the data folder. There should be 3 distinct files, one for each strategy with the name of the network.


Plotting the network:

TODO


Information of the network:
	
