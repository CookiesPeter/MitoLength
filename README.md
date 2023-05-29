# MitoLength (With TrackMate 7)
Tested under anaconda package.

H2B-GFP serves as a marker for DNA condensation and has been used as an marker for cell cycle progression.
When DNA condenses, H2B-GFP signals also concentrates and can be captured as an increase of the standard deviation of the signal.

For each cell:
The program first extract the standard deviation of the H2B-GFP channel (default: CH1) and smoothens it with filtfilt noise filtering.
The program then identifies the peak(s) of the signal. Then identifies the local minimum before each peak.
Eventually outputing a plot and a txt recording the peak index.
