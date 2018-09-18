import flask
import dash
import base64
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import requests
import io
import datetime

class parser_csv():
    # reusable componenets
    def make_dash_table(df):
        ''' Return a dash definition of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    def parse_contents(contents, filename,dates):
        content_type, content_string = contents.split(',')
        df = None

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
            print("successful got df", df.head())
            print("df tail", df.tail())
            data = html.H3("File Uploaded Succesfully")
            return data
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])


        return html.Div([
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),

            # Use the DataTable prototype component:
            # github.com/plotly/dash-table-experiments
            # dt.DataTable(rows=df.to_dict('records')),
            # self.make_dash_table(df),

            html.Hr(),  # horizontal line

            # For debugging, display the raw contents provided by the web browser
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])