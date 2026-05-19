import tkinter as tk
from tkinter import ttk, messagebox


class Node:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq
        self.left = None
        self.right = None


class DictionarySearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Dictionary Search Optimization - OBST")
        self.root.geometry("1100x700")

        self.words_data = []

        title = tk.Label(
            root,
            text="Intelligent Dictionary Search Optimization using OBST",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Word:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.word_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.word_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Frequency:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        self.freq_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.freq_entry.grid(row=0, column=3, padx=5)

        add_btn = tk.Button(input_frame, text="Add Word", command=self.add_word, bg="#4CAF50", fg="white")
        add_btn.grid(row=0, column=4, padx=5)

        sample_btn = tk.Button(input_frame, text="Load Sample Data", command=self.load_sample_data)
        sample_btn.grid(row=0, column=5, padx=5)

        clear_btn = tk.Button(input_frame, text="Clear", command=self.clear_all, bg="#f44336", fg="white")
        clear_btn.grid(row=0, column=6, padx=5)

        table_frame = tk.Frame(root)
        table_frame.pack(pady=10)

        self.table = ttk.Treeview(table_frame, columns=("Word", "Frequency"), show="headings", height=6)
        self.table.heading("Word", text="Word")
        self.table.heading("Frequency", text="Frequency")
        self.table.column("Word", width=180)
        self.table.column("Frequency", width=120)
        self.table.pack()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Build OBST - Dynamic Programming",
            command=self.build_obst,
            bg="#2196F3",
            fg="white",
            width=28
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Build Greedy BST",
            command=self.build_greedy,
            bg="#FF9800",
            fg="white",
            width=22
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            button_frame,
            text="Build Balanced BST",
            command=self.build_balanced,
            bg="#9C27B0",
            fg="white",
            width=22
        ).grid(row=0, column=2, padx=10)

        self.result_label = tk.Label(
            root,
            text="Result will be displayed here",
            font=("Arial", 12, "bold"),
            fg="blue"
        )
        self.result_label.pack(pady=5)

        self.canvas = tk.Canvas(root, width=1050, height=360, bg="white")
        self.canvas.pack(pady=10)

        self.comparison_label = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            justify="left"
        )
        self.comparison_label.pack(pady=5)

    def add_word(self):
        word = self.word_entry.get().strip().lower()
        freq = self.freq_entry.get().strip()

        if word == "" or freq == "":
            messagebox.showerror("Error", "Please enter both word and frequency")
            return

        if not freq.isdigit():
            messagebox.showerror("Error", "Frequency must be a number")
            return

        freq = int(freq)

        for existing_word, _ in self.words_data:
            if existing_word == word:
                messagebox.showerror("Error", "Word already exists")
                return

        self.words_data.append((word, freq))
        self.update_table()

        self.word_entry.delete(0, tk.END)
        self.freq_entry.delete(0, tk.END)

    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for word, freq in self.words_data:
            self.table.insert("", tk.END, values=(word, freq))

    def clear_all(self):
        self.words_data = []
        self.update_table()
        self.canvas.delete("all")
        self.result_label.config(text="Result will be displayed here")
        self.comparison_label.config(text="")

    def load_sample_data(self):
        self.words_data = [
            ("apple", 30),
            ("ball", 10),
            ("cat", 50),
            ("dog", 5),
            ("elephant", 20),
            ("fish", 15),
            ("goat", 25)
        ]
        self.update_table()

    def insert_bst(self, root, word, freq):
        if root is None:
            return Node(word, freq)

        if word < root.word:
            root.left = self.insert_bst(root.left, word, freq)
        else:
            root.right = self.insert_bst(root.right, word, freq)

        return root

    def calculate_cost(self, root, level=1):
        if root is None:
            return 0

        return (
            root.freq * level
            + self.calculate_cost(root.left, level + 1)
            + self.calculate_cost(root.right, level + 1)
        )

    def build_greedy(self):
        if not self.words_data:
            messagebox.showerror("Error", "Please add words first")
            return

        sorted_by_freq = sorted(self.words_data, key=lambda x: x[1], reverse=True)

        root = None
        for word, freq in sorted_by_freq:
            root = self.insert_bst(root, word, freq)

        cost = self.calculate_cost(root)

        self.result_label.config(
            text=f"Greedy BST Search Cost: {cost} | Root: {root.word}"
        )

        self.draw_tree(root)
        self.show_comparison("Greedy BST", cost)

    def build_balanced(self):
        if not self.words_data:
            messagebox.showerror("Error", "Please add words first")
            return

        sorted_words = sorted(self.words_data, key=lambda x: x[0])
        root = self.create_balanced_bst(sorted_words, 0, len(sorted_words) - 1)

        cost = self.calculate_cost(root)

        self.result_label.config(
            text=f"Balanced BST Search Cost: {cost} | Root: {root.word}"
        )

        self.draw_tree(root)
        self.show_comparison("Divide and Conquer Balanced BST", cost)

    def create_balanced_bst(self, arr, start, end):
        if start > end:
            return None

        mid = (start + end) // 2
        word, freq = arr[mid]

        root = Node(word, freq)
        root.left = self.create_balanced_bst(arr, start, mid - 1)
        root.right = self.create_balanced_bst(arr, mid + 1, end)

        return root

    def build_obst(self):
        if not self.words_data:
            messagebox.showerror("Error", "Please add words first")
            return

        data = sorted(self.words_data, key=lambda x: x[0])
        words = [item[0] for item in data]
        freq = [item[1] for item in data]
        n = len(words)

        cost = [[0 for _ in range(n)] for _ in range(n)]
        root_table = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            cost[i][i] = freq[i]
            root_table[i][i] = i

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                cost[i][j] = float("inf")

                total_freq = sum(freq[i:j + 1])

                for r in range(i, j + 1):
                    left_cost = cost[i][r - 1] if r > i else 0
                    right_cost = cost[r + 1][j] if r < j else 0

                    current_cost = left_cost + right_cost + total_freq

                    if current_cost < cost[i][j]:
                        cost[i][j] = current_cost
                        root_table[i][j] = r

        root = self.create_obst_tree(words, freq, root_table, 0, n - 1)

        self.result_label.config(
            text=f"OBST Minimum Search Cost: {cost[0][n - 1]} | Root: {root.word}"
        )

        self.draw_tree(root)
        self.show_comparison("Optimal BST using Dynamic Programming", cost[0][n - 1])

    def create_obst_tree(self, words, freq, root_table, i, j):
        if i > j:
            return None

        r = root_table[i][j]
        root = Node(words[r], freq[r])

        root.left = self.create_obst_tree(words, freq, root_table, i, r - 1)
        root.right = self.create_obst_tree(words, freq, root_table, r + 1, j)

        return root

    def draw_tree(self, root):
        self.canvas.delete("all")

        if root is None:
            return

        self.draw_node(root, 525, 40, 230)

    def draw_node(self, node, x, y, gap):
        if node is None:
            return

        radius = 28

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="#E3F2FD",
            outline="#1565C0",
            width=2
        )

        self.canvas.create_text(
            x,
            y - 5,
            text=node.word,
            font=("Arial", 9, "bold")
        )

        self.canvas.create_text(
            x,
            y + 12,
            text=f"f={node.freq}",
            font=("Arial", 8)
        )

        if node.left:
            child_x = x - gap
            child_y = y + 80

            self.canvas.create_line(
                x,
                y + radius,
                child_x,
                child_y - radius,
                width=2
            )

            self.draw_node(node.left, child_x, child_y, gap // 2)

        if node.right:
            child_x = x + gap
            child_y = y + 80

            self.canvas.create_line(
                x,
                y + radius,
                child_x,
                child_y - radius,
                width=2
            )

            self.draw_node(node.right, child_x, child_y, gap // 2)

    def show_comparison(self, algorithm_name, cost):
        self.comparison_label.config(
            text=f"Selected Algorithm: {algorithm_name}\n"
                 f"Total Weighted Search Cost: {cost}\n"
                 f"Lower cost means better dictionary search performance."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = DictionarySearchGUI(root)
    root.mainloop()