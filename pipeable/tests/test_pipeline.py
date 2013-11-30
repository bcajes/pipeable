import unittest


def get_sample_context():
    class SampleTestContext(object):
        count = 0
    return SampleTestContext()


class TestPipeline(unittest.TestCase):
    
    def _getTargetClass(self):
        from pipeable.components import Pipeline
        return Pipeline

    def _makeOne(self, pipes, ctx=None):
        return self._getTargetClass()(pipes, ctx)
    
    def test_class_conforms_to_IPipeline(self):
        from zope.interface.verify import verifyClass
        from pipeable.interfaces import IPipeline
        verifyClass(IPipeline, self._getTargetClass())

    def test_should_run_simple_pipes_add_one_add_two(self):
        test_pipes = self._getSimpleTestPipes()
        pipe_line = self._makeOne(test_pipes)
        res = pipe_line.run(1).next()
        self.assertEquals(4, res, res)

    def test_should_run_simple_pipes_add_one_add_two_generator_input(self):
        test_pipes = self._getSimpleTestPipes()
        pipe_line = self._makeOne(test_pipes)
        res = list(pipe_line.run((x for x in range(1, 3))))
        self.assertEquals([4,5], res, res)

    def test_should_yield_forward_and_backward(self):
        test_pipes = self._getForwardReverseTitles()
        class step_cnt_ctx(object):
            count = 0
        pipe_line = self._makeOne(test_pipes, step_cnt_ctx())
        res = list(pipe_line.run(['foo', 'bar']))
        self.assertEquals(['Foo', 'Oof', 'Bar', 'Rab'], 
                          res, res)

    def test_should_skip_foo(self):
        from pipeable.exceptions import SkipPipeItem
        class ForwardReverseNoFoo(object):
            def process_item(self, str_item, ctx):
                if str_item == 'foo':
                    raise SkipPipeItem
                yield str_item
                yield str_item[::-1]
        test_pipes = [ForwardReverseNoFoo]
        pipe_line = self._makeOne(test_pipes)
        res = list(pipe_line.run(['foo', 'bar']))
        self.assertEquals(['bar', 'rab'], 
                          res, res)

    def test_should_run_pipe_while_updating_shared_context(self):
        test_pipes = self._getForwardReverseTitles()
        class step_cnt_ctx(object):
            count = 0
        pipe_line = self._makeOne(test_pipes, step_cnt_ctx())
        res = list(pipe_line.run(['foo', 'bar', 'baz']))
        self.assertEquals(['Foo', 'Oof', 'Bar', 'Rab', 'Baz', 'Zab'], 
                          res, res)
        self.assertEquals(pipe_line.context.count, 9, 
                          pipe_line.context.count)

    def _getSimpleTestPipes(self):
        class TestPipe1(object):
            def process_item(self, item, ctx):
                yield item + 1
        class TestPipe2(object):
            def process_item(self, item, ctx):
                yield item + 2
        return [TestPipe1, TestPipe2]

    def _getForwardReverseTitles(self):
        class ForwardReverse(object):
            def process_item(self, str_item, step_cnt_ctx):
                yield str_item
                yield str_item[::-1]
                step_cnt_ctx.count += 1
        class Title(object):
            def process_item(self, str_item, step_cnt_ctx):
                yield str_item.title()
                step_cnt_ctx.count +=1
        return [ForwardReverse, Title]



class TestYamlPipelineConfigurator(unittest.TestCase):
    
    def _getTargetClass(self):
        from pipeable.components import YamlPipelineConfigurator
        return YamlPipelineConfigurator

    def test_should_create_pipeline_given_config_and_context(self):
        try:
            from io import StringIO
        except ImportError:
            from StringIO import StringIO
        config = StringIO(unicode(self._sample_yaml_config_contents))
        ctx = get_sample_context()
        yaml_configurator = self._getTargetClass()
        pipeline = yaml_configurator.createPipeline(config, ctx)
        res = list(pipeline.run(1))
        self.assertEquals(len(pipeline.pipes), 2)
        self.assertEquals(pipeline.context.count, 0)
        self.assertEquals(res, [4])


    _sample_yaml_config_contents = """
    pipes:
       - pipeable.tests.sample_pipes.TestPipe1
       - pipeable.tests.sample_pipes.TestPipe2
    """

    
