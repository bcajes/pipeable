class TestPipe1(object):

    def process_item(self, item, context):
        yield item + 1


class TestPipe2(object):
    
    def process_item(self, item, context):
        yield item + 2
