#!/usr/bin/env python
# -*- coding: utf-8 -*-


V = u'\u2502   '                       # [|    ]
C = u'\u251c\u2500\u2500 '
E = u'\u2514\u2500\u2500 '


# print(V)
# print(C)
# print(E)

class Render(object):
    def __init__(self, tree):
        self.tree = tree


    def show(self):
        node = self.tree.root
        self.__iii(node, list())


    def __iii(self, node, continues):

        if node.parent is None:
            pass
        else:
            node_index = node.parent.childrens.index(node)
            
            #--- replace prev
            if len(continues) > 1:
                continues[-2] = V

            #--- if only 1 child - end
            if len(node.parent.childrens) == 1:
                continues[-1] = E

            #--- if last - end
            elif node_index + 1 == len(node.parent.childrens):        # last
                continues[-1] = E                           # end

            #--- if first - continue
            elif node_index == 0 and len(node.parent.childrens)>1:  # first
                continues[-1] = C
            
            #--- continue
            else:
                continues[-1] = C                           # continue


        pre = "".join(continues)
        print(pre + node.name)

        if node.childrens:
            continues.append("---")

        for n in node.childrens:
            self.__iii(n, continues[:])


    



# class AbstractStyle(object):

#     def __init__(self, vertical, cont, end):
#         """
#         Tree Render Style.
#         Args:
#             vertical: Sign for vertical line.
#             cont: Chars for a continued branch.
#             end: Chars for the last branch.
#         """
#         super(AbstractStyle, self).__init__()
#         self.vertical = vertical
#         self.cont = cont
#         self.end = end
#         assert (len(cont) == len(vertical) and len(cont) == len(end)), (
#             "'%s', '%s' and '%s' need to have equal length" % (vertical, cont,
#                                                                end))

#     @property
#     def empty(self):
#         """Empty string as placeholder."""
#         return ' ' * len(self.end)

#     def __repr__(self):
#         classname = self.__class__.__name__
#         return "%s()" % classname



# class ContStyle(AbstractStyle):

#     def __init__(self):
#         u"""
#         Continued style, without gaps.
#         >>> root = Node("root")
#         >>> s0 = Node("sub0", parent=root)
#         >>> s0b = Node("sub0B", parent=s0)
#         >>> s0a = Node("sub0A", parent=s0)
#         >>> s1 = Node("sub1", parent=root)
#         >>> print(RenderTree(root, style=ContStyle()))
#         Node('root')
#         ├── Node('root/sub0')
#         │   ├── Node('root/sub0/sub0B')
#         │   └── Node('root/sub0/sub0A')
#         └── Node('root/sub1')
#         """
#         super(ContStyle, self).__init__(u'\u2502   ',
#                                         u'\u251c\u2500\u2500 ',
#                                         u'\u2514\u2500\u2500 ')
