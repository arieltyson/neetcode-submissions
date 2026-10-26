class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # ---------- Disjoint Set Union (union by rank + path compression) ----------
        parent = list(range(n))
        rank = [0] * n

        def find(node):
            root = node
            while parent[root] != root:
                root = parent[root]
            while parent[node] != root:          # path compression (iterative)
                parent[node], node = root, parent[node]
            return root

        def union(node_a, node_b):
            root_a, root_b = find(node_a), find(node_b)
            if root_a == root_b:
                return False
            if rank[root_a] < rank[root_b]:
                root_a, root_b = root_b, root_a
            parent[root_b] = root_a
            if rank[root_a] == rank[root_b]:
                rank[root_a] += 1
            return True

        # ---------- Tarjan bridge finding on the contracted component graph ----------
        component_graph = defaultdict(list)   # component root -> [(neighbor root, edge index)]
        discovery_time = {}
        low_link = {}
        bridge_edges = set()
        timer = 0

        def dfs(node, incoming_edge_index):
            nonlocal timer
            discovery_time[node] = low_link[node] = timer
            timer += 1
            for neighbor, edge_index in component_graph[node]:
                if edge_index == incoming_edge_index:      # skip the exact edge we came in on
                    continue
                if neighbor in discovery_time:             # back edge
                    low_link[node] = min(low_link[node], discovery_time[neighbor])
                else:                                      # tree edge
                    dfs(neighbor, edge_index)
                    low_link[node] = min(low_link[node], low_link[neighbor])
                    if low_link[neighbor] > discovery_time[node]:
                        bridge_edges.add(edge_index)

        # ---------- Group edge indices by weight ----------
        edges_by_weight = defaultdict(list)
        for edge_index, (_, _, weight) in enumerate(edges):
            edges_by_weight[weight].append(edge_index)

        critical_edges, pseudo_critical_edges = [], []

        for weight in sorted(edges_by_weight):
            component_graph.clear()
            discovery_time.clear()
            low_link.clear()
            bridge_edges.clear()
            timer = 0
            candidate_edges = []

            # 1) Contract: map each edge onto the components formed by all lighter edges
            for edge_index in edges_by_weight[weight]:
                node_u, node_v, _ = edges[edge_index]
                root_u, root_v = find(node_u), find(node_v)
                if root_u != root_v:                       # otherwise it would close a cycle -> never in an MST
                    component_graph[root_u].append((root_v, edge_index))
                    component_graph[root_v].append((root_u, edge_index))
                    candidate_edges.append(edge_index)

            # 2) Bridges of the contracted graph are critical, other candidates are pseudo-critical
            for component in list(component_graph):
                if component not in discovery_time:
                    dfs(component, -1)

            for edge_index in candidate_edges:
                if edge_index in bridge_edges:
                    critical_edges.append(edge_index)
                else:
                    pseudo_critical_edges.append(edge_index)

            # 3) Merge components with this weight class before moving to the next weight
            for edge_index in candidate_edges:
                union(edges[edge_index][0], edges[edge_index][1])

        return [critical_edges, pseudo_critical_edges]