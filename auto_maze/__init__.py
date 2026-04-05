import random
from typing import Final, Literal

START: Final[str] = 'S'
END: Final[str] = 'E'
WALL: Final[int] = 1
PATH: Final[int] = 0
SOLUTION: Final[int] = 2


maze = [
    [1, 1, 1, 1, 1],
    [1, 'S', 0, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 0, 0,'E', 1],
    [1, 1, 1, 1, 1]
]

class Maze:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        # 四个方向：上下左右
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    def get_start(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == START:
                    return (i, j)
        return None
    def get_end(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == END:
                    return (i, j)
        return None

    # 判断移动是否合法（不越界、不是墙、未走过）
    def is_valid_move(self, pos):
        x, y = pos
        return 0 <= x < self.rows and 0 <= y < self.cols and self.maze[x][y] != WALL

    # 获取所有可移动方向
    def get_valid_moves(self, pos):
        moves = []
        for dx, dy in self.directions:
            new_x = pos[0] + dx
            new_y = pos[1] + dy
            if self.is_valid_move((new_x, new_y)):
                moves.append((new_x, new_y))
        return moves

    # 递归求解迷宫（DFS + 路径记录，防死循环）
    def solution(self, start=None, history=None):
        # 初始化起点和路径
        if start is None:
            start = self.get_start()  # 默认起点，可自行修改
        if history is None:
            history = []

        x, y = start
        # 终止条件：到达终点（这里设为右下角，可修改）
        end = self.get_end()
        if start == end:
            return history + [start]

        # 防止重复走同一个位置（核心：避免递归死循环）
        if start in history:
            return None

        # 记录当前位置
        new_history = history + [start]

        # 遍历所有可行方向
        for next_pos in self.get_valid_moves(start):
            result = self.solution(next_pos, new_history)
            if result:
                return result

        # 无路可走，回溯
        return None
    def format_solution(self, path):
        formated_solution = []
        temp1 = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if (i, j) in path:
                    temp1.append(SOLUTION)
                else:
                    temp1.append(self.maze[i][j])
            formated_solution.append(temp1)
            temp1 = []
        return formated_solution


# ===================== 测试示例 =====================
if __name__ == '__main__':
    class_maze = Maze(maze)
    result = class_maze.solution()
    print("迷宫求解路径（坐标）：", class_maze.format_solution(result))
    if result:
        print("✅ 找到迷宫解法！")
    else:
        print("❌ 迷宫无解")