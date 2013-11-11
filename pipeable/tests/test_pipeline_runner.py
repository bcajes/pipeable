import unittest


class TestPipeline(unittest.TestCase):
    
    def _getTargetClass(self):
        from pipeable.components import Pipeline
        return Pipeline

    def _makeOne(self, pipes):
        return self._getTargetClass()(pipes)
    
    def test_class_conforms_to_IPipeline(self):
        from zope.interface.verify import verifyClass
        from pipeable.interfaces import IPipeline
        verifyClass(IPipeline, self._getTargetClass())

    def test_should_run_simple_pipes_add_one_add_two(self):
        test_pipes = self._getSimpleTestPipes()
        pipe_line = self._makeOne(test_pipes)
        res_gen = pipe_line.run([1])
        res = res_gen.next()
        self.assertEquals(4, res, res)

    def test_should_yield_forward_and_backward(self):
        test_pipes = self._getForwardReverseTitles()
        pipe_line = self._makeOne(test_pipes)
        res = pipe_line.run(['foo', 'bar'])
        self.assertEquals(['Foo', 'Oof', 'Bar', 'Rab'], 
                          list(res), list(res))

    def test_should_skip_foo(self):
        from pipeable.exceptions import SkipPipeItem
        class ForwardReverseNoFoo(object):
            def process_item(self, str_item):
                if str_item == 'foo':
                    raise SkipPipeItem
                yield str_item
                yield str_item[::-1]
        test_pipes = [ForwardReverseNoFoo]
        pipe_line = self._makeOne(test_pipes)
        res = pipe_line.run(['foo', 'bar'])
        self.assertEquals(['bar', 'rab'], 
                          list(res), list(res))

    def test_should_raise_invalid_pipe_input_on_non_iterable(self):
        from pipeable.exceptions import InvalidPipeInput
        test_pipes = self._getForwardReverseTitles()
        pipe_line = self._makeOne(test_pipes)
        self.assertRaises(InvalidPipeInput, pipe_line.run,
                          'bad_input_non_iterable')

    def _getSimpleTestPipes(self):
        class TestPipe1(object):
            def process_item(self, item):
                yield item + 1
        class TestPipe2(object):
            def process_item(self, item):
                yield item + 2
        return [TestPipe1, TestPipe2]

    def _getForwardReverseTitles(self):
        class ForwardReverse(object):
            def process_item(self, str_item):
                yield str_item
                yield str_item[::-1]
        class Title(object):
            def process_item(self, str_item):
                yield str_item.title()
        return [ForwardReverse, Title]


    
        
