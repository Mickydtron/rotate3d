import sys
import numpy as np
import math

class Object3d:
	"""represents a 3d object parsed from a .obj file"""
	def __init__(self, g, v, vn, f):
		self.g = g
		self.v = v
		self.vn = vn
		self.f = f

	def rotate(self, rmatrix):
		"""Rotate this object by the provided rotation matrix"""
		self.v = self.v.dot(rmatrix)
		self.vn = self.vn.dot(rmatrix)

	def write_to_file(self, filename):
		"""Write the current state of this object to a file in .obj format."""
		file = open(filename, 'w')
		file.write('g {}\n'.format(self.g))
		write_section(file, 'v', self.v)
		write_section(file, 'vn', self.vn)
		write_section(file, 'f', self.f)

def write_section(f, identifier, array):
	"""Write the identifier and points from array to file f."""
	f.write('\n')
	for item in array:
		f.write('{} {} {} {}\n'.format(identifier, item[0], item[1], item[2]))

def read_obj(filename):
	"""Open the provided file and parse the contents as an .obj file. 
	Return the parsed object."""
	file = open(filename, 'r')
	g = ''
	v = []
	vn = []
	f = []
	for line in file:
		tokens = line.split()
		if len(tokens) > 0:
			if tokens[0] == "g":
				g = tokens[1]
			elif tokens[0] == "v":
				v.append(tokens[1:4])
			elif tokens[0] == "vn":
				vn.append(tokens[1:4])
			elif tokens[0] == "f":
				f.append(tokens[1:4])
	return Object3d(g, np.array(v, float), np.array(vn, float), np.array(f, int))

def normalize(x,y,z):
	"""Normalize the given 3d vector."""
	length = (x*x + y*y + z*z)**0.5
	return (x/length, y/length, z/length)

def axis_angle_to_rotation_matrix(x, y, z, angle):
	"""Convert the provided vector and angle to a rotation matrix and return it.

	x,y,z -- the axis vector
	angle -- the angle (in radians) to rotate around the given axis
	"""
	(x,y,z) = normalize(x,y,z)
	first = math.cos(angle) * np.eye(3)
	second = (1 - math.cos(angle)) * np.array([[x*x, x*y, x*z],[y*x,y*y,y*z],[z*x,z*y,z*z]])
	third = math.sin(angle) * np.array([[0,-z,y],[z,0,-x],[-y,x,0]])
	return first + second + third

def main():
	"""Load 3d object from file (default teapot.obj), rotate it 90 degrees around the Z axis, 
	and write the result to a new file."""
	inputfilename = "teapot.obj"
	if len(sys.argv) > 1:
		inputfilename = sys.argv[1]
	outputfilename = 'rotated_{}'.format(inputfilename)
	obj3d = read_obj(inputfilename)
	rotation = axis_angle_to_rotation_matrix(0,0,1,(np.pi/2))
	obj3d.rotate(rotation)
	obj3d.write_to_file(outputfilename)

if __name__ == '__main__':
	main()