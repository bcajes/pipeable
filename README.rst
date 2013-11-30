************
Pipeable
************

Light-weight, config-driven, data pipeline framework
****************************************************

Example usage
-------------

example_pipeline_config.yaml::

  pipes:
    - example.pipes.ForwardReverse
    - example.pipes.Title

example.pipes::

        class ForwardReverse(object):
            def process_item(self, str_item, step_cnt_ctx):
                yield str_item
                yield str_item[::-1]
                step_cnt_ctx.count += 1
        class Title(object):
            def process_item(self, str_item, step_cnt_ctx):
                yield str_item.title()
                step_cnt_ctx.count +=1

example main::

        from pipeable.components import YamlPipelineConfigurator
  
        class step_cnt_ctx(object):
            #example context object that is shared between pipes
            count = 0
  
        pipe_line = YamlPipelineConfigurator.createPipeline(example_pipeline_config, step_cnt_ctx())
        result = list(pipe_line.run(['foo', 'bar', 'baz']))
        assert ['Foo', 'Oof', 'Bar', 'Rab', 'Baz', 'Zab'] == result
        assert pipe_line.context.count == 9





