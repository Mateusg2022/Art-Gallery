import plotly.graph_objects as go
from plotTriangulation import *

def plotCameras(colorMap):
    polygonTxt = 'polygon.txt'
    polygon = readPolygon(polygonTxt)
    verticesx = [vertex[0] for vertex in polygon]
    verticesy = [vertex[1] for vertex in polygon]
    verticesx.append(verticesx[0])
    verticesy.append(verticesy[0])

    #encontrando a cor que possui menos vértices
    corCount = {}
    for cor in colorMap.values():
        if cor in corCount:
            corCount[cor] += 1
        else:
            corCount[cor] = 1

    leastColor = min(corCount, key=corCount.get)
    verticesLeastColorX = []
    verticesLeastColorY = []

    for vertice, cor in colorMap.items():
        if cor == leastColor:
            index = polygon.index(vertice) 
            verticesLeastColorX.append(polygon[index][0])
            verticesLeastColorY.append(polygon[index][1])

    if leastColor == 0:
        leastColor = 'red'
    elif leastColor == 1:
        leastColor = 'green'
    else:
        leastColor = 'blue'

    frames=[]
    frames.append(go.Frame(
        data=[go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), 
                text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right', name='Polígono'),
        go.Scatter(x=verticesLeastColorX, y=verticesLeastColorY, mode='markers', marker=dict(size=15, color=leastColor), name='Câmeras')
        ],
        name=f'frame{len(frames)}'
    ))

    initial_data = [
        go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), 
                text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right', name='Polígono'),
        go.Scatter(x=verticesx + [verticesx[0]], y=verticesy + [verticesy[0]], mode='lines', line=dict(color='black')),
    ]
    
    fig = go.Figure(
        data=initial_data,
        layout=go.Layout(
            xaxis=dict(range=[min(verticesx) - 1, max(verticesx) + 1], autorange=False),
            yaxis=dict(range=[min(verticesy) - 1, max(verticesy) + 1], autorange=False),
            title="Vértices das Câmeras",
            updatemenus=[{
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Frame Timeline:",
                    "visible": True,
                    "xanchor": "right"
                },
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [{"label": f"{i}", "method": "animate", "args": [[frames[i]], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 500}}]} for i in range(len(frames))]
            }]
        ),
        frames=frames
    )

    #fig.show()

    fig.write_html("cameras.html")

    return