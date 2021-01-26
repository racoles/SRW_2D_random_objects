# -*- coding: utf-8 -*-
#############################################################################
# SRWLIB Example#17(opPathDif only): Simulating propagation a 2D random 
#   object sample
# Authors/Contributors: Rebecca Ann Coles
# September 1, 2019
# April 11, 2020
#############################################################################

#**********************Import:
from __future__ import print_function #Python 2.7 compatibility
from srwlib import srwl_uti_save_intens_hdf5
from uti_plot import uti_plot2d, uti_plot_show #required for plotting
from srwl_uti_smp import srwl_opt_setup_smp_rnd_obj2d

import os

print('SRWLIB Python Example # 17 (opPathDif only): Simulating a 2D random object sample')

#**********************Data file names
#data sub-folder name
strDataFolderName = 'data_example_17'
#file name for optical path difference data
strOpPathOutFileName = 'ex17_res_opt_path_dif-HDF5.dat'
#output type ('srw', 'png', 'jpg','tif')
return_type = 'srw' 

#**********************Initial Electric Field Wavefront:
eStart = 12400 #Initial Photon Energy [eV]
eFin = 12400 #Final Photon Energy [eV]

#***********Optical Elements:
delta = 3.738856e-05 #refractive index decrement
attenLen = 3.38902e-06 #attenuation length [m].
thickness = 3e-06 #thickness of the sample [m]. 1e-06m = 0.001mm
extTr = 1 #(srwlib.SRWLOptT) transmission outside the grid/mesh is zero (0), or it is same as on boundary (1)
ne = 1 #(srwlib.SRWLOptT) number of transmission data points vs photon energy
xc = 0 #horizontal coordinate of center [m].
yc = 0 #vertical coordinate of center [m].

#***********2D random object properties:
rx = 0.00001 #range of the horizontal coordinate [m] for which the transmission is defined (0.02m = 20mm)
ry = 0.00001 #range of the vertical coordinate [m] for which the transmission is defined (0.02m = 20mm)
nx=10001 #number of transmission data points in the horizontal direction
ny=10001 #number of transmission data points in the vertical direction

density = 3000000 #approximate density [particles per mm^2]
minimum_dist_between_obj = 0.0000006 #[m]
object_shape = 2 #choices are: 1=rectangle, 2=ellipse, 3=triangle, 4=polygon, 5=random_shapes
object_minimum_size = 0.0000001 #each particle radius [m] (0.0001 m = 0.1 mm)
object_maximum_size = 0.0000003 #each particle radius [m] (0.0003 m = 0.3 mm)
object_size_distibution = 3 #distribution of sizes. Choices are: 1=uniform, 2=normal(Gaussian), 3=Flory–Schulz
minimum_angle_rotation = 0 #minimum angle of rotation
maximum_angle_rotation = 45 #maximum angle of rotation
angle_rotation_distibution = 3 #distribution of rotation angle. Choices are: 1=uniform, 2=normal(Gaussian), 3=Flory–Schulz

#Randomization algorithm for object placement. Choices are: 'uniform_seeding' or '2D_walk'
#   randomization_algorithm = 1 # random ~uniform seeding (default)
#       Algorithm will create a uniform set of objects based on: density, 
#       minimum and maximum object size, and the minimum distance between
#       objects. It then applies random seeded noise to the point locations.
#   randomization_algorithm = 2 # 2D random walk
#       Each object will be placed using a random 2D random walk.
randomization_algorithm = 1

#Optional Object Parameter (1): Object side ratios
#   rectangle: ratio of width to length (length is the longest dimension). 
#       Leaving value as None will give 1.0 (square) as width to length 
#       ratio unless _obj_par2 = True is selected to randomize the 
#       width to length ratio.
#   ellipse: ratio of minor to major semi-axes. 
#       Leaving value as None will give 1.0 (circle) as minor to major 
#       semi-axes ratio unless _obj_par2 = True is selected to 
#       randomize the minor to major semi-axes ratio.
#   triangle: ratio of height (y, or "opposite") to width (x, or adjunct). 
#       Leaving value as None will give 1.0 (1/1) as height to width 
#       ratio unless _obj_par2 = True is selected to randomize the 
#       height to width ratio (default is an equilateral triangle).
#   regular polygon: number of polygon vertices.
#       Leaving value as None will give a hexagon (6 sides)
#       unless _obj_par2 = True is selected to randomize the numer of 
#       polygon vertices.
#   random shapes: Which shapes to randomly generate.
#       Choices are [1='rectangle',2='ellipse',3='triangle',4='polygon'].
#       Leaving value as None will give all shape options as:
#         [1,2,3,4]
object_parameter1 = None

#Optional Object Parameter (2): Randomize object side ratios
#   rectangle: value set to True will randomize the width 
#       to length ratio.
#   ellipse: Value set to True will randomize the minor to major 
#       semi-axes ratio.
#   triangle: value set to True will randomize the height (y, or "opposite")
#       to width (x, or adjunct) ratio.
#   regular polygon: Value set to True will randomize the numer of polygon 
#       vertices. Max vertices = 12.
object_parameter2 = None


#***********Generating a 2D random disk:
print('   Setting-up random 2D Objects ...')
opT = srwl_opt_setup_smp_rnd_obj2d(_thickness=thickness, _delta=delta, _atten_len=attenLen, _rx=rx, _ry=ry, _xc=xc, _yc=yc, _nx=nx, _ny=ny,
                                     _dens=density, _obj_type=object_shape, _r_min_bw_obj = minimum_dist_between_obj,
                                     _obj_size_min = object_minimum_size, _obj_size_max = object_maximum_size, _size_dist = object_size_distibution,
                                     _ang_min = minimum_angle_rotation, _ang_max = maximum_angle_rotation, _ang_dist = angle_rotation_distibution, 
                                     _rand_alg = randomization_algorithm,
                                     _obj_par1 = object_parameter1, _obj_par2 = object_parameter2,
                                     _extTr=extTr, _ne=ne, _e_start=eStart, _e_fin=eFin,
                                     _ret=return_type, _file_path=strDataFolderName, _file_name=strOpPathOutFileName)

if return_type == 'srw':
#Extracting transmission data characteristic for subsequent plotting and saving it to a file
    opPathDif = opT.get_data(3, 3)
    opTMesh = opT.mesh

#Optical path difference data to an ASCII file:
    print("   Saving optical path difference data to an HDF5 file: " + strOpPathOutFileName)
    srwl_uti_save_intens_hdf5(opPathDif, opTMesh, os.path.join(os.getcwd(), strDataFolderName, strOpPathOutFileName))

#**********************Plotting results (requires 3rd party graphics package):
    print('   Plotting the results (blocks script execution; close any graph windows to proceed) ... ', end='')

#Plotting Sample Optical Path Difference
    plotMeshX = [opTMesh.xStart, opTMesh.xFin, opTMesh.nx]
    plotMeshY = [opTMesh.yStart, opTMesh.yFin, opTMesh.ny]
    uti_plot2d(opPathDif, plotMeshX, plotMeshY, ['Horizontal Position [M]', 'Vertical Position [M]', '2D Random Disk Optical Path Difference'])

    uti_plot_show() #show all graphs (blocks script execution; close all graph windows to proceed)
    print('   done')

