from pipeable.interfaces import IPipeline, IPipe, IPipelineRunner
from pipeable.exceptions import InvalidPipeInput, SkipPipeItem
from zope.interface import implements, implementer
import collections


class Pipeline(object):
    implements(IPipeline)

    def __init__(self, pipes):
        """
        """
        #xxx TODO handle list of pipes of now, later handle dict with order numbers, and yaml file constructor params
        self.pipe_runners = []
        for pipe in pipes:
            pipe_runner = PipeRunner(implementer(IPipe)(pipe()))
            self.pipe_runners.append(pipe_runner)

    def run(self, it):
        if not hasattr(it, '__iter__'):
            raise InvalidPipeInput("Pipeline requires iterable input, got: " + it)
        res = it
        for pipe_runner in self.pipe_runners:
            res = pipe_runner.execute(res)
        return res

class PipeRunner(object):
    implements(IPipelineRunner)

    def __init__(self, pipe):
        self.pipe = pipe

    def execute(self, item_gen):            
        for item in item_gen:
            try:
                for res in self.pipe.process_item(item):
                    #process_items can produce multiple yields
                    yield res
            except SkipPipeItem:
                continue
                
