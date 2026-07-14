# Propagating Gottesman-Kitaev-Preskill states encoded in an optical oscillator

<https://doi.org/10.5061/dryad.t76hdr86j>

## Description of the data and file structure

The data are the processed quadrature values of the generated states. The Wigner function can be obtained by reconstructing the data via maximum likelihood method. The files in this submission are

1.  quad_0deg.npy
2.  quad_30deg.npy
3.  quad_60deg.npy
4.  quad_-30deg.npy	
5.  quad_-60deg.npy
6.  quad_-90deg.npy

The text **deg corresponds to the phase of the measured data. Note that for the quadrature distribution in the paper, we redefine the phase as the minus phase correspond to the same phase +180 deg with the quadrature values flipped. This process is done for making the figure simpler in the paper and does not affect the subsequent calculation.

The file can be opened by standard Python library called Numpy using the Load command. Each file contains a single array and each element corresponds to an event of the measured quadrature of the generated states processed by integration of the homodyne measurement signals with the wave packet shape.
