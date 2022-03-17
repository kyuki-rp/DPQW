import numpy as np
from scipy.sparse import csr_matrix, lil_matrix


class QuantumWalk():
    '''
    Quantum walk class.
    '''
    def __init__(self):
        pass
   
    def get_matrix(self, assignments, edges, coin, xi):
        amp = np.cos(np.radians(xi)) + np.sin(np.radians(xi))*1j
        U = amp * coin

        # graph_edges
        graph_edges = np.array([[edge.initial_node.identifier, edge.final_node.identifier, edge.data['edge_type'], edge] for edge in edges])
        for key, val in {'s0':0,'h+':1,'h-':2,'s1':3,'v+':4,'v-':5}.items():
            graph_edges = np.where(graph_edges==key, val, graph_edges)

        graph_edges = np.array(sorted(graph_edges, key=lambda x:(x[1], x[2])))

        boundary_node_identifiers = [assignment.split("->")[0] for assignment in assignments.keys()]
        
        # get_evolve_matrix
        dim = graph_edges.shape[0]
        evolve_matrix = lil_matrix((dim+1, dim+1))*(1+0j)
        for dim_row in range(dim):
            target = graph_edges[dim_row, 0]
            dim_cols = np.where(graph_edges[:, 1]==target)[0]
            row_edge_type = graph_edges[dim_row, 2]

            for dim_col in dim_cols:
                col_edge_type = graph_edges[dim_col, 2]
                if target not in boundary_node_identifiers:
                    evolve_matrix[dim_row, dim_col] = U[row_edge_type, col_edge_type]

        evolve_matrix[-1, -1] = 1

        # add boundary
        Us = []
        for usi in range(2):
            Utemp = evolve_matrix.copy()

            for key, val in assignments.items():
                no = np.where((graph_edges[:, 0]==key.split("->")[0]) & (graph_edges[:, 1]==key.split("->")[1]))[0][0]
                if type(val[usi]) in [int, float]:
                    Utemp[no, -1] = val[usi]
                else:
                    reflect_no = np.where((graph_edges[:, 0]==key.split("->")[1]) & (graph_edges[:, 1]==key.split("->")[0]))[0][0]
                    Utemp[no, :] = Utemp[reflect_no, :]

            Us.append(Utemp.tocsr())

        # inflow
        inflow = lil_matrix((1, dim+1)).T
        inflow[-1, 0] = 1
        inflow = inflow.tocsr()
        
        return graph_edges, Us, inflow

