import os
import datetime
import pandas as pd

# Path to the repository.
REPO_PATH = "/Users/eric/Documents/asana_challenge"

# Number of visits within the time period for a user to be considered "adopted".
ADOPTION_NUM_VISITS = 3

# File path with engagement data.
ENGAGEMENT_CSV = 'data/takehome_user_engagement-intern.csv'

# The file path destination for adoption data.
ADOPTION_CSV = 'data/adoption.csv'


def get_previous_week_visits(df, n_days=7):
    """Counts the number of visits for each user in the n days prior to each logged timestamp.
    Args:
        df (pandas.DataFrame): The engagement dataframe.
        n_days (int): Number of days for the window.

    Returns:
        visits (pandas.DataFrame)
    """
    df['previous_week'] = df['date'] - datetime.timedelta(days=n_days)
    df = df[['user_id', 'date', 'previous_week']]

    # Join each user's daily activity to itself.
    days_df = pd.merge(df, df[['user_id', 'date']], how='left', on=['user_id'])
    within_prev_week = (days_df['date_y'] > days_df['previous_week']) & (days_df['date_y'] <= days_df['date_x'])
    days_df = days_df.loc[within_prev_week]

    visits = days_df.groupby(['user_id', 'date_x'], as_index=False).count()
    visits = visits.rename(columns={'date_x': 'date', 'previous_week': 'previous_week_visits'})
    return visits[['user_id', 'date', 'previous_week_visits']]


def clean_engagement_data(engagement):
    engagement['time_stamp'] = pd.to_datetime(engagement['time_stamp'], infer_datetime_format=True)
    engagement['date'] = engagement['time_stamp'].map(lambda row: row.date())
    return engagement


def calculate_adoption(engagement):
    """Return a dataframe with the initial date of adoption for each user."""
    visits = get_previous_week_visits(engagement)
    visits = visits.loc[visits['previous_week_visits'] >= ADOPTION_NUM_VISITS]
    adoption_dates = visits.groupby(['user_id'], as_index=False).first()
    return adoption_dates


def main(verbose=1):
    engagement_csv = os.path.join(REPO_PATH, ENGAGEMENT_CSV)

    if verbose > 0:
        print("Reading engagement data from: {}".format(engagement_csv))

    raw_engagement = pd.read_csv(engagement_csv)
    engagement = clean_engagement_data(raw_engagement)

    if verbose > 0:
        print("Creating adoption dataset...")

    adoption = calculate_adoption(engagement)
    adoption_csv = os.path.join(REPO_PATH, ADOPTION_CSV)
    adoption.to_csv(adoption_csv, index=False)

    if verbose > 0:
        print("Wrote adoption data to: {}".format(adoption_csv))


if __name__ == "__main__":
    main()
