from zope.interface import Interface, Attribute


class IPipe(Interface):
    """A pipe is responsible for processing a single item
    and yields one or more iterables. 
    """

    def process_item(item, context=None):
        """process single item
        - `item`: the item to process
        - `context`: optional shared context
        """
        pass

class IPipeline(Interface):
    """ Pipeline interface
    """

    pipes = Attribute('iterable of pipes')
    context = Attribute('optional shared context (eg. database connection)')

    def run(it):
        """begin pipeline execution given a starting object 'it'
        and optional shared context object that can be accesed by
        each pipe
        """
        pass
