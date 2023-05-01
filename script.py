import datetime
import pandas as pd


def get_date_range():
    """
    Get the start and end date from the user and return a list of dates between them.
    """
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')

    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')

    current_date = start_date
    days = []
    while current_date <= end_date:
        days.append(current_date)
        current_date += datetime.timedelta(days=1)

    return days


def read_data(days, blocks):
    """
    Read the data from CSV files for each day and block, and return a concatenated DataFrame.
    """
    day_data = []
    for j in range(len(blocks)):
        for i in range(len(days)):
            day_data.append(pd.read_csv('./data/'+days[i].strftime('%Y-%m-%d') + '_' + str(blocks[j]) + '.csv'))

    return pd.concat(day_data, axis=0)


def get_caterer_counts(df, master_df, caterers):
    """
    Calculate the number of enrolled and present students for each caterer in the given DataFrame,
    and return a dictionary of caterers with their corresponding counts.
    """
    caterer_counts = {caterer: {'enrolled': 0, 'present': 0} for caterer in caterers}

    for regno in df['regno']:
        master_row = master_df.loc[master_df['regno'] == regno]
        if not master_row.empty and df.loc[df['regno'] == regno, 'status'].iloc[0] == 'present':
            caterer = master_row.iloc[0]['caterer']
            if caterer in caterer_counts:
                caterer_counts[caterer]['present'] += 1

    for caterer in caterers:
        caterer_counts[caterer]['enrolled'] = len(master_df[master_df['caterer'] == caterer])

    return caterer_counts


def create_output_df(caterer_counts):
    """
    Create a DataFrame from the given caterer counts dictionary.
    """
    vec1 = list(caterer_counts.keys())
    vec2 = [count['enrolled'] for count in caterer_counts.values()]
    vec3 = [count['present'] / sum(vec2) for count in caterer_counts.values()]

    data = {'caterer': vec1, 'enrolled_st': vec2, 'present_st': vec3}
    return pd.DataFrame(data)


def run_script():
    """
    Run the script to read data, get caterer counts, and create the output DataFrame.
    """
    # Get date range and blocks
    days = get_date_range()
    blocks = ['G', 'H']

    # Read data
    data_df = read_data(days, blocks)
    master_df = pd.read_csv('./data/'+'master.csv')

    # Get caterer counts
    caterers = set(master_df['caterer'])
    caterer_counts = get_caterer_counts(data_df, master_df, caterers)

    # Create output DataFrame
    output_df = create_output_df(caterer_counts)
    print(output_df)


if __name__ == '__main__':
    run_script()
