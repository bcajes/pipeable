from pipeable.interfaces import IPipeline, IPipe, IPipelineConfigurator
from pipeable.exceptions import SkipPipeItem
from zope.interface import implementer
from pipeable.utils import load_object
import yaml


@implementer(IPipeline)
class Pipeline(object):

    def __init__(self, pipes, context=None):
        """
        """
        if not hasattr(pipes, '__iter__'):
            raise ValueError("pipes not an iterable")
        self.pipes = []
        self.context = context
        for pipe in pipes:
            self.pipes.append(implementer(IPipe)(pipe()))

    def run(self, it):
        if not hasattr(it, '__iter__'):
            it = [it]
        res = it
        for pipe in self.pipes:
            res = self._execute_pipe(pipe, res)
        return res

    def _execute_pipe(self, pipe, item_generator):            
        for item in item_generator:
            try:
                for res in pipe.process_item(item, self.context):
                    #process_items can produce multiple yields
                    yield res
            except SkipPipeItem:
                continue


@implementer(IPipelineConfigurator)
class YamlPipelineConfigurator(object):
    """
    Configuration file should contain a section called "pipes"
    that is an ordered list of python paths to pipe classes

    Sample yaml config file:
    
    pipes:
      - mypackage.module1.pipeclass1
      - mypackage.module2.pipeclass2
      - anotherpackage.somemodule.someotherpipe
    """

    @staticmethod
    def createPipeline(config_file, context=None):
        pipe_class_paths = yaml.load(config_file)['pipes']
        pipes = []
        for pipe_class in pipe_class_paths:
            pipe = load_object(pipe_class)
            pipes.append(pipe)
        return Pipeline(pipes, context)
        

