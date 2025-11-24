import tkinter as tk
from tkinter import ttk

# 1. 初始化主窗口
root = tk.Tk()
root.title("数独求解可视化工具 - V1.0")
root.geometry("500x750")
root.resizable(False, False)

# 2. 创建9×9网格容器
grid_frame = ttk.Frame(root, padding="20")
grid_frame.pack(expand=True, fill=tk.BOTH)

# 存储9×9输入框的二维列表
sudoku_entries = [[None for _ in range(9)] for _ in range(9)]

# 宫格颜色配置（3×3宫交替区分）
cell_colors = []
for row in range(9):
    row_colors = []
    for col in range(9):
        if (row // 3 + col // 3) % 2 == 0:
            row_colors.append("#f0f0f0")  # 浅色
        else:
            row_colors.append("#ffffff")  # 白色
    cell_colors.append(row_colors)

# 循环创建9×9输入框
for row in range(9):
    for col in range(9):
        entry = tk.Entry(
            grid_frame,
            width=3,
            font=("Arial", 16, "bold"),
            justify=tk.CENTER,
            state="normal"  # 改为 "normal" 让用户可以编辑
        )
        entry.grid(
            row=row, column=col,
            padx=1 if (col + 1) % 3 != 0 else 3,
            pady=1 if (row + 1) % 3 != 0 else 3,
            sticky="nsew"
        )
        entry.config(background=cell_colors[row][col])
        sudoku_entries[row][col] = entry

# 网格自适应配置
for row in range(9):
    grid_frame.grid_rowconfigure(row, weight=1)
for col in range(9):
    grid_frame.grid_columnconfigure(col, weight=1)

# 3. 数字显示核心函数
def fill_sudoku(sudoku_data):
    for row in range(9):
        for col in range(9):
            value = sudoku_data[row][col]
            entry = sudoku_entries[row][col]
            entry.config(state="normal")
            entry.delete(0, tk.END)
            if value != 0:
                entry.insert(0, str(value))

def clear_sudoku():
    for row in range(9):
        for col in range(9):
            entry = sudoku_entries[row][col]
            entry.config(state="normal")
            entry.delete(0, tk.END)
    # 清空性能数据
    update_performance(None)

# 示例数独数据
sample_sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# 4. 功能按钮区
button_frame = ttk.Frame(root, padding="0 10 0 20")
button_frame.pack(fill=tk.X, padx=20)

fill_btn = ttk.Button(button_frame, text="填充示例数独", command=lambda: fill_sudoku(sample_sudoku))
fill_btn.pack(side=tk.LEFT, padx=5)

clear_btn = ttk.Button(button_frame, text="清空网格", command=clear_sudoku)
clear_btn.pack(side=tk.LEFT, padx=5)

# 5. 算法选择区
algorithm_frame = ttk.Frame(root, padding="0 0 0 10")
algorithm_frame.pack(fill=tk.X, padx=20)

alg_label = ttk.Label(algorithm_frame, text="选择求解算法：")
alg_label.pack(side=tk.LEFT, padx=5)

# 改用 ttk.Combobox
algorithm_var = tk.StringVar(value="请选择算法")
alg_options = ["基础DFS算法（成员A）", "进阶CSP算法（成员C）"]

alg_menu = ttk.Combobox(algorithm_frame, textvariable=algorithm_var, values=alg_options, state="readonly")
alg_menu.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

# 6. 性能对比板块
performance_frame = ttk.LabelFrame(root, text="算法性能统计", padding="10")
performance_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)

# 性能指标标签
perf_labels = {}

metrics = [
    ("algorithm", "算法名称：", "未运行"),
    ("time", "执行时间：", "0.000 秒"),
    ("nodes", "搜索节点数：", "0"),
    ("backtracks", "回溯次数：", "0"),
    ("status", "求解状态：", "待求解")
]

for i, (key, label_text, default_value) in enumerate(metrics):
    row_frame = ttk.Frame(performance_frame)
    row_frame.pack(fill=tk.X, pady=3)
    
    label = ttk.Label(row_frame, text=label_text, font=("Arial", 10))
    label.pack(side=tk.LEFT)
    
    value_label = ttk.Label(row_frame, text=default_value, font=("Arial", 10, "bold"), foreground="#0066cc")
    value_label.pack(side=tk.LEFT, padx=5)
    
    perf_labels[key] = value_label

# 更新性能数据的函数
def update_performance(perf_data):
    """
    更新性能显示
    perf_data: 字典，包含 algorithm, time, nodes, backtracks, status
    例如: {
        'algorithm': '基础DFS算法',
        'time': 0.123,
        'nodes': 456,
        'backtracks': 78,
        'status': '成功'
    }
    """
    if perf_data is None:
        # 重置为默认值
        perf_labels['algorithm'].config(text="未运行")
        perf_labels['time'].config(text="0.000 秒")
        perf_labels['nodes'].config(text="0")
        perf_labels['backtracks'].config(text="0")
        perf_labels['status'].config(text="待求解", foreground="#666666")
    else:
        perf_labels['algorithm'].config(text=perf_data.get('algorithm', '未知'))
        perf_labels['time'].config(text=f"{perf_data.get('time', 0):.3f} 秒")
        perf_labels['nodes'].config(text=str(perf_data.get('nodes', 0)))
        perf_labels['backtracks'].config(text=str(perf_data.get('backtracks', 0)))
        
        status = perf_data.get('status', '未知')
        if status == '成功':
            perf_labels['status'].config(text=status, foreground="#00aa00")
        elif status == '失败':
            perf_labels['status'].config(text=status, foreground="#cc0000")
        else:
            perf_labels['status'].config(text=status, foreground="#666666")

# 7. 求解按钮
solve_frame = ttk.Frame(root, padding="0 0 0 20")
solve_frame.pack(fill=tk.X, padx=20)

def solve_sudoku():
    """模拟求解过程（示例）"""
    import time
    import random
    
    selected_alg = algorithm_var.get()
    if selected_alg == "请选择算法":
        perf_labels['status'].config(text="请先选择算法", foreground="#cc0000")
        return
    
    # 模拟求解过程
    start_time = time.time()
    time.sleep(0.1)  # 模拟计算时间
    end_time = time.time()
    
    # 模拟性能数据
    perf_data = {
        'algorithm': selected_alg,
        'time': end_time - start_time,
        'nodes': random.randint(100, 1000),
        'backtracks': random.randint(10, 200),
        'status': '成功'
    }
    
    update_performance(perf_data)

solve_btn = ttk.Button(solve_frame, text="开始求解", command=solve_sudoku)
solve_btn.pack(side=tk.LEFT, padx=5)

compare_btn = ttk.Button(solve_frame, text="对比所有算法", command=lambda: None)
compare_btn.pack(side=tk.LEFT, padx=5)

# 8. 启动主循环
root.mainloop()
