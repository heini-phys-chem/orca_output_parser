#!/usr/bin/env python2
import sys
import os
import numpy as np

# Function to parse datafile to a dictionary
def get_properties(filenames, path):
    """ Returns a dictionary with energy and forces for each xyz-file.
    """
    # define dictionairies and constants
    properties = dict()

    # to convert Hartree/Bohr -> kcal/(mol angstrom) and Hartree -> kcal/mol
    convF = 627.509/0.529
    convE = 627.509

    for filename in filenames:
      # define dict key
      name				= filename[:-4]
      # open orca output file and read lines
      f_log	= open(path + filename, "r")
      lines	= f_log.readlines()
      f_log.close()

      # find line with the final forces, coordinates
      indexF    = lines.index('The final MP2 gradient\n')
      indexXYZ  = lines.index('CARTESIAN COORDINATES (ANGSTROEM)\n')

      # define np arrays
      forces    = np.array([]).astype(float)
      xyz       = np.array([]).astype(float)
      atomTypes = np.array([]).astype(str)
      numAtoms  = 0

      # get forces and numAtoms
      for line in lines[indexF+1:]:
        tokens = line.strip()
        if tokens == '': break

        tokens  = line.split()
        forces  = np.append(forces, [[ float(tokens[1])*convF, float(tokens[2])*convF, float(tokens[3])*convF]] )
        numAtoms += 1

      # get coordinates
      for line in lines[indexXYZ+2:indexXYZ+numAtoms+2]:
        tokens  = line.split()
        xyz     = np.append(xyz, [[ float(tokens[1]), float(tokens[2]), float(tokens[3]) ]])
        atomTypes = np.append(atomTypes, tokens[0])

      # reshape np arrays (forces and coordinates)
      forces    = forces.reshape(numAtoms,3)
      xyz       = xyz.reshape(numAtoms,3)

      # get energies in a mp.array
      energy		= float(lines[indexF+numAtoms+7].split()[4])*convE

      # dict with name as key and energies, forces, xyz, numAtoms, atomTypes as elements
      properties[name] = [energy, numAtoms, atomTypes, forces, xyz]

    return properties

if __name__ == "__main__":
  path = sys.argv[1]
  filenames = os.listdir(path)
  data = get_properties(filenames, path)

  toprint = []

  # get dict as list
  print "name, energy, numAtoms, atomTypes, forces, xyz"
  for key, value in data.iteritems():
    print (key, value[0], value[1], value[2].tolist(), value[3].tolist(), value[4].tolist())

  # print list to csv file
  #with open('data.csv', 'w') as f:
  #  f.write("name, energy, numAtoms, atomTypes, forces, xyz\n")
  #  for i in toprint:
  #    f.write(str(i))
  #    f.write('\n')



