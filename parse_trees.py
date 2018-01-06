#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

from operator import add
import itertools


class TreeNode:
    def __init__(self, body, children=[]):
        '''Initialize a tree with body and children'''
        self.body = body
        self.children = children

    def __len__(self):
        '''A length of a tree is its leaves count'''
        if self.is_leaf():
            return 1
        else:
            return reduce(add, [len(child) for child in self.children])

    def __repr__(self):
        '''Returns string representation of a tree in bracket notation'''
        st = "[.{0}".format(self.body)
        if not self.is_leaf():
            st += ' '.join([str(child) for child in self.children])
        st += ']'
        return st

    def is_leaf(self):
        '''A leaf is a childless node'''
        return len(self.children) == 0


class ParseTrees:
    def __init__(self, parser):
        '''Initialize a syntax tree parsing process'''
        self.parser = parser
        self.charts = parser.charts
        self.length = len(parser)

        self.nodes = []
        for root in parser.complete_parses:
            self.nodes.extend(self.build_nodes(root))

    def __len__(self):
        '''Trees count'''
        return len(self.nodes)

    def __repr__(self):
        '''String representation of a list of trees with indexes'''
        return '<Parse Trees>\n{0}</Parse Trees>' \
            .format('\n'.join("Parse tree #{0}:\n{1}\n\n" \
                              .format(i + 1, str(self.nodes[i]))
                              for i in range(len(self))))

    '''
    Thuật toán
    Item: S -> NP VP PP. , i
    B1: Xây dựng cây có root = PP
    B2: Duyệt các item previous để xây dựng lần lượt các cây VP, NP
    B3: Tạo cây có root=S, children=[NP, VP, PP]
    Hàm trả về 1 list các Tree vì có thể có nhiều cây suy dẫn
    '''
    def build_nodes(self, root):
        #B1(forest = list of trees)

        #tạo nút lá
        if root.completings == []:
            forest = [TreeNode(root.prev_category())]
        #lần ngược về các completing để xây dựng cây
        else:
            forest = []
            for x in root.completings:
                forest.extend(self.build_nodes(x))

        # B2
        l = [forest]
        prev = root.previous
        while prev and prev.dot > 0:
            l[:0] = [self.build_nodes(x) for x in prev.completings]
            prev = prev.previous
        # l = [[list cây có root=NP], [list cây có root=VP], [list cây có root=PP]]

        #B3
        forestResult = []
        for element in itertools.product(*l): #tổ hợp các phần tử từ các list cây trong l
            forestResult.append(TreeNode(root.rule.lhs, list(element))) #xây dựng cây
        return forestResult
