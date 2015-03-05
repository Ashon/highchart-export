''' __init__.py

    @author
        ashon

    @date
        2014-08-27 ~

    @dependencies
'''

import requests

CHART_RENDERER_HOST = '127.0.0.1:3000'

def get_encoded_image(chart_data, chart_constr):
    ''' getEncodedImage(chart_data, constr)

        @description
            Generate & POST highchart-convert settings to phantomjs export server.
            It returns base64 encoded highchart image string.(for generating MIME Content easier.)

            !! Requires phantomjs webserver (and highchart-convert.js)
              - phantomjs == 1.9.0 (stable)

        @params
            <string> chart_data : highchart jsonString settings
            <string> chart_constr : highchart convert param of argument '-constr' (chart constructor)
                - reference of highchart's '-constr'
                  http://www.highcharts.com/component/content/article/2-articles/news/52-serverside-generated-charts

        @returns
            <string> : base64 encoded chart image (.png)
    '''

    # phantomjs highchart-convert server host
    CHART_RENDERER_HOST = CHART_RENDERER_HOST

    # chart export options
    HIGHCHART_WIDTH = '800'
    HIGHCHART_SCALE = '1'

    # export Settings
    infile = '"infile":"' + chart_data + '"'
    constr = '"constr":"' + chart_constr + '"'
    width = '"width":' + HIGHCHART_WIDTH
    scale = '"scale":' + HIGHCHART_SCALE
    export_json = '{' + ','.join((infile, constr, width, scale)) + '}'

    try:
        response = requests.post(CHART_RENDERER_HOST, data=export_json)
        return response.content
    except Exception as renderer_exception:
        raise renderer_exception

def get_export_server_status():
    try:
        response = requests.get(CHART_RENDERER_HOST)
        return response
    except Exception as renderer_exception:
        raise renderer_exception
