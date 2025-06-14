import sys
import random

class Node:
    def __init__(self, PID, niceValue=0, vruntime=0, dealtExec=0, timeToExec=10):
        self.color = 1
        self.PID = PID
        self.niceValue = niceValue
        self.weight = 1024 // (1 + niceValue)
        self.vruntime = vruntime
        self.dealtExec = dealtExec
        self.timeToExec = timeToExec
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = 0
        self.root = self.TNULL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, node):
        node.left = self.TNULL
        node.right = self.TNULL
        node.parent = None
        y = None
        x = self.root
        while x != self.TNULL:
            y = x
            if node.vruntime < x.vruntime:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y == None:
            self.root = node
        elif node.vruntime < y.vruntime:
            y.left = node
        else:
            y.right = node
        if node.parent == None:
            node.color = 0
            return
        if node.parent.parent == None:
            return
        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent and k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u and u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u and u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def delete_min(self):
        min_node = self.minimum(self.root)
        self.delete_node(min_node)
        return min_node

    def delete_node(self, node):
        def transplant(u, v):
            if u.parent == None:
                self.root = v
            elif u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
            v.parent = u.parent
        y = node
        y_original_color = y.color
        if node.left == self.TNULL:
            x = node.right
            transplant(node, node.right)
        elif node.right == self.TNULL:
            x = node.left
            transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

    def print_tree(self, node=None, indent="", last=True):
        if node is None:
            node = self.root
        if node != self.TNULL:
            print(indent, "`-- " if last else "|-- ", f"P{node.PID} v={node.vruntime:.2f} w={node.weight} t={node.timeToExec:.2f}", sep="")
            self.print_tree(node.left, indent + ("    " if last else "|   "), False)
            self.print_tree(node.right, indent + ("    " if last else "|   "), True)

if __name__ == "__main__":
    tree = RedBlackTree()
    for pid in range(1, 7):
        nice = random.randint(0, 10)
        exec_time = random.uniform(10, 20)
        task = Node(PID=pid, niceValue=nice, vruntime=0, timeToExec=exec_time)
        tree.insert(task)
    print("\nInitial Task Tree:")
    tree.print_tree()
    print("\n--- Starting Scheduling Simulation ---\n")
    tick = 0
    while tree.root != tree.TNULL:
        tick += 1
        task = tree.delete_min()
        delta_exec = random.uniform(1, 5)
        if delta_exec > task.timeToExec:
            delta_exec = task.timeToExec
        task.dealtExec += delta_exec
        task.vruntime += delta_exec * (1024 / task.weight)
        task.timeToExec -= delta_exec
        print(f"T{tick} : Ran PID {task.PID} for {delta_exec:.2f} ms, Remaining: {task.timeToExec:.2f} ms, vruntime: {task.vruntime:.2f}")
        if task.timeToExec > 0:
            tree.insert(task)
        print("\nCurrent Task Tree:")
        tree.print_tree()
        print("\n")
    print("--- All Tasks Completed ---")




"""
Code output:

Initial Task Tree:
`-- P2 v=0.00 w=113 t=13.50
    |-- P1 v=0.00 w=113 t=14.68
    `-- P4 v=0.00 w=93 t=16.41
        |-- P3 v=0.00 w=128 t=10.52
        `-- P5 v=0.00 w=170 t=19.32
            `-- P6 v=0.00 w=113 t=10.70

--- Starting Scheduling Simulation ---

T1 : Ran PID 1 for 1.22 ms, Remaining: 13.46 ms, vruntime: 11.03

Current Task Tree:
`-- P2 v=0.00 w=113 t=13.50
    `-- P4 v=0.00 w=93 t=16.41
        |-- P3 v=0.00 w=128 t=10.52
        `-- P6 v=0.00 w=113 t=10.70
            |-- P5 v=0.00 w=170 t=19.32
            `-- P1 v=11.03 w=113 t=13.46


T2 : Ran PID 2 for 2.63 ms, Remaining: 10.87 ms, vruntime: 23.85

Current Task Tree:
`-- P4 v=0.00 w=93 t=16.41
    |-- P3 v=0.00 w=128 t=10.52
    `-- P6 v=0.00 w=113 t=10.70
        |-- P5 v=0.00 w=170 t=19.32
        `-- P1 v=11.03 w=113 t=13.46
            `-- P2 v=23.85 w=113 t=10.87


T3 : Ran PID 3 for 3.41 ms, Remaining: 7.10 ms, vruntime: 27.32

Current Task Tree:
`-- P4 v=0.00 w=93 t=16.41
    `-- P6 v=0.00 w=113 t=10.70
        |-- P5 v=0.00 w=170 t=19.32
        `-- P1 v=11.03 w=113 t=13.46
            `-- P2 v=23.85 w=113 t=10.87
                `-- P3 v=27.32 w=128 t=7.10


T4 : Ran PID 4 for 2.95 ms, Remaining: 13.45 ms, vruntime: 32.53

Current Task Tree:
`-- P6 v=0.00 w=113 t=10.70
    |-- P5 v=0.00 w=170 t=19.32
    `-- P1 v=11.03 w=113 t=13.46
        `-- P2 v=23.85 w=113 t=10.87
            `-- P3 v=27.32 w=128 t=7.10
                `-- P4 v=32.53 w=93 t=13.45


T5 : Ran PID 5 for 3.67 ms, Remaining: 15.65 ms, vruntime: 22.12

Current Task Tree:
`-- P6 v=0.00 w=113 t=10.70
    `-- P1 v=11.03 w=113 t=13.46
        `-- P2 v=23.85 w=113 t=10.87
            |-- P5 v=22.12 w=170 t=15.65
            `-- P3 v=27.32 w=128 t=7.10
                `-- P4 v=32.53 w=93 t=13.45


T6 : Ran PID 6 for 3.21 ms, Remaining: 7.49 ms, vruntime: 29.08

Current Task Tree:
`-- P1 v=11.03 w=113 t=13.46
    `-- P2 v=23.85 w=113 t=10.87
        |-- P5 v=22.12 w=170 t=15.65
        `-- P3 v=27.32 w=128 t=7.10
            `-- P4 v=32.53 w=93 t=13.45
                |-- P6 v=29.08 w=113 t=7.49


T7 : Ran PID 1 for 1.29 ms, Remaining: 12.17 ms, vruntime: 22.75

Current Task Tree:
`-- P1 v=22.75 w=113 t=12.17
    |-- P5 v=22.12 w=170 t=15.65
    `-- P2 v=23.85 w=113 t=10.87
        `-- P3 v=27.32 w=128 t=7.10
            `-- P4 v=32.53 w=93 t=13.45
                |-- P6 v=29.08 w=113 t=7.49


T8 : Ran PID 5 for 3.51 ms, Remaining: 12.14 ms, vruntime: 43.26

Current Task Tree:
`-- P1 v=22.75 w=113 t=12.17
    `-- P2 v=23.85 w=113 t=10.87
        `-- P3 v=27.32 w=128 t=7.10
            `-- P4 v=32.53 w=93 t=13.45
                |-- P6 v=29.08 w=113 t=7.49
                `-- P5 v=43.26 w=170 t=12.14


T9 : Ran PID 1 for 4.13 ms, Remaining: 8.04 ms, vruntime: 60.19

Current Task Tree:
`-- P2 v=23.85 w=113 t=10.87
    `-- P3 v=27.32 w=128 t=7.10
        `-- P5 v=43.26 w=170 t=12.14
            |-- P4 v=32.53 w=93 t=13.45
            |   |-- P6 v=29.08 w=113 t=7.49
            `-- P1 v=60.19 w=113 t=8.04


T10 : Ran PID 2 for 3.34 ms, Remaining: 7.53 ms, vruntime: 54.08

Current Task Tree:
`-- P3 v=27.32 w=128 t=7.10
    `-- P5 v=43.26 w=170 t=12.14
        |-- P4 v=32.53 w=93 t=13.45
        |   |-- P6 v=29.08 w=113 t=7.49
        `-- P1 v=60.19 w=113 t=8.04
            |-- P2 v=54.08 w=113 t=7.53


T11 : Ran PID 3 for 3.06 ms, Remaining: 4.04 ms, vruntime: 51.80

Current Task Tree:
`-- P5 v=43.26 w=170 t=12.14
    |-- P4 v=32.53 w=93 t=13.45
    |   |-- P6 v=29.08 w=113 t=7.49
    `-- P1 v=60.19 w=113 t=8.04
        |-- P2 v=54.08 w=113 t=7.53
        |   |-- P3 v=51.80 w=128 t=4.04


T12 : Ran PID 6 for 4.35 ms, Remaining: 3.14 ms, vruntime: 68.49

Current Task Tree:
`-- P5 v=43.26 w=170 t=12.14
    |-- P4 v=32.53 w=93 t=13.45
    `-- P1 v=60.19 w=113 t=8.04
        |-- P2 v=54.08 w=113 t=7.53
        |   |-- P3 v=51.80 w=128 t=4.04
        `-- P6 v=68.49 w=113 t=3.14


T13 : Ran PID 4 for 3.11 ms, Remaining: 10.35 ms, vruntime: 66.75

Current Task Tree:
`-- P5 v=43.26 w=170 t=12.14
    `-- P1 v=60.19 w=113 t=8.04
        |-- P2 v=54.08 w=113 t=7.53
        |   |-- P3 v=51.80 w=128 t=4.04
        `-- P6 v=68.49 w=113 t=3.14
            |-- P4 v=66.75 w=93 t=10.35


T14 : Ran PID 5 for 1.86 ms, Remaining: 10.28 ms, vruntime: 54.45

Current Task Tree:
`-- P1 v=60.19 w=113 t=8.04
    |-- P2 v=54.08 w=113 t=7.53
    |   |-- P3 v=51.80 w=128 t=4.04
    |   `-- P5 v=54.45 w=170 t=10.28
    `-- P6 v=68.49 w=113 t=3.14
        |-- P4 v=66.75 w=93 t=10.35


T15 : Ran PID 3 for 1.48 ms, Remaining: 2.56 ms, vruntime: 63.62

Current Task Tree:
`-- P1 v=60.19 w=113 t=8.04
    |-- P2 v=54.08 w=113 t=7.53
    |   `-- P5 v=54.45 w=170 t=10.28
    `-- P4 v=66.75 w=93 t=10.35
        |-- P3 v=63.62 w=128 t=2.56
        `-- P6 v=68.49 w=113 t=3.14


T16 : Ran PID 2 for 3.54 ms, Remaining: 3.99 ms, vruntime: 86.20

Current Task Tree:
`-- P1 v=60.19 w=113 t=8.04
    |-- P5 v=54.45 w=170 t=10.28
    `-- P6 v=68.49 w=113 t=3.14
        |-- P4 v=66.75 w=93 t=10.35
        |   |-- P3 v=63.62 w=128 t=2.56
        `-- P2 v=86.20 w=113 t=3.99


T17 : Ran PID 5 for 4.99 ms, Remaining: 5.29 ms, vruntime: 84.53

Current Task Tree:
`-- P1 v=60.19 w=113 t=8.04
    `-- P6 v=68.49 w=113 t=3.14
        |-- P4 v=66.75 w=93 t=10.35
        |   |-- P3 v=63.62 w=128 t=2.56
        `-- P2 v=86.20 w=113 t=3.99
            |-- P5 v=84.53 w=170 t=5.29


T18 : Ran PID 1 for 1.68 ms, Remaining: 6.36 ms, vruntime: 75.39

Current Task Tree:
`-- P6 v=68.49 w=113 t=3.14
    |-- P4 v=66.75 w=93 t=10.35
    |   |-- P3 v=63.62 w=128 t=2.56
    `-- P2 v=86.20 w=113 t=3.99
        |-- P5 v=84.53 w=170 t=5.29
        |   |-- P1 v=75.39 w=113 t=6.36


T19 : Ran PID 3 for 2.56 ms, Remaining: 0.00 ms, vruntime: 84.13

Current Task Tree:
`-- P6 v=68.49 w=113 t=3.14
    |-- P4 v=66.75 w=93 t=10.35
    `-- P2 v=86.20 w=113 t=3.99
        |-- P5 v=84.53 w=170 t=5.29
        |   |-- P1 v=75.39 w=113 t=6.36


T20 : Ran PID 4 for 3.59 ms, Remaining: 6.75 ms, vruntime: 106.31

Current Task Tree:
`-- P6 v=68.49 w=113 t=3.14
    `-- P2 v=86.20 w=113 t=3.99
        |-- P5 v=84.53 w=170 t=5.29
        |   |-- P1 v=75.39 w=113 t=6.36
        `-- P4 v=106.31 w=93 t=6.75


T21 : Ran PID 6 for 1.37 ms, Remaining: 1.77 ms, vruntime: 80.92

Current Task Tree:
`-- P2 v=86.20 w=113 t=3.99
    |-- P5 v=84.53 w=170 t=5.29
    |   |-- P1 v=75.39 w=113 t=6.36
    |   |   `-- P6 v=80.92 w=113 t=1.77
    `-- P4 v=106.31 w=93 t=6.75


T22 : Ran PID 1 for 3.03 ms, Remaining: 3.33 ms, vruntime: 102.83

Current Task Tree:
`-- P1 v=102.83 w=113 t=3.33
    |-- P2 v=86.20 w=113 t=3.99
    |   |-- P5 v=84.53 w=170 t=5.29
    |   |   |-- P6 v=80.92 w=113 t=1.77
    `-- P4 v=106.31 w=93 t=6.75


T23 : Ran PID 6 for 1.77 ms, Remaining: 0.00 ms, vruntime: 96.98

Current Task Tree:
`-- P1 v=102.83 w=113 t=3.33
    |-- P2 v=86.20 w=113 t=3.99
    |   |-- P5 v=84.53 w=170 t=5.29
    `-- P4 v=106.31 w=93 t=6.75


T24 : Ran PID 5 for 3.42 ms, Remaining: 1.87 ms, vruntime: 105.11

Current Task Tree:
`-- P1 v=102.83 w=113 t=3.33
    |-- P2 v=86.20 w=113 t=3.99
    `-- P4 v=106.31 w=93 t=6.75
        |-- P5 v=105.11 w=170 t=1.87


T25 : Ran PID 2 for 2.04 ms, Remaining: 1.95 ms, vruntime: 104.66

Current Task Tree:
`-- P1 v=102.83 w=113 t=3.33
    `-- P4 v=106.31 w=93 t=6.75
        |-- P5 v=105.11 w=170 t=1.87
        |   |-- P2 v=104.66 w=113 t=1.95


T26 : Ran PID 1 for 3.33 ms, Remaining: 0.00 ms, vruntime: 133.02

Current Task Tree:
`-- P4 v=106.31 w=93 t=6.75
    |-- P5 v=105.11 w=170 t=1.87
    |   |-- P2 v=104.66 w=113 t=1.95


T27 : Ran PID 2 for 1.95 ms, Remaining: 0.00 ms, vruntime: 122.35

Current Task Tree:
`-- P4 v=106.31 w=93 t=6.75
    |-- P5 v=105.11 w=170 t=1.87


T28 : Ran PID 5 for 1.36 ms, Remaining: 0.51 ms, vruntime: 113.33

Current Task Tree:
`-- P4 v=106.31 w=93 t=6.75
    `-- P5 v=113.33 w=170 t=0.51


T29 : Ran PID 4 for 1.11 ms, Remaining: 5.64 ms, vruntime: 118.52

Current Task Tree:
`-- P5 v=113.33 w=170 t=0.51
    `-- P4 v=118.52 w=93 t=5.64


T30 : Ran PID 5 for 0.51 ms, Remaining: 0.00 ms, vruntime: 116.38

Current Task Tree:
`-- P4 v=118.52 w=93 t=5.64


T31 : Ran PID 4 for 1.43 ms, Remaining: 4.21 ms, vruntime: 134.30

Current Task Tree:
`-- P4 v=134.30 w=93 t=4.21


T32 : Ran PID 4 for 1.92 ms, Remaining: 2.29 ms, vruntime: 155.42

Current Task Tree:
`-- P4 v=155.42 w=93 t=2.29


T33 : Ran PID 4 for 2.29 ms, Remaining: 0.00 ms, vruntime: 180.67

Current Task Tree:


--- All Tasks Completed ---

Process finished with exit code 0

"""
