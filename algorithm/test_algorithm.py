from pytest import raises


class TestQueueStackClass(object):

    def test_queue(self):
        from .queue_and_stack import QueueWithTwoStacks
        queue = QueueWithTwoStacks()

        for i in range(10):
            queue.push(i)

        test_ret = []
        for i in range(10):
            test_ret.append(queue.pop())

        assert test_ret == list(range(10)), 'queue is invalid'

    def test_stack(self):
        from .queue_and_stack import StackWithTwoQueues
        stack = StackWithTwoQueues()

        for i in range(10):
            stack.push(i)

        test_ret = []
        for i in range(10):
            test_ret.append(stack.pop())
        assert test_ret == list(reversed(range(10))), 'stack is invalid'





