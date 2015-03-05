''' builders/__init__.py

    @authon
        ashon

    @date
        2014-08-26 ~
'''
import json
import traceback

class HighchartJsonBuilderException(Exception):
    '''
    HighchartJsonBuilderException
    '''
    def __init__(self, code, msg=''):
        super(HighchartJsonBuilderException, self).__init__(code)
        self.exception_table = {
            # builder initialize exception
            0: 'Chart json template is needed.',
            1: 'Exception occurred while loading json template.',

            # chart compile exception
            10: 'Chart is not compiled.',

            # build exception
            100: 'Build Exception.',
            101: 'build_chart() must have return value.',
            102: 'build_chart() must return <dict> value.',

            # builder factory exception
            1000: 'Factory has no matched builder.',
            1001: 'Factory has no selected builder.',
            1010: 'Factory preprocess exception.',
        }
        self.code = code
        self.msg = self.exception_table.get(self.code, 'Unknown Error.') + ' (%s)' % str(msg)
        self.trace = traceback.format_exc()
    def __str__(self):
        return repr(self.code)

    def print_trace(self):
        print "HighchartJsonBuilderException: [code %(code)s] %(message)s\n%(trace)s" % {
            'code': self.code,
            'message': self.msg,
            'trace': self.trace
        }

class HighchartJsonBuilder(object):
    ''' HighchartJsonBuilder

        @description
            Generate highchart settings jsonString.
    '''

    def __init__(self, highchart_template_path=None):
        ''' HighchartJsonBuilder()
            @constructor

            @description
                Initialize highchart global settings.
        '''
        if highchart_template_path is not None:
            self.__chart_constructor = 'StockChart'
            self.__template_path = highchart_template_path
            try:
                self.__template_json = json.load(open(self.__template_path, 'r'))
            except (OSError, IOError):
                raise HighchartJsonBuilderException(1, self.__template_path)
            self.__compiled_chart_option = None
        else:
            raise HighchartJsonBuilderException(0)

    def get_json_path(self):
        return self.__template_path

    def get_compiled_chart(self):
        return self.__compiled_chart_option

    def get_chart_template(self):
        return self.__template_json

    def get_compiled_chart_json(self):
        '''
            get_compiled_chart_json
            @returns
                <string> : highchart setting json
        '''
        if self.__compiled_chart_option is not None:
            json_string = json.dumps(self.__compiled_chart_option)
            json_string = json_string.replace('"', "'")
            return json_string
        else:
            raise HighchartJsonBuilderException(10)

    def set_export_constr(self, string):
        self.__chart_constructor = string

    def get_export_constr(self):
        return self.__chart_constructor

    def __flush_option(self):
        self.__compiled_chart_option = None

    def build_chart(self, **kwargs):
        ''' build_chart()
            @interface
        '''
        pass

    def build(self, **kwargs):
        ''' build()
            @final

            @exception
                <BuildSeriesException>
        '''
        self.__flush_option()
        try:
            self.__compiled_chart_option = self.build_chart(**kwargs)
            if self.__compiled_chart_option is None:
                raise HighchartJsonBuilderException(101)
            else:
                if type(self.__compiled_chart_option) is not dict:
                    raise HighchartJsonBuilderException(102)
        except HighchartJsonBuilderException as builder_exception:
            raise HighchartJsonBuilderException(builder_exception.code)

class HighchartBuilderFactory(object):
    ''' HighchartBuilderFactory

        @description
            Factory of HighchartJsonBuilder
    '''
    def __init__(self, **kwargs):
        # init default variables
        self.__chart_builder_dict = {}
        self.__chart_builder = None
        self.__chart_key = ''
        self.__optional_params = kwargs
    def add_builder(self, string, json_builder):
        if isinstance(json_builder, HighchartJsonBuilder):
            self.__chart_builder_dict[string] = json_builder

    def get_builder(self, builder_key):
        chart_builder = self.__chart_builder_dict.get(builder_key, None)
        if chart_builder is None:
            raise HighchartJsonBuilderException(1000)
        return chart_builder

    def get_builder_dict(self):
        return self.__chart_builder_dict

    def select_builder(self, key):
        ''' select_builder(key)

            @description
                select chart builder matched with key.
                if not matched, then raise exception.

            @params
                key <string> - builder key.

            @exception
                <FactoryHasNoMatchedBuilderException>
        '''
        self.__chart_builder = self.get_builder(key)
        self.__chart_key = key

    def get_selected_chart_key(self):
        return self.__chart_key

    def get_selected_builder(self):
        ''' get_selected_builder()

            @description
                Returns selected builder.
                if selected builder is null, then raise exception.

            @returns
                <HighchartJsonBuilder> - selected builder

            @exception
                <FactoryHasNoSelectedBuilderException>
        '''
        if self.__chart_builder is None:
            raise HighchartJsonBuilderException(1001, self.__chart_key)
        else:
            return self.__chart_builder

    def preprocess(self):
        ''' preprocess()

            @abstract

            @description
                before build chartOption
        '''
        pass

    def build(self):
        ''' build()

            @final

            @exception
                <FactoryHasNoSelectedBuilderException>
                <PreprocessException>
                <BuildSeriesException>
        '''
        selcted_builder = self.get_selected_builder()
        try:
            self.preprocess()
        except Exception:
            raise HighchartJsonBuilderException(1010)
        selcted_builder.build()

    def get_compiled_chart_json(self):
        ''' get_json_string()

            @facade of
                HighchartJsonBuilder

            @exception
                <FactoryHasNoSelectedBuilderException>
        '''
        return self.get_selected_builder().get_compiled_chart_json()

    def get_export_constr(self):
        ''' get_export_constr()

            @facade of
                HighchartJsonBuilder

            @exception
                <FactoryHasNoSelectedBuilderException>
        '''
        return self.get_selected_builder().get_export_constr()
