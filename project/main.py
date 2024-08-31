from plotTriangulation import *
from plotColoring import *
from plotCameras import *

additionalEdgesX, additionalEdgesY, triangles = triangleVertex()
colorMap = plotColoring(additionalEdgesX, additionalEdgesY, triangles)
plotCameras(colorMap)