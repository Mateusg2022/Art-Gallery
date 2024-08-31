import plotly.graph_objects as go

def convex(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0

def areaTriangle(a, b, c):
    return abs((a[0]*b[1] + b[0]*c[1] + c[0]*a[1]) - (a[1]*b[0] + b[1]*c[0] + c[1]*a[0])) / 2

def pointInTriangle(p, a, b, c):
    area_orig = areaTriangle(a, b, c)
    area1 = areaTriangle(p, b, c)
    area2 = areaTriangle(p, a, c)
    area3 = areaTriangle(p, a, b)
    return abs(area_orig - (area1 + area2 + area3)) < 1e-10

def isEar(polygon, i):
    a, b, c = polygon[i-1], polygon[i], polygon[(i+1) % len(polygon)]

    if not convex(a, b, c):
        return False

    for p in polygon:
        if p not in (a, b, c) and pointInTriangle(p, a, b, c):
            return False
    return True

#aplica o algoritmo de corte de orelhas e sua animação
def earClippingTriangulation(polygon):
    triangles = []
    triangulationFrames = []
    poly = polygon[:]
    verticesx = [vertex[0] for vertex in polygon]
    verticesy = [vertex[1] for vertex in polygon]
    verticesx.append(verticesx[0])
    verticesy.append(verticesy[0])
    additionalEdgesX = []
    additionalEdgesY = []
    erasedEdgesX = []
    erasedEdgesY = []
    markedPointsX = []
    markedPointsY = []
    erased = []
    while len(poly) > 3:
        for i in range(len(poly)):
            if isEar(poly, i):
                p1, p2, p3 = poly[i-1], poly[i], poly[(i+1) % len(poly)]
                triangles.append((p1, p2, p3))
                edgesArray = [p1, p2, p3]
                
                for edge in edgesArray:
                    if edge != p2:
                        additionalEdgesX.append(edge[0])
                        additionalEdgesY.append(edge[1])
                        erased.append({edge[0], edge[1]})
                        
                    markedPointsX.append(edge[0])
                    markedPointsY.append(edge[1])

                triangulationFrames.append(go.Frame(
                    data=[
                        go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), 
                                   text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right', name='Polígono'),
                        go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='blue'), name='Aresta da Orelha'),
                        go.Scatter(x=erasedEdgesX, y=erasedEdgesY, mode='lines', line=dict(color='lightgray'), name='Arestas Cortadas'),
                        go.Scatter(x=markedPointsX, y=markedPointsY, mode='markers+lines', line=dict(color='red'), name='Arestas da Iteração'),            
                    ],
                    name=f'frame{len(triangulationFrames)}'
                ))
                markedPointsX.clear()
                markedPointsY.clear()
                for edge in edgesArray:
                    erasedEdgesX.append(edge[0])
                    erasedEdgesY.append(edge[1])
                    
                del poly[i]
                break
            
    triangulationFrames.append(go.Frame(
        data=[
            go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), 
                        text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right', name='Polígono'),
            go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='black'), name='Aresta da Orelha'),
            go.Scatter(x=erasedEdgesX, y=erasedEdgesY, mode='lines', line=dict(color='lightgray'), name='Arestas Cortadas'),
            go.Scatter(x=markedPointsX, y=markedPointsY, mode='markers+lines', line=dict(color='red'), name='Arestas da Iteração'),         
        ],
        name=f'frame{len(triangulationFrames)}'
    ))

    triangles.append((poly[0], poly[1], poly[2]))
    return triangulationFrames, additionalEdgesX, additionalEdgesY, triangles