import unittest

class QueueWithTwoStacks(object):
    """
    两个栈实现一个队列
    """

    def __init__(self):
        self._stack1 = []
        self._stack2 = []

    def push(self, x):
        """向队列中添加元素"""
        self._stack1.append(x)

    def pop(self):
        """弹出队列中一个元素"""
        if not self._stack2:
            assert self._stack1, '队列已经空了,请增加元素'
            while self._stack1:
                item = self._stack1.pop()
                self._stack2.append(item)
        return self._stack2.pop()


class StackWithTwoQueues(object):
    """
    两个队列实现一个栈
    """

    def __init__(self):
        self._queue1 = []
        self._queue2 = []

    def push(self, x):
        """push """
        if not self._queue1:
            self._queue1.append(x)
        elif not self._queue2:
            self._queue2.append(x)
        if len(self._queue2) == 1 and len(self._queue1) >= 1:
            while self._queue1:
                self._queue2.append(self._queue1.pop(0))
        elif len(self._queue1) == 1 and len(self._queue2) > 1:
            while self._queue2:
                self._queue1.append(self._queue2.pop(0))

    def pop(self):
        """pop"""
        if self._queue1:
            return self._queue1.pop(0)
        elif self._queue2:
            return self._queue2.pop(0)


class Stack2WithTwoQueue(object):
    """
    优化的两个队列实现栈
    """

    def __init__(self):
        self._queue1 = []
        self._queue2 = []

    def push(self, x):
        pass



