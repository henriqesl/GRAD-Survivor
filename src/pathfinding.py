import heapq

def astar(grid, start, end):
    """
    Encontra o caminho mais curto usando o algoritmo A*.
    :param grid: Matriz 2D (0 para livre, 1 para obstáculo).
    :param start: Tupla (x, y) da posição inicial no grid.
    :param end: Tupla (x, y) da posição final no grid.
    :return: Lista de tuplas (x, y) representando o caminho, ou None se não houver caminho.
    """
    rows, cols = len(grid), len(grid[0])
    
    # Movimentos possíveis (8 direções, incluindo diagonais)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: (start[0] - end[0])**2 + (start[1] - end[1])**2}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == end:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.reverse()
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            
            if not (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows):
                continue
                
            if grid[neighbor[1]][neighbor[0]] == 1: # Se for um obstáculo
                continue
                
            tentative_g_score = gscore[current] + 1

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + ((neighbor[0] - end[0])**2 + (neighbor[1] - end[1])**2)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
                
    return None # Nenhum caminho encontrado