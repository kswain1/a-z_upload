import flask
import dash
import base64
import dash_html_components as html
import pandas as pd
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
            data = html.H3(filename, " Uploaded Succesfully")

            # requests.post(url=url, payload=)
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


class HomerTechniqueCSVReader:
    # parsing the csv files for homertechnique
    # params of interest
    def __init__(self):
        self.tib_anterior_lle = [] 
        self.tib_anterior_rle = []
        self.peroneals_rle = []
        self.peroneals_lle = []
        self.med_gastro_rle = []
        self.med_gastro_lle = []
        self.lat_gastro_rle = []
        self.lat_gastro_lle = []

    def read_csv(filename):
        # content_type, content_string = contents.split(',') #splits the content type from the content code
        # df = None
        # decoded_value = base64.b64decode(content_string)
        try:
            df = pd.read_csv(filename)
        except Exception as e:
            print(e)
            return 'There was an error processing your file %s' % e

        # gets to data row
        emg_data = df[9:]

        # removes unwanted columns
        emg_data = emg_data.drop(columns=['Subject info', 'Project 1'])
        emg_data = emg_data.drop(emg_data.columns[-1], axis=1)

        # setting columns labels
        right_leg = ['time','tib_anterior_rle','peroneals_rle','med_gastro_rle','lat_gastro_rle']
        left_leg = ['time','tib_anterior_lle','peroneals_lle','med_gastro_lle','lat_gastro_lle']

        if 'LT' in emg_data.iloc[0][2]:
            emg_data = emg_data.set_axis(left_leg,axis='columns', inplace=False)
        else:
            emg_data = emg_data.set_axis(right_leg,axis='columns', inplace=False)

        emg_data = emg_data.reset_index(drop=True)

        return emg_data

    def neuro_sum(emg_data):
        # functinos is for converting nureomuscular averages based on the three different angles
        """The three different areas bad > 66, 66 > ok > 33 good > 33"""
        #use a counter for each metric, then divide the counter by a 100
        payload_left = dict(tib_anterior_lle=[],peroneals_lle=[],med_gastro_lle=[],lat_gastro_lle=[])
        payload_right = dict(tib_anterior_rle=[],peroneals_rle=[],med_gastro_rle=[],lat_gastro_rle=[])
        # do it for one row, then create an iteration to go through all of the columns in the data frame
        s = emg_data
        s = s.fillna(value=0)
        duration_sum_index = s[s['time'] == 'Sum of Duration, %'].index
        duration_sum_index = duration_sum_index[0]
        sum = s[duration_sum_index: duration_sum_index+3]

        #drop the time columns
        sum = sum.drop(columns=['time',])
        if 'lle' in sum._info_axis._values[1]:
            for i in payload_left:
                payload_left[i] = list(sum[i])
            return payload_left
        else:
            for i in payload_right:
                payload_right[i] = list(sum[i])
            return payload_right
        payload = payload_left
        payload.update(payload_right)

        return payload


#Test examples
#s = HomerTechniqueCSVReader
#k = s.read_csv(file='kehlin_athlete.csv')
#k = s.neuro_sum(k)



