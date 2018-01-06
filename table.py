#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

class Item:
    def __init__(self, rule, dot=0, start=0, previous=None, completings=[]):
        '''Initialize a chart row, consisting of a rule, a position
           index inside the rule, index of starting chart and
           pointers to parent rows
        '''
        self.rule = rule #instance of Rule
        self.dot = dot # dot=i => dot nằm trước rhs[] trong rule. S->NP.VP => dot=1
        self.start = start #vị trí bảng sinh ra Item này
        '''
        Example: có các item
            VP -> vt. , i (Item a)
            VP -> vi NP. , (Item b)
            S -> NP VP. , i (Item c)
            item a, b complete làm cho item c complete
            => c.completings = [a, b]
        '''
        self.completings = completings
        '''
        Item a: VP -> . vt, i
        Item b: VP -> vt . , i
        => b.previous = a (có a.dot = b.dot-1
        '''
        self.previous = previous

    def __len__(self):
        '''A chart's length is its rule's length'''
        return len(self.rule)

    def __repr__(self):
        '''Nice string representation:
            <Row <LHS -> RHS .> [start]>'''
        rhs = list(self.rule.rhs)
        rhs.insert(self.dot, '.')
        rule_str = "[{0} -> {1}]".format(self.rule.lhs, ' '.join(rhs))
        return "<Row {0} [{1}]>".format(rule_str, self.start)

    def __cmp__(self, other):
        '''Two rows are equal if they share the same rule, start and dot'''
        if len(self) == len(other):
            if self.dot == other.dot:
                if self.start == other.start:
                    if self.rule == other.rule:
                        return 0
                        #không xét completings
        return 1

    def is_complete(self):
        '''Returns true if rule was completely parsed, i.e. the dot is at the end'''
        return len(self) == self.dot

    def next_category(self):
        '''Return next category to parse, i.e. the one after the dot'''
        if self.dot < len(self):
            return self.rule[self.dot]
        return None

    def prev_category(self):
        '''Returns last parsed category'''
        if self.dot > 0:
            return self.rule[self.dot - 1]
        return None

class Table:
    def __init__(self, rows):
        '''An Earley chart is a list of rows for every input word'''
        self.rows = rows

    def __len__(self):
        '''Chart length'''
        return len(self.rows)

    def __repr__(self):
        '''Nice string representation'''
        st = '<Chart>\n\t'
        st += '\n\t'.join(str(r) for r in self.rows)
        st += '\n</Chart>'
        return st

    def add_row(self, row):
        '''Add a row to chart, only if wasn't already there'''
        # nếu row chưa có, thêm vào
        if not row in self.rows:
            self.rows.append(row)
        #nếu row đã có và completings khác, thêm completing
        else:
            for i in range(len(self.rows)):
                if self.rows[i] == row:
                    self.rows[i].completings.extend([x for x in row.completings if x not in self.rows[i].completings])
                    break