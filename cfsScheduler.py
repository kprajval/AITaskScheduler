import sys
import random

class Node:
    def __init__(self, PID, niceValue=0, vruntime=0, dealtExec=0):
        self.color = 1
        self.PID = PID
        self.niceValue = niceValue
        self.weight = 1024 // (1 + niceValue)
        self.vruntime = vruntime
        self.dealtExec = dealtExec
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
            print(indent, "`-- " if last else "|-- ", f"P{node.PID} v={node.vruntime:.2f} w={node.weight}", sep="")
            self.print_tree(node.left, indent + ("    " if last else "|   "), False)
            self.print_tree(node.right, indent + ("    " if last else "|   "), True)

if __name__ == "__main__":
    tree = RedBlackTree()
    for pid in range(1, 7):
        nice = random.randint(0, 10)
        task = Node(PID=pid, niceValue=nice, vruntime=0)
        tree.insert(task)
    print("\nInitial Task Tree:")
    tree.print_tree()
    print("\n--- Starting Scheduling Simulation ---\n")
    for _ in range(10):
        task = tree.delete_min()
        delta_exec = random.uniform(1, 5)
        task.dealtExec += delta_exec
        task.vruntime += delta_exec * (1024 / task.weight)
        print(f"Ran PID {task.PID} for {delta_exec:.2f} ms. New vruntime: {task.vruntime:.2f}")
        tree.insert(task)
        print("\nCurrent Task Tree:")
        tree.print_tree()
        print("\n")
    print("--- Simulation Ended ---")
