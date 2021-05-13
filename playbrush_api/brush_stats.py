import pandas as pd
import numpy as np
import warnings

pd.options.mode.chained_assignment = None
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


def preprocess_data(raw_df, groups_df):
    """Steps:
    Clean NaN
    Def time variable
    Sort
    """
    # Clean NaN
    raw_df = raw_df.dropna()
    groups_df = groups_df.dropna()

    # Def time variable
    raw_df['TimestampUTC'] = pd.to_datetime(raw_df['TimestampUTC'])

    # POSSIBLE EXCEPTION: disorder
    return raw_df.sort_values(by=['PlaybrushID', 'TimestampUTC']), groups_df.sort_values(by=['group', 'PBID'])


def week_stats(raw_csv, groups_csv):
    """
    Provides two CSV files with user and group week statistic data
    :param raw_csv:
    :param groups_csv:
    :return:
    """
    # Task 1 - User Information
    # OUT: group, PBID, mon, tue, wed, thu, fri, sat, sun, total-brushes, twice-brushes, avg-brush-time

    # Read CSV & convert to DataFrame
    raw_df = pd.read_csv(raw_csv, usecols=range(7))
    groups_df = pd.read_csv(groups_csv)

    raw_df, groups_df = preprocess_data(raw_df, groups_df)

    # Merge brush sessions that are less than 2minutes apart into a single brush session
    threshold_selector_time = (raw_df.TimestampUTC - raw_df.TimestampUTC.shift(1)) > pd.Timedelta(seconds=120)
    threshold_selector_user = raw_df.PlaybrushID != raw_df.PlaybrushID.shift(1)
    groups_time = threshold_selector_time.cumsum()
    groups_user = threshold_selector_user.cumsum()
    raw_df = raw_df.groupby([groups_time, groups_user]).agg({'PlaybrushID': min, 'TimestampUTC': min, 'UpTime': sum,
                                                             'DownTime': sum, 'LeftTime': sum, 'RightTime': sum,
                                                             'NoneTime': sum})

    # Sum all movements times
    raw_df['brush_time'] = raw_df[['UpTime', 'DownTime', 'LeftTime', 'RightTime', 'NoneTime']].sum(axis=1)\
        .drop(columns=['UpTime', 'DownTime', 'LeftTime', 'RightTime', 'NoneTime'])

    # Discard brush sessions that are less than 20 seconds in total
    raw_df = raw_df[raw_df['brush_time'] >= 20.0]

    # When a user brushes multiple times in a morning or an evening, record the longest brush and discard
    # the others. 2pm is a morning brush while every brush after 2pm is an evening brush.

    # New column for morning (True) and afternoon (False) brushes
    raw_df['morning'] = raw_df['TimestampUTC'].dt.hour <= 14

    # New column from weekday & drop TimestampUTC
    raw_df['weekday'] = raw_df['TimestampUTC'].dt.day_name().drop(columns=['TimestampUTC'])

    # Group by user, weekday, morning/afternoon
    threshold_selector_user = raw_df.PlaybrushID != raw_df.PlaybrushID.shift(1)
    threshold_selector_weekday = raw_df.weekday != raw_df.weekday.shift(1)
    threshold_selector_morning = raw_df.morning != raw_df.morning.shift(1)
    groups_user = threshold_selector_user.cumsum()
    groups_weekday = threshold_selector_weekday.cumsum()
    groups_morning = threshold_selector_morning.cumsum()
    raw_df = raw_df.groupby([groups_user, groups_weekday, groups_morning]).\
        agg({'PlaybrushID': min, 'brush_time': max, 'morning': min, 'weekday': min}).reset_index(drop=True)

    # Add groups
    raw_df = pd.merge(raw_df, groups_df, how='left', left_on='PlaybrushID', right_on='PBID').drop(columns=['PBID'])

    # Split brushes per weekday
    raw_df = raw_df.groupby(['group', 'PlaybrushID', 'weekday']).agg(['mean', 'count']).drop(columns=['morning'])
    raw_df.reset_index(inplace=True)
    raw_df['avg-brush-time'] = raw_df.brush_time['mean']
    raw_df['count'] = raw_df.brush_time['count']
    raw_df = raw_df.drop(columns=['brush_time'])

    raw_df = raw_df.pivot(index=['group', 'PlaybrushID', 'avg-brush-time'], columns="weekday", values='count')

    raw_df.reset_index(inplace=True)
    raw_df = raw_df.groupby(['group', 'PlaybrushID']).agg({'avg-brush-time': np.mean, 'Monday': sum, 'Tuesday': sum,
                                                           'Wednesday': sum, 'Thursday': sum, 'Friday': sum,
                                                           'Saturday': sum, 'Sunday': sum})

    # total-brushes
    raw_df['total-brushes'] = raw_df[['Monday',  'Tuesday',  'Wednesday',  'Thursday',  'Friday',  'Saturday',
                                      'Sunday']].sum(axis=1)

    # twice-brushes
    raw_df['twice-brushes'] = raw_df[raw_df == 2.0].count(axis=1)

    # reorder and format
    cols = raw_df.columns.tolist()[1:] + raw_df.columns.tolist()[:1]
    raw_df = raw_df[cols]
    raw_df = raw_df.rename(columns={"Monday": "mon", "Tuesday": "tue", "Wednesday": "wed", "Thursday": "thu",
                                    "Friday": "fri", "Saturday": "sat", 'Sunday': 'sun'})
    raw_df.index.names = ['group', 'PBID']
    raw_df = raw_df.astype({'mon': int,  'tue': int,  'wed': int,  'thu': int,  'fri': int,  'sat': int,  'sun': int,
                            'total-brushes': int})

    # Task 2 - Group Dynamics
    # OUT: group, total-brushes, avg-brushes, avg-brush-time, score-performance
    group_dynamic_df = raw_df.copy()
    group_dynamic_df.reset_index(inplace=True)

    group_dynamic_df = group_dynamic_df.drop(columns=['PBID',  'mon',  'tue',  'wed',  'thu',  'fri',  'sat',  'sun',
                                                      'twice-brushes'], axis=1)

    group_dynamic_df['avg-brushes'] = group_dynamic_df['total-brushes']

    group_dynamic_df = group_dynamic_df.groupby(['group']).agg({'total-brushes': sum, 'avg-brush-time': np.mean,
                                                                'avg-brushes': np.mean})

    # score-performance is the result of average brush time vs average brushes
    group_dynamic_df['score-performance'] = group_dynamic_df['avg-brush-time'] * group_dynamic_df['avg-brushes']

    group_dynamic_df = group_dynamic_df.sort_values(by=['score-performance'], ascending=False)

    return raw_df.to_csv(float_format='%.2f'), group_dynamic_df.to_csv(float_format='%.2f')
