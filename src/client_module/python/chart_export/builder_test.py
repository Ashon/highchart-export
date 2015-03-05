# test
from builders import HighchartJsonBuilder
from builders import HighchartJsonBuilderException

# test code
try:
    test_super_builder = HighchartJsonBuilder('chart_template/test_template.json')
except HighchartJsonBuilderException as exception:
    exception.print_trace()
try:
    test_super_builder.build(hello='world')
except HighchartJsonBuilderException as exception:
    exception.print_trace()
# get result value
try:
    test_super_builder.get_compiled_chart_json()
except HighchartJsonBuilderException as exception:
    exception.print_trace()

# test child class
class TestBuilder(HighchartJsonBuilder):
    def build_chart(self, **kwargs):
        dictionary = self.get_chart_template()
        dictionary['series'] = kwargs.get('niceto')
        return dictionary

test_extended_builder = TestBuilder('chart_template/test_template.json')
try:
    test_extended_builder.build(niceto='meetyou')
    result = test_extended_builder.get_compiled_chart_json()
    print result
except HighchartJsonBuilderException as exception:
    exception.print_trace()
