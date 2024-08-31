from plotTriangulation import *
from coloring import *

def plotColoring(additionalEdgesX, additionalEdgesY, triangles):
    polygonTxt = 'polygon.txt'
    polygon = readPolygon(polygonTxt)

    verticesx = [vertex[0] for vertex in polygon]
    verticesy = [vertex[1] for vertex in polygon]
    verticesx.append(verticesx[0])
    verticesy.append(verticesy[0])

    frames = []
    frames, colorMap = coloringTriangles(triangles, polygon, additionalEdgesX, additionalEdgesY, frames)

    initial_data = [
        go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), name='Polígono'),
        go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='black'), name='Arestas Cortadas'),
        go.Scatter(x=verticesx + [verticesx[0]], y=verticesy + [verticesy[0]], mode='lines', line=dict(color='black')),
    ]

    trace = go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), 
                        text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right', name='Polígono')
    
    fig = go.Figure(
        data=[trace] + initial_data,
        layout=go.Layout(
            xaxis=dict(range=[min(verticesx) - 1, max(verticesx) + 1], autorange=False),
            yaxis=dict(range=[min(verticesy) - 1, max(verticesy) + 1], autorange=False),
            title="3-Coloração do Polígono",
            annotations=[
                dict(
                    x=0.5,
                    y=1.1,
                    xref='paper',
                    yref='paper',
                    text="Clique no Botão Play para entender o algoritmo",
                    showarrow=False,
                    font=dict(size=14)
                )
            ],
            updatemenus=[{
                "buttons": [
                    {
                        "label": "Play", 
                        "method": "animate", 
                        "args": [None, {"frame": {"duration": 1000, "redraw": True}, "fromcurrent": True, "mode": "immediate"}]
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]
                    }
                ],
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

    fig.add_trace(
        go.Scatter(x=verticesx, y=verticesy, mode='lines+text', line=dict(color='black'), name='Polígono')
    )

    #fig.show()

    fig.write_html("coloring.html")

    return colorMap