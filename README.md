# MitoLength (With TrackMate 7)
Written under Python package. Developed by Peter Fu and Steven Qi from HKUST.
Tested under Anaconda package.

	How to use:
	Trackmate
	Please pass Trackmate TRACK data into this program.
	This program extracts the standard deviation and frame data from Trackmate TRACK csv file. 
 	Please export the csv file into the same folder as this program, renamed as 'export.csv'. Please make sure the H2B-GFP channel is as CH1.
	
	After such run the program and it generates two types of files:
	1. Plotted images of each tracks, with identified peaks
	2. csv file for all the recorded events of cell division. Appended after everytime the program runs. 
 	Does not overwrite old file. Users can take this for calculations of mitotic length, number of cell split etc.

H2B-GFP is a genetically-encoded fluorescent protein that can be used as a marker to track the progression of cells through the cell cycle. Specifically, H2B-GFP is fused to histone H2B, which is a protein that is involved in packaging DNA into chromatin within the nucleus. During the cell cycle, the chromatin undergoes a series of changes that are reflected in the behavior of H2B-GFP. During mitosis, H2B-GFP becomes highly condensed and is visible as distinct spots within the nucleus.		 By tracking the behavior of H2B-GFP over time, researchers can gain insights into the timing and progression of the cell cycle in different cell types and under different experimental conditions.
