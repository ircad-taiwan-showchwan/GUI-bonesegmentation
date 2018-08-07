#algorithm to create the URI address of an image
from datauri import DataURI
def generateURI(filepath):
	png_uri = DataURI.from_file(filepath)
	png_uri.mimetype
	'image/png'
	png_uri.data
	#the data URI is png_uri
	#print(png_uri);
	return png_uri
