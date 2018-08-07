#algorithm to convert a DICOM file into PNG
import vtk
from vtk import vtkDICOMImageReader
from vtk import vtkImageShiftScale
from vtk import vtkPNGWriter

def convert(filepath):

	filepath = "./display/"
	reader = vtk.vtkDICOMImageReader() #we create a new vtkDICOMImageReader under the name of reader which we use to read the DICOM images.
	reader.SetDirectoryName(filepath)
	reader.Update()
	image = reader.GetOutput()

	shiftScaleFilter = vtkImageShiftScale()
	shiftScaleFilter.SetOutputScalarTypeToUnsignedChar()
	shiftScaleFilter.SetInputConnection(reader.GetOutputPort())

	shiftScaleFilter.SetShift(-1.0*image.GetScalarRange()[0])
	oldRange = image.GetScalarRange()[1] - image.GetScalarRange()[0]
	newRange = 255

	shiftScaleFilter.SetScale(newRange/oldRange)
	shiftScaleFilter.Update()

	writer = vtkPNGWriter()
	writer.SetFileName('./display/output.png') # you give the path-filename where you want the output to be
	writer.SetInputConnection(shiftScaleFilter.GetOutputPort())
	writer.Write()

	return 1
