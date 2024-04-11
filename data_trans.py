import pandas as pd

df2014 = pd.read_csv('./data/2014.csv')
df2015 = pd.read_csv('./data/2015.csv')
df2016 = pd.read_csv('./data/2016.csv')
df2017 = pd.read_csv('./data/2017.csv')
df2018 = pd.read_csv('./data/2018.csv')
df2019 = pd.read_csv('./data/2019.csv')


def make_my_cols(df):

    new_df = df.groupby(['Reference Number', 'Grid Ref: Easting', 'Grid Ref: Northing', 'Accident Date', 'Time (24hr)']).count().reset_index()

    new_df = new_df.rename(columns = {'Number of Vehicles': 'Casualties'})

    new_df = new_df[['Reference Number', 'Grid Ref: Easting', 'Grid Ref: Northing', 'Accident Date', 'Time (24hr)', 'Casualties']]


    return new_df




clean2014 = make_my_cols(df2014)
clean2015 = make_my_cols(df2015)
clean2016 = make_my_cols(df2016)
clean2017 = make_my_cols(df2017)
clean2018 = make_my_cols(df2018)
clean2019 = make_my_cols(df2019)

clean2014.to_csv('./data/clean_2014.csv', index=False)
clean2015.to_csv('./data/clean_2015.csv', index=False)
clean2016.to_csv('./data/clean_2016.csv', index=False)
clean2017.to_csv('./data/clean_2017.csv', index=False)
clean2018.to_csv('./data/clean_2018.csv', index=False)
clean2019.to_csv('./data/clean_2019.csv', index=False)