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
        self.root.geometry("1250x760")
        self.root.configure(bg="#F4F7FB")

        self.words_data = []
        self.last_costs = {}

        self.setup_styles()
        self.create_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#1F2937",
            rowheight=30,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#1E3A8A",
            foreground="white"
        )

        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")]
        )

    def create_layout(self):
        # Header
        header = tk.Frame(self.root, bg="#1E3A8A", height=80)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Intelligent Dictionary Search Optimization",
            font=("Segoe UI", 22, "bold"),
            bg="#1E3A8A",
            fg="white"
        )
        title.pack(pady=(12, 0))

        subtitle = tk.Label(
            header,
            text="Optimal Binary Search Tree using Dynamic Programming",
            font=("Segoe UI", 11),
            bg="#1E3A8A",
            fg="#BFDBFE"
        )
        subtitle.pack()

        # Main container
        main_frame = tk.Frame(self.root, bg="#F4F7FB")
        main_frame.pack(fill="both", expand=True, padx=20, pady=18)

        # Left panel
        left_panel = tk.Frame(main_frame, bg="#FFFFFF", bd=0, relief="flat")
        left_panel.pack(side="left", fill="y", padx=(0, 15))

        self.create_input_card(left_panel)
        self.create_table_card(left_panel)
        self.create_action_card(left_panel)

        # Right panel
        right_panel = tk.Frame(main_frame, bg="#F4F7FB")
        right_panel.pack(side="right", fill="both", expand=True)

        self.create_result_cards(right_panel)
        self.create_canvas_card(right_panel)
        self.create_comparison_card(right_panel)

    def create_input_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=18, pady=15)
        card.pack(fill="x", padx=0, pady=(0, 15))

        tk.Label(
            card,
            text="Add Dictionary Word",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#111827"
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Enter a word and its search frequency",
            font=("Segoe UI", 9),
            bg="white",
            fg="#6B7280"
        ).pack(anchor="w", pady=(0, 12))

        tk.Label(
            card,
            text="Word",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#374151"
        ).pack(anchor="w")

        self.word_entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid",
            width=28
        )
        self.word_entry.pack(fill="x", pady=(4, 10), ipady=6)

        tk.Label(
            card,
            text="Search Frequency",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#374151"
        ).pack(anchor="w")

        self.freq_entry = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bd=1,
            relief="solid",
            width=28
        )
        self.freq_entry.pack(fill="x", pady=(4, 14), ipady=6)

        add_btn = tk.Button(
            card,
            text="+ Add Word",
            command=self.add_word,
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        add_btn.pack(fill="x", ipady=8)

        sample_btn = tk.Button(
            card,
            text="Load Sample Data",
            command=self.load_sample_data,
            font=("Segoe UI", 10, "bold"),
            bg="#ECFDF5",
            fg="#047857",
            activebackground="#D1FAE5",
            relief="flat",
            cursor="hand2"
        )
        sample_btn.pack(fill="x", pady=(10, 0), ipady=8)

        clear_btn = tk.Button(
            card,
            text="Clear All",
            command=self.clear_all,
            font=("Segoe UI", 10, "bold"),
            bg="#FEF2F2",
            fg="#B91C1C",
            activebackground="#FEE2E2",
            relief="flat",
            cursor="hand2"
        )
        clear_btn.pack(fill="x", pady=(10, 0), ipady=8)

    def create_table_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=18, pady=15)
        card.pack(fill="both", expand=True, pady=(0, 15))

        tk.Label(
            card,
            text="Dictionary Dataset",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#111827"
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Words are sorted internally for BST construction",
            font=("Segoe UI", 9),
            bg="white",
            fg="#6B7280"
        ).pack(anchor="w", pady=(0, 12))

        table_frame = tk.Frame(card, bg="white")
        table_frame.pack(fill="both", expand=True)

        self.table = ttk.Treeview(
            table_frame,
            columns=("Word", "Frequency"),
            show="headings",
            height=9
        )

        self.table.heading("Word", text="Word")
        self.table.heading("Frequency", text="Frequency")

        self.table.column("Word", width=180, anchor="center")
        self.table.column("Frequency", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_action_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=18, pady=15)
        card.pack(fill="x")

        tk.Label(
            card,
            text="Build Algorithms",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#111827"
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Compare different tree construction methods",
            font=("Segoe UI", 9),
            bg="white",
            fg="#6B7280"
        ).pack(anchor="w", pady=(0, 12))

        obst_btn = tk.Button(
            card,
            text="Build OBST - Dynamic Programming",
            command=self.build_obst,
            font=("Segoe UI", 10, "bold"),
            bg="#1E3A8A",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        obst_btn.pack(fill="x", ipady=9)

        greedy_btn = tk.Button(
            card,
            text="Build Greedy BST",
            command=self.build_greedy,
            font=("Segoe UI", 10, "bold"),
            bg="#F97316",
            fg="white",
            activebackground="#EA580C",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        greedy_btn.pack(fill="x", pady=(10, 0), ipady=9)

        balanced_btn = tk.Button(
            card,
            text="Build Balanced BST",
            command=self.build_balanced,
            font=("Segoe UI", 10, "bold"),
            bg="#7C3AED",
            fg="white",
            activebackground="#6D28D9",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        balanced_btn.pack(fill="x", pady=(10, 0), ipady=9)

    def create_result_cards(self, parent):
        cards_frame = tk.Frame(parent, bg="#F4F7FB")
        cards_frame.pack(fill="x", pady=(0, 15))

        self.algorithm_card = self.create_stat_card(
            cards_frame,
            "Selected Algorithm",
            "Not selected",
            "#EFF6FF",
            "#1E3A8A"
        )
        self.algorithm_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.cost_card = self.create_stat_card(
            cards_frame,
            "Search Cost",
            "-",
            "#ECFDF5",
            "#047857"
        )
        self.cost_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.root_card = self.create_stat_card(
            cards_frame,
            "Root Node",
            "-",
            "#FFF7ED",
            "#C2410C"
        )
        self.root_card.pack(side="left", fill="both", expand=True)

    def create_stat_card(self, parent, title, value, bg_color, value_color):
        card = tk.Frame(parent, bg=bg_color, padx=18, pady=14)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg="#374151"
        ).pack(anchor="w")

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 15, "bold"),
            bg=bg_color,
            fg=value_color
        )
        value_label.pack(anchor="w", pady=(5, 0))

        card.value_label = value_label
        return card

    def create_canvas_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=15, pady=15)
        card.pack(fill="both", expand=True, pady=(0, 15))

        top = tk.Frame(card, bg="white")
        top.pack(fill="x")

        tk.Label(
            top,
            text="Tree Visualization",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#111827"
        ).pack(side="left")

        tk.Label(
            top,
            text="Each node shows word and frequency",
            font=("Segoe UI", 9),
            bg="white",
            fg="#6B7280"
        ).pack(side="right")

        self.canvas = tk.Canvas(
            card,
            width=850,
            height=390,
            bg="#F9FAFB",
            highlightthickness=1,
            highlightbackground="#E5E7EB"
        )
        self.canvas.pack(fill="both", expand=True, pady=(12, 0))

        self.canvas.create_text(
            430,
            190,
            text="Build a tree to view visualization",
            font=("Segoe UI", 14, "bold"),
            fill="#9CA3AF"
        )

    def create_comparison_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=15, pady=12)
        card.pack(fill="x")

        tk.Label(
            card,
            text="Algorithm Analysis",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#111827"
        ).pack(anchor="w")

        self.comparison_label = tk.Label(
            card,
            text="OBST minimizes expected search cost. Greedy and Balanced BST are used for comparison.",
            font=("Segoe UI", 10),
            bg="white",
            fg="#374151",
            justify="left"
        )
        self.comparison_label.pack(anchor="w", pady=(6, 0))

    def add_word(self):
        word = self.word_entry.get().strip().lower()
        freq = self.freq_entry.get().strip()

        if word == "" or freq == "":
            messagebox.showerror("Input Error", "Please enter both word and frequency.")
            return

        if not freq.isdigit():
            messagebox.showerror("Input Error", "Frequency must be a positive number.")
            return

        freq = int(freq)

        if freq <= 0:
            messagebox.showerror("Input Error", "Frequency must be greater than zero.")
            return

        for existing_word, _ in self.words_data:
            if existing_word == word:
                messagebox.showerror("Duplicate Word", "This word already exists.")
                return

        self.words_data.append((word, freq))
        self.update_table()

        self.word_entry.delete(0, tk.END)
        self.freq_entry.delete(0, tk.END)

    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for word, freq in sorted(self.words_data, key=lambda x: x[0]):
            self.table.insert("", tk.END, values=(word, freq))

    def clear_all(self):
        self.words_data = []
        self.last_costs = {}
        self.update_table()
        self.canvas.delete("all")

        self.canvas.create_text(
            430,
            190,
            text="Build a tree to view visualization",
            font=("Segoe UI", 14, "bold"),
            fill="#9CA3AF"
        )

        self.update_result_cards("Not selected", "-", "-")

        self.comparison_label.config(
            text="OBST minimizes expected search cost. Greedy and Balanced BST are used for comparison."
        )

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

    def update_result_cards(self, algorithm, cost, root_word):
        self.algorithm_card.value_label.config(text=algorithm)
        self.cost_card.value_label.config(text=str(cost))
        self.root_card.value_label.config(text=str(root_word))

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
            messagebox.showerror("Error", "Please add words first.")
            return

        sorted_by_freq = sorted(self.words_data, key=lambda x: x[1], reverse=True)

        root = None
        for word, freq in sorted_by_freq:
            root = self.insert_bst(root, word, freq)

        cost = self.calculate_cost(root)
        self.last_costs["Greedy BST"] = cost

        self.update_result_cards("Greedy BST", cost, root.word)
        self.draw_tree(root, "#FFF7ED", "#EA580C")
        self.show_comparison("Greedy BST", cost)

    def build_balanced(self):
        if not self.words_data:
            messagebox.showerror("Error", "Please add words first.")
            return

        sorted_words = sorted(self.words_data, key=lambda x: x[0])
        root = self.create_balanced_bst(sorted_words, 0, len(sorted_words) - 1)

        cost = self.calculate_cost(root)
        self.last_costs["Balanced BST"] = cost

        self.update_result_cards("Balanced BST", cost, root.word)
        self.draw_tree(root, "#F5F3FF", "#7C3AED")
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
            messagebox.showerror("Error", "Please add words first.")
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

        final_cost = cost[0][n - 1]
        self.last_costs["OBST"] = final_cost

        self.update_result_cards("OBST - DP", final_cost, root.word)
        self.draw_tree(root, "#EFF6FF", "#2563EB")
        self.show_comparison("Optimal BST using Dynamic Programming", final_cost)

    def create_obst_tree(self, words, freq, root_table, i, j):
        if i > j:
            return None

        r = root_table[i][j]
        root = Node(words[r], freq[r])

        root.left = self.create_obst_tree(words, freq, root_table, i, r - 1)
        root.right = self.create_obst_tree(words, freq, root_table, r + 1, j)

        return root

    def draw_tree(self, root, node_fill, node_outline):
        self.canvas.delete("all")

        if root is None:
            return

        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 850

        self.draw_node(
            node=root,
            x=canvas_width // 2,
            y=55,
            gap=canvas_width // 4,
            node_fill=node_fill,
            node_outline=node_outline
        )

    def draw_node(self, node, x, y, gap, node_fill, node_outline):
        if node is None:
            return

        radius = 34

        if node.left:
            child_x = x - gap
            child_y = y + 90
            self.canvas.create_line(
                x,
                y + radius,
                child_x,
                child_y - radius,
                fill="#94A3B8",
                width=2
            )
            self.draw_node(node.left, child_x, child_y, max(gap // 2, 45), node_fill, node_outline)

        if node.right:
            child_x = x + gap
            child_y = y + 90
            self.canvas.create_line(
                x,
                y + radius,
                child_x,
                child_y - radius,
                fill="#94A3B8",
                width=2
            )
            self.draw_node(node.right, child_x, child_y, max(gap // 2, 45), node_fill, node_outline)

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=node_fill,
            outline=node_outline,
            width=3
        )

        display_word = node.word
        if len(display_word) > 9:
            display_word = display_word[:8] + "..."

        self.canvas.create_text(
            x,
            y - 7,
            text=display_word,
            font=("Segoe UI", 9, "bold"),
            fill="#111827"
        )

        self.canvas.create_text(
            x,
            y + 12,
            text=f"f = {node.freq}",
            font=("Segoe UI", 8),
            fill="#374151"
        )

    def show_comparison(self, algorithm_name, cost):
        text = (
            f"Selected Algorithm: {algorithm_name}\n"
            f"Total Weighted Search Cost: {cost}\n"
            f"Meaning: Lower search cost gives faster dictionary search performance.\n"
        )

        if self.last_costs:
            text += "\nCurrent Recorded Costs:\n"
            for algo, algo_cost in self.last_costs.items():
                text += f"• {algo}: {algo_cost}\n"

        self.comparison_label.config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    app = DictionarySearchGUI(root)
    root.mainloop()
