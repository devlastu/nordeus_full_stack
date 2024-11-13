def dfs(matrix, visited, i, j, island_cells):
    # Definišemo pravce kretanja (gore, dole, levo, desno)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    stack = [(i, j)]  # Početna pozicija
    visited[i][j] = True
    island_cells.append((i, j))  # Dodajemo početnu ćeliju ostrva

    while stack:
        x, y = stack.pop()

        # Prolazimo kroz sve susedne ćelije
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Proveravamo da li je nova pozicija u matrici i nije posetena
            if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and not visited[nx][ny] and matrix[nx][ny] > 0:
                visited[nx][ny] = True
                stack.append((nx, ny))
                island_cells.append((nx, ny))  # Dodajemo ćeliju ostrva

    return island_cells


def find_islands(matrix):
    visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
    islands = []  # Svi ostrvi
    island_avg_heights = []  # Prosečne visine ostrva

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0 and not visited[i][j]:  # Ako ćelija predstavlja kopno i nije posetena
                island_cells = []  # Ćelije koje čine ovo ostrvo
                # Pokrećemo DFS i nalazimo sve povezane ćelije ostrva
                island_cells = dfs(matrix, visited, i, j, island_cells)

                # Izračunavamo prosečnu visinu ostrva
                total_height = sum(matrix[x][y] for x, y in island_cells)
                avg_height = total_height / len(island_cells)
                islands.append(island_cells)
                island_avg_heights.append(avg_height)

    return islands, island_avg_heights


def find_island_with_max_avg_height(islands, avg_heights):
    max_avg_height = max(avg_heights)
    island_index = avg_heights.index(max_avg_height)
    max_avg_island = islands[island_index]

    return max_avg_island, max_avg_height
