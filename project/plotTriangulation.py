from triangulate import *
from coloring import *
import plotly.graph_objects as go

#faz a leitura do polígono do arquivo de texto
def readPolygon(caminho):
        vertices = []
        with open(caminho, 'r') as arquivo:
            for linha in arquivo:
                coordenadas = linha.strip().split()
                x, y = float(coordenadas[0]), float(coordenadas[1])
                vertices.append((x, y))
        return vertices

def triangleVertex():
    polygonTxt = 'polygon.txt'
    polygon = readPolygon(polygonTxt)

    verticesx = [vertex[0] for vertex in polygon]
    verticesy = [vertex[1] for vertex in polygon]
    verticesx.append(verticesx[0])
    verticesy.append(verticesy[0])
    frames = []
    erasedEdgesX = []
    erasedEdgesY = []

    #realiza a triangulação do polígono
    triangulationFrames, additionalEdgesX, additionalEdgesY, triangles = earClippingTriangulation(polygon)
    frames = frames + triangulationFrames

    #frame de transição
    frames.append(go.Frame(
        data=[go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'),
                        text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right', name='Polígono'),
            go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines+markers', line=dict(color='black'), name='Arestas da Triangulação'),
            go.Scatter(x=verticesx + [verticesx[0]], y=verticesy + [verticesy[0]], mode='lines', line=dict(color='black'))
        ],
        name=f'frame{len(frames)}'
    ))

    initial_data = [
        go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), 
                text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right', name='Polígono'),
        go.Scatter(x=erasedEdgesX, y=erasedEdgesY, mode='lines', line=dict(color='lightgray'), name='Aresta da Orelha'),
        go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='black'), name='Arestas Cortadas'),
        go.Scatter(x=verticesx + [verticesx[0]], y=verticesy + [verticesy[0]], mode='lines', line=dict(color='black')),
    ]

    fig = go.Figure(
        data=initial_data,
        layout=go.Layout(
            xaxis=dict(range=[min(verticesx) - 1, max(verticesx) + 1], autorange=False),
            yaxis=dict(range=[min(verticesy) - 1, max(verticesy) + 1], autorange=False),
            title="Triangulação do Polígono",
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

    #fig.show()
    fig.write_html("triangulation.html")

    return additionalEdgesX, additionalEdgesY, triangles