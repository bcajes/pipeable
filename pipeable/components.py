from pipeable.interfaces import IPipeline, IPipe
from pipeable.exceptions import SkipPipeItem
from zope.interface import implements, implementer


class Pipeline(object):

    implements(IPipeline)

    def __init__(self, pipes, context=None):
        """
        """
        #xxx TODO handle list of pipes of now, later handle dict with order numbers, and yaml file constructor params
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
                        


                
