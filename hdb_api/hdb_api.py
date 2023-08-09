# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 06:22:56 2019

@author: buriona
"""

import sys
from datetime import datetime as dt
from datetime import date
from datetime import timedelta
from dateutil.parser import parse
from requests import get
from requests.exceptions import HTTPError, ConnectionError, ChunkedEncodingError
from urllib3.exceptions import NewConnectionError, MaxRetryError
from socket import gaierror
import pandas as pd
if int(pd.__version__.split('.')[0]) > 0:  
    from pandas import json_normalize
else:
    from pandas.io.json import json_normalize

EMAIL = 'buriona@usbr.gov'
UC_HOST = 'http://ibr4ucrap020.bor.doi.net/'
LC_HOST = 'http://IBRMAZWB011.bor.doi.net/'
HdbConnectionErrors = (
    ConnectionError, NewConnectionError, MaxRetryError, gaierror, ChunkedEncodingError
)

class HdbApiError(Exception):
        
    def __init__(self, err_type=None, err_msg=None, status_code=None, 
                 *args, **kwargs):
        if err_msg:
            self.message = err_msg
        self.__dict__.update(kwargs)
        self.type = err_type
        self.code = status_code
        
    def __str__(self):
        if self.message:
            if self.code:
                return f'HdbApiError, {self.type}\n{self.code}\n{self.message}'
            else:
                return f'HdbApiError, {self.type}\n{self.message}'
        else:
            return 'HdbApiError for unknown reasons! Spooky! Contact: {EMAIL}'

class Hdb:

    def __init__(self, config, **kwargs):
        self.db = config['database']
        self.user = config['username']
        self.psswrd = config['psswrd']
        self.headers = {
            'Accept': 'application/json',
            'api_hdb': self.db,
            'api_user': self.user,
            'api_pass': self.psswrd
        }
        
        self.host = UC_HOST
        self.failover_host = LC_HOST
        if self.db in ['lchdb', 'yaohdb']:
            self.host = LC_HOST
            self.failover_host = UC_HOST
            
    def call_api(self, endpoint, failover=False):
        get_url = f'{self.host}{endpoint}'
        if failover:
            get_url = f'{self.failover_host}{endpoint}'
        get_url_len = len(get_url)
        if get_url_len > 2083:
            raise HdbApiError(
                err_type='GetMethodLengthExceeded', 
                err_msg=f'GET url length ({get_url_len}) exceeds max of 2083'
            )
        try:
            response = get(
                url=get_url,
                headers=self.headers
            )
            response.raise_for_status()
        except HdbConnectionErrors as err:
            if not failover:
                # print('Failed connection attempt, trying failover...')
                response = self.call_api(endpoint, failover=True)
            else:
                raise HdbApiError(
                    err_type='ConnectionError', err_msg=err
                )
        except HTTPError:
            raise HdbApiError(
                err_type='StatusCodeError', 
                status_code=response.status_code, 
                err_msg=response.json().get('message', response.text)
            )
        else:
            return response.json()
        
    def suffix_gen(self, param, items, **kwargs):
        if not param or not items:
            return None
        if isinstance(items, list):
            return f"{'&'.join([f'{param}={i}' for i in items])}"
        return f'{param}={items}'

    def combine_suffixes(self, method, suffixes, **kwargs):
        return f"{method}?{'&'.join([i for i in suffixes if i])}"
    
    def error_check(self, response):
        if response.status_code == 200:
            return None
        
class HdbConnect(Hdb):

    def hdb(self):
        suffix = 'hdb'
        return_json = self.call_api(suffix)

        return return_json

    def connect(self):

        suffixes = []
        suffixes.append(self.suffix_gen('hdb', self.db))
        suffixes.append(self.suffix_gen('username', self.user))
        suffixes.append(self.suffix_gen('password', self.psswrd))
        suffix = self.combine_suffixes('connect', suffixes)

        return_json = self.call_api(suffix)

        return return_json


class HdbTables(Hdb):

    def datatypes(self, datatype_list=None, output='df', **kwargs):

        def to_df(data):
            df = pd.DataFrame(data)
            df.set_index('datatype_id', inplace=True, drop=False)

            return df

        suffixes = []
        suffixes.append(self.suffix_gen('id', datatype_list))
        suffix = self.combine_suffixes('datatypes', suffixes)
        return_json = self.call_api(suffix)

        if output == 'df' and return_json:
            return to_df(return_json)
        return return_json

    def modelruns(self, idtype=None, id_list=None, name=None,
                  output='df', **kwargs):

        def to_df(data):
            df = pd.DataFrame(data)
            df.set_index('model_run_id', inplace=True, drop=False)
            df['date_time_loaded'] = pd.to_datetime(
                df['date_time_loaded'],
                errors='coerce'
            )

            df['run_date'] = pd.to_datetime(df['run_date'], errors='coerce')

            return df

        valid_idtypes = ['model_run_id', 'model_id']

        if idtype not in valid_idtypes:
            idtype = 'model_run_id'
        suffixes = []
        suffixes.append(self.suffix_gen('idtype', idtype))
        suffixes.append(self.suffix_gen('id', id_list))
        suffixes.append(self.suffix_gen('modelrunname', name))
        suffix = self.combine_suffixes('modelruns', suffixes)

        return_json = self.call_api(suffix)

        if output == 'df' and return_json:
            return to_df(return_json)
        return return_json

    def sitedatatypes(self, sdi_list=None, sid_list=None, did_list=None,
                      output='df', **kwargs):

        def to_df(data):
            df = pd.DataFrame(data)
            metadata_list = df['metadata'].tolist()
            metadata = json_normalize(metadata_list)
            df = df.join([metadata])
            df.drop(['metadata'], axis=1, inplace=True)
            df.set_index('site_datatype_id', inplace=True, drop=False)

            return df

        suffixes = []
        suffixes.append(self.suffix_gen('sdi', sdi_list))
        suffixes.append(self.suffix_gen('sid', sid_list))
        suffixes.append(self.suffix_gen('did', did_list))
        suffix = self.combine_suffixes('sitedatatypes', suffixes)
        return_json = self.call_api(suffix)
        if output == 'df' and return_json:
            return to_df(return_json)
        return return_json

    def sites(self, ids=None, output='df', **kwargs):

        def to_df(data):
            df = pd.DataFrame(data)
            df.set_index('site_id', inplace=True, drop=False)

            return df

        suffixes = []
        suffixes.append(self.suffix_gen('id', ids))
        suffix = self.combine_suffixes('sites', suffixes)
        return_json = self.call_api(suffix)

        if output == 'df' and return_json:
            return to_df(return_json)
        return return_json
    
    def select(self, sql='', output='df', **kwargs):
        
        def to_df(data):
            df = pd.DataFrame(data)

            return df
        
        suffixes = []
        suffixes.append(self.suffix_gen('svr', self.db))
        suffixes.append(self.suffix_gen('sqlStatement', sql))
        suffix = self.combine_suffixes('select', suffixes)
        return_json = self.call_api(suffix)

        if output == 'df' and return_json:
            return to_df(return_json)
        return return_json
    
class HdbTimeSeries(Hdb):

    def series(self, sdi=None, t1='POR', t2='POR', interval='month',
               rbase=False, table='R', mrid=None, instantminutes=None,
               data_only=True, output='df', drop_flags=True, drop_date=False,
               label_overide=None, **kwargs):

        def to_df(data):
            try:
                df = pd.DataFrame(
                    data['data'],
                    dtype=float
                )
            except:
                print(f'Error getting data from - {self.host}/{suffix}', data)
                return pd.DataFrame([],columns=['value', 'datetime'])
            if df.empty:
                return pd.DataFrame([],columns=['value', 'datetime'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True, drop=drop_date)
            df.index = pd.to_datetime(df.index, errors='ignore')
            meta_data = data['metadata']
            datatype_meta = meta_data['datatype_metadata']
            col_name = datatype_meta['datatype_common_name']
            if label_overide:
                col_name = label_overide
            df.rename(columns={'value': col_name}, inplace=True)
            if drop_flags:
                df.drop(['flag'], axis=1, inplace=True)
            if not data_only:
                metadata_list = df['metadata'].tolist()
                metadata = json_normalize(metadata_list)
                df = df.join([metadata])
                df.drop(['metadata'], axis=1, inplace=True)

            return df

        def validate_date(t_date, interval, default_dt):

            def set_year_interval(t_date):
                return date(t_date.year, 1, 1)

            def set_month_interval(t_date):
                return date(t_date.year, t_date.month, 1)

            def set_day_interval(t_date):
                return date(t_date.year, t_date.month, t_date.day)

            def set_hour_interval(t_date):
                return dt(t_date.year, t_date.month, t_date.day, t_date.hour)

            def set_instant_interval(t_date):
                minutes = 0#(t_date.minute//15+1)*15
                return dt(
                    t_date.year, t_date.month, t_date.day, t_date.hour, minutes
                )

            if isinstance(t_date, str):
                #default "POR" string fails parse and reverts to default, ugly...
                try:
                    t_date = parse(t_date)
                except ValueError:
                    t_date = default_dt

            set_interval_date = {
                'year': set_year_interval,
                'month': set_month_interval,
                'day': set_day_interval,
                'hour': set_hour_interval,
                'instant': set_instant_interval
            }
            result_date = set_interval_date[interval](t_date)
            return result_date.strftime('%m-%d-%Y %H:%M')

        begin = dt(1899, 10, 1, 0, 0)
        end = dt.now()
        if mrid:
            end = end + timedelta(days=36525)
        t1 = validate_date(t1, interval, begin)
        t2 = validate_date(t2, interval, end)
        valid_intervals = ['instant', 'hour', 'day', 'month', 'year']
        if interval not in valid_intervals:
            interval = 'month'
        valid_rbases = [True, False]
        if rbase not in valid_rbases:
            rbase = False
        valid_tables = ['R', 'M']
        if table not in valid_tables:
            table = 'R'
        if mrid:
            table = 'M'
        if mrid:
            try:
                mrid = int(mrid)
            except TypeError:
                mrid = None
                table = 'R'
        suffixes = []
        suffixes.append(self.suffix_gen('sdi', sdi))
        suffixes.append(self.suffix_gen('t1', t1))
        suffixes.append(self.suffix_gen('t2', t2))
        suffixes.append(self.suffix_gen('interval', interval))
        suffixes.append(self.suffix_gen('rbase', rbase))
        suffixes.append(self.suffix_gen('table', table))
        suffixes.append(self.suffix_gen('mrid', mrid))
        suffixes.append(self.suffix_gen('instantminutes', instantminutes))
        suffix = self.combine_suffixes('series', suffixes)
        return_json = self.call_api(suffix)

        if output == 'df' and return_json:
            return to_df(return_json)
        if data_only:
            return return_json['data']
        return return_json

if __name__ == '__main__':

    from hdb_utils import get_eng_config
    import sys
    #    Usage examples below:
    #
    #    Keep in mind dictioanries of arguments can be passed to any method
    #    as long as the keys of the dict match the methods named arguments.
    #    All optional args should be defaulted or ignored where needed.
    config = get_eng_config()
    hdb = Hdb(config)

    #    Connections methods:
    meta = HdbConnect
    try:
        dbs = meta.hdb(hdb)
        connect_info = meta.connect(hdb)

        #    Tables methods:
        tables = HdbTables
        datatypes_list = [1393, 1502]
        datatypes_all = tables.datatypes(hdb)
        datatypes = tables.datatypes(hdb, datatypes_list)
        modelruns_all = tables.modelruns(
            hdb,
            idtype='model_id',
            id_list=2
        )

        model_ids = [3085, 3084]
        modelruns_bynumber = tables.modelruns(hdb, id_list=model_ids)
        modelruns_byname = tables.modelruns(hdb, name='Jan', output='json')
        sdi_list = [2101, 150]
        sitedatatypes = tables.sitedatatypes(hdb, sdi_list=sdi_list)
        sites_all = tables.sites(hdb)
        site_ids = [919, 121]
        sites = tables.sites(hdb, ids=site_ids)
    
        #    Series methods:
        #
        #    Need to add POST and DELETE methods too
        ts = HdbTimeSeries
        site_data = ts.series(hdb, sdi=2101, t1='10/1/2010')
        site_data_all_avail = ts.series(hdb, sdi=2101)
        site_data_model = ts.series(hdb, sdi=2101, mrid=3085)
        more_data = ts.series(
            hdb,
            sdi=1856,
            t1='01/01/2018',
            t2='2021-10-1',
            interval='day'
        )
    except HdbApiError as err:
        print(err.message, err.code)
    sys.exit(0)
