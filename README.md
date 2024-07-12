# RC Model

This repository has been created to reproduce the experiments for the RC Model, an open source processor 
temperature prediction model. The RC Model has been integrated into OpenDC, a discrete event simulator for data centers
allowing us to leverage the simulator's capabilities to evaluate the model's performance.

## Getting Started
The file, `rcmodel.py`, contains the code to run the simulation on an executable version of OpenDC. The 'rcmodel.py' file 
calls OpenDC with the input data and runs the simulation automatically. Once the simulation is complete, the results are
automatically plotted in a similar manner as those in our thesis paper. We plot the predicted temperature against the actual temperature, 
and histograms of the error distributions between the two temperatures and power draw values.


## Data
The data required to run the simulation is stored in the `input` directory. This directory contains the following 
directories and files:
- `M100_input`: This directory contains the input data from the M100 supercomputer, which is used for plotting.
- `scenarios`: This scenario file is used to inform OpenDC on where the topologies are located for the 6 different 
nodes, thus defining 6 different scenarios.
- `topologies`: This directory contains the topology used in the simulation.
- `traces`: This directory contains the traces from the 6 nodes used in the simulation, with each node containing 
two different files.
