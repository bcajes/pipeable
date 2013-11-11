from zope.interface import Interface, Attribute


class IPipe(Interface):
    """A pipe is responsible for processing a single item
    and yields one or more iterables
    """
    def process_item(item):
        """process single item
        """
        pass

class IPipeline(Interface):
    """ Master pipeline interface
    """
    
    pipe_runners = Attribute('a collection of pipe_runners')
    
    def run(it):
        """begin pipeline execution given iterable
        """
        pass

class IPipelineRunner(Interface):
    """Handles execution of pipe and skip item exceptions
    """
    
    pipe = Attribute('single pipe being wrapped')
    
    def execute(it):
        """execute pipe with given iterable
        """
        pass
