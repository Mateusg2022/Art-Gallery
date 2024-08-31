import plotly.graph_objects as go

def coloringTriangles(triangles, polygon, additionalEdgesX, additionalEdgesY, frames):
    verticesx = [vertex[0] for vertex in polygon]
    verticesy = [vertex[1] for vertex in polygon]
    verticesx.append(verticesx[0])
    verticesy.append(verticesy[0])
    colorMap = {}
    
    neighbors = {}
    
    for triangle in triangles:
        for i in range(3):
            point = triangle[i]
            if point not in neighbors:
                neighbors[point] = set()
            neighbors[point].add(triangle[(i+1)%3])
            neighbors[point].add(triangle[(i+2)%3])
    
    for point in neighbors:
        available_colors = {0, 1, 2} - {colorMap.get(neigh) for neigh in neighbors[point]}
        colorMap[point] = min(available_colors)

    redVerticesX = []
    redVerticesY = []
    greenVerticesX = []
    greenVerticesY = []
    blueVerticesX = []
    blueVerticesY = []

    for p, colored in colorMap.items():
        
        if colored == 0:
            redVerticesX.append(p[0])
            redVerticesY.append(p[1])
        elif colored == 1:
            greenVerticesX.append(p[0])
            greenVerticesY.append(p[1])
        else: 
            blueVerticesX.append(p[0])
            blueVerticesY.append(p[1])

        frames.append(go.Frame(
            data=[#go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), 
             #                text=[str(i) for i in range(len(polygon))], textposition='top right', name='Polígono'),
                    go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='gray'), name='Arestas Triangulação'),
                    go.Scatter(x=redVerticesX, y=redVerticesY, mode='markers', marker=dict(size=10, color='red'), name='Vértices Vermelhos'),
                    go.Scatter(x=greenVerticesX, y=greenVerticesY, mode='markers', marker=dict(size=10, color='green'), name='Vértices Verdes'),
                    go.Scatter(x=blueVerticesX, y=blueVerticesY, mode='markers', marker=dict(size=10, color='blue'), name='Vértices Azuis'),
            ],
            name=f'frame{len(frames)}'
        ))
    
    return frames, colorMap