import vtk
from vtk.util import numpy_support
import os
import numpy
import vtk
import plotly
from plotly.graph_objs import *
from IPython.display import Image

#plotly.plotly.sign_in("qcourbon", "PGCO6CnXRiqaYlpmkE9u")
plotly.plotly.sign_in("somada141", "1t2qb5b9y1")
def modelisation(value):
	def vtkImageToNumPy(image, pixelDims):
	    pointData = image.GetPointData()
	    arrayData = pointData.GetArray(0)
	    ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
	    ArrayDicom = ArrayDicom.reshape(pixelDims, order='F')
	    
	    return ArrayDicom



	def plotHeatmap(array, name="plot"):
	    data = Data([
	        Heatmap(
	            z=array,
	            colorscale='Greys'
	        )
	    ])
	    layout = Layout(
	        autosize=False,
	        title=name
	    )
	    fig = Figure(data=data, layout=layout)

	    return plotly.plotly.iplot(fig, filename=name)


	def vtk_show(renderer, width=400, height=300):
	    """
	    Takes vtkRenderer instance and returns an IPython Image with the rendering.
	    """
	    renderWindow = vtk.vtkRenderWindow()
	    renderWindow.SetOffScreenRendering(1)
	    renderWindow.AddRenderer(renderer)
	    renderWindow.SetSize(width, height)
	    renderWindow.Render()
	     
	    windowToImageFilter = vtk.vtkWindowToImageFilter()
	    windowToImageFilter.SetInputData(renderWindow)
	    windowToImageFilter.Update()
	     
	    writer = vtk.vtkPNGWriter()
	    writer.SetWriteToMemory(1)
	    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
	    writer.Write()
	    data = bytes(memoryview(writer.GetResult()))
	    
	    return Image(data)

	PathDicom = "./ups/"
	reader = vtk.vtkDICOMImageReader() #we create a new vtkDICOMImageReader under the name of reader which we use to read the DICOM images.
	reader.SetDirectoryName(PathDicom)
	reader.Update()


	# Load dimensions using `GetDataExtent`
	_extent = reader.GetDataExtent()
	ConstPixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]

	# Load spacing values
	ConstPixelSpacing = reader.GetPixelSpacing()



	ArrayDicom = vtkImageToNumPy(reader.GetOutput(), ConstPixelDims)
	plotHeatmap(numpy.rot90(ArrayDicom[:, 256, :]), name="CT_Original")

	#Apply thresholding and createa " bone mask "
	threshold = vtk.vtkImageThreshold ()
	threshold.SetInputConnection(reader.GetOutputPort())
	threshold.ThresholdByLower(value)  # remove all soft tissue
	threshold.ReplaceInOn()
	threshold.SetInValue(0)  # set all values below 400 to 0
	threshold.ReplaceOutOn()
	threshold.SetOutValue(1)  # set all values above 400 to 1
	threshold.Update()

	ArrayDicom = vtkImageToNumPy(threshold.GetOutput(), ConstPixelDims)
	plotHeatmap(numpy.rot90(ArrayDicom[:, 256, :]), name="CT_Thresholded")


	#marching cube algorithm 
	dmc = vtk.vtkDiscreteMarchingCubes()
	dmc.SetInputConnection(threshold.GetOutputPort())
	dmc.GenerateValues(1, 1, 1)
	dmc.Update()

	mapper = vtk.vtkPolyDataMapper()
	mapper.SetInputConnection(dmc.GetOutputPort())

	actor = vtk.vtkActor()
	actor.SetMapper(mapper)

	renderer = vtk.vtkRenderer()
	renderer.AddActor(actor)
	renderer.SetBackground(1.0, 1.0, 1.0)

	camera = renderer.MakeCamera()
	camera.SetPosition(-500.0, 245.5, 122.0)
	camera.SetFocalPoint(301.0, 245.5, 122.0)
	camera.SetViewAngle(30.0)
	camera.SetRoll(-90.0)
	renderer.SetActiveCamera(camera)
	#vtk_show(renderer, 600, 600)

	camera = renderer.GetActiveCamera()
	camera.SetPosition(301.0, 1045.0, 122.0)
	camera.SetFocalPoint(301.0, 245.5, 122.0)
	camera.SetViewAngle(30.0)
	camera.SetRoll(0.0)
	renderer.SetActiveCamera(camera)
	#vtk_show(renderer, 600, 600)

	writer = vtk.vtkSTLWriter()
	writer.SetInputConnection(dmc.GetOutputPort())
	writer.SetFileTypeToBinary()
	writer.SetFileName("./static/3Dmodel.stl")
	writer.Write()
	return 1

# # display the .stl file
# filename="clavicle.stl"
# reader = vtk.vtkSTLReader()
# reader.SetFileName(filename)
 
# mapper = vtk.vtkPolyDataMapper()
# if vtk.VTK_MAJOR_VERSION <= 5:
#     mapper.SetInput(reader.GetOutput())
# else:
#     mapper.SetInputConnection(reader.GetOutputPort())
 
# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
 
# # Create a rendering window and renderer
# ren = vtk.vtkRenderer()
# renWin = vtk.vtkRenderWindow()
# renWin.AddRenderer(ren)
 
# # Create a renderwindowinteractor
# iren = vtk.vtkRenderWindowInteractor()
# iren.SetRenderWindow(renWin)
 
# # Assign actor to the renderer
# ren.AddActor(actor)
 
# # Enable user interface interactor
# iren.Initialize()
# renWin.Render()
# iren.Start()

