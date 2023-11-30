import streamlit as st
import os
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots
from dotenv import load_dotenv
import datetime

load_dotenv()

API_BASE_URL = os.environ['API_BASE_URL']
ADMIN_KEY = os.environ['ADMIN_KEY']

def get_user_count(start_date=None, end_date=None):
    headers = {'admin-key': ADMIN_KEY}
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date

    response = requests.get(f'{API_BASE_URL}/stats/users_count', params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['users_count']
    else:
        st.error('Failed to retrieve user count data')

def get_active_users_count(start_date=None, end_date=None, n_calls=1, as_days=False):
    headers = {'admin-key': ADMIN_KEY}
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    if n_calls:
        params['n_calls'] = n_calls
    if as_days:
        params['as_days'] = as_days

    response = requests.get(f'{API_BASE_URL}/stats/active_users_count', params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if as_days:
            active_users = data['active_users_count']
            return active_users
        else:
            return data['active_users_count']
    else:
        st.error('Failed to retrieve active users count data')


def main():
    st.title('Telemetry Dashboard')

    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')

    user_count = get_user_count(start_date=start_date, end_date=end_date)
    st.subheader('User Count')
    st.write(user_count)

    n_calls = st.number_input('Minimum Number of Calls', min_value=1, step=1, value=1)
    as_days = st.checkbox('Show Active Users Count per Day')

    active_users_data = get_active_users_count(start_date=start_date, end_date=end_date, n_calls=n_calls, as_days=as_days)
    st.subheader('Active Users Count')
    if as_days:
        fig = go.Figure(data=go.Scatter(x=active_users_data['days'], y=active_users_data['active_users'], mode='lines'))
        st.plotly_chart(fig)
    else:
        st.write(active_users_data)


if __name__ == '__main__':
    main()