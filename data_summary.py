import click
import numpy as np
import pandas as pd


BIRTHDATE_COL = 'DDN'
VISITS_DATE_COL = 'Début Passage'
AGE_COL = 'Age'
NAN_SUMMARY_NAME = '<vide>'

def read_order_relationship(config_value):
    return config_value.strip().split(' ')

def parse_config(config_value, column_name):
    if isinstance(config_value, np.int64):
        return [config_value]
    config_value = config_value.split(';')
    config_value = [cv.strip() for cv in config_value]
    if column_name not in [AGE_COL, VISITS_DATE_COL]:
        try:
            config_value = [int(cv) for cv in config_value]
        except ValueError:
            pass
    elif column_name == VISITS_DATE_COL:
        assert len(config_value) < 3, 'Date filtering should not have more than 2 elements'
        config_value = [pd.to_datetime(cv) for cv in config_value]
    else:
        config_value = [read_order_relationship(cv) for cv in config_value]
    return config_value

def build_query(config_value, column_name, df):
    if column_name not in [AGE_COL, VISITS_DATE_COL]:
        new_query = df[column_name].isin(config_value)
    elif column_name == VISITS_DATE_COL:
        lower_bound = config_value[0]
        new_query = pd.to_datetime(df[column_name]) >= lower_bound
        if len(config_value) == 2:
            upper_bound = config_value[1]
            new_query = new_query & (pd.to_datetime(df[column_name]) <= upper_bound)
    else:
        new_query = None
        for (op, num_value) in config_value:
            num_value = float(num_value)
            if op == '>':
                order_query = df[column_name] > num_value
            elif op in ['>=', '≥']:
                order_query = df[column_name] >= num_value
            elif op == '<':
                order_query = df[column_name] < num_value
            elif op in ['<=', '≤']:
                order_query = df[column_name] <= num_value
            else:
                raise ValueError(f'{op} not understood as a relationship operator')
            if new_query is None:
                new_query = order_query
            else:
                new_query = new_query & order_query
    return new_query

def format_value(value, col_name):
    if pd.isna(value):
        return NAN_SUMMARY_NAME
    elif isinstance(value, float):
        if int(value) == value:
            return int(value)
        else:
            return f'{value:.2f}'
    else:
        return value

def get_ordered_value_counts(series):
    vc = series.value_counts(dropna=False)
    try:
        ovc = vc.sort_index(
            ascending=False
        ).sort_values(
            ascending=False,
            kind='mergesort',
        )
    except TypeError:
        try:
            ovc = get_ordered_value_counts(pd.to_datetime(series))
        except TypeError:
            return vc
    return ovc

SEP = "*"*100

def summarize_data(visits_file_name, config_file_name, results_file_name, verbose=False):
    df_visits = pd.read_excel(
        visits_file_name,
        sheet_name=0,
        engine='openpyxl',
        convert_float=True,
        parse_dates=True,
    )
    print(SEP)
    print('Raw data file looks like the following:')
    print(df_visits.head(10))

    # reformat df visits
    for col_name in df_visits.columns:
        df_visits[col_name] = df_visits[col_name].astype('Int64', errors='ignore')
    df_visits.dropna(how='all', inplace=True)
    df_visits[AGE_COL] = (pd.to_datetime(df_visits[VISITS_DATE_COL]) - pd.to_datetime(df_visits[BIRTHDATE_COL])) / np.timedelta64(1, 'Y')
    print(SEP)
    print('Reformatted data file looks like the following:')
    print(df_visits.head(10))
    df_config = pd.read_excel(config_file_name, engine='openpyxl')
    assert len(df_config) == 1, "Config has not exactly one line"
    # config parsing
    dict_config = {
        k: parse_config(v, k)
        for k, v in df_config.loc[0].iteritems()
        if pd.notna(v)
    }
    print(SEP)
    print('Config has been read as the following:')
    print(dict_config)
    # https://stackoverflow.com/a/17071908/4332585
    query = None
    for k, v in dict_config.items():
        # here we would have a function that builds a query from the column name
        # and the values passed
        new_query = build_query(v, k, df_visits)
        if query is None:
            query = new_query
        else:
            query = (query & new_query)
    df_queried = df_visits[query]
    if verbose:
        print(SEP)
        print('The data meeting the conditions is the following (might be truncated for readability):')
        print(df_queried)
    results_age_col = df_queried.pop(AGE_COL)
    age_pos = list(df_queried.columns).index(BIRTHDATE_COL) + 1
    df_queried.insert(age_pos, AGE_COL, results_age_col)
    print('Now summarizing this information')
    # format the queried df in order to prepare for summary
    # Before formatting age compute the mean and std
    df_queried_formatted = df_queried.copy()
    age_col = df_queried_formatted[AGE_COL]
    mean_age = np.mean(age_col)
    std_age = np.std(age_col)
    df_queried_formatted[AGE_COL] = np.floor(age_col).astype(int)
    # summaries for each column
    # we can filter out elements that are in the config and those not worth
    n_queried = len(df_queried)
    results_formatted = {
        col_name: [
            f'{format_value(i, col_name)}: {v} / {n_queried}'
            for i, v in get_ordered_value_counts(df_queried_formatted[col_name]).iteritems()
        ]
        for col_name in df_queried_formatted.columns
    }
    results_formatted[AGE_COL] += [
        f'Mean: {mean_age:.4f}',
        f'Std: {std_age:.4f}',
    ]
    df_results = pd.DataFrame.from_dict(results_formatted, orient='index')
    df_results = df_results.transpose()
    print(SEP)
    print('The summaries are the following (might be truncated for readability):')
    print(df_results)
    writer = pd.ExcelWriter(results_file_name, engine='xlsxwriter')
    df_results.to_excel(writer, index=False, sheet_name='Results summary')
    df_queried.to_excel(writer, index=False, sheet_name='Results detail')
    writer.close()
    return df_results


@click.command()
@click.option('visits_file_name', '--data-file', type=click.Path(exists=True, dir_okay=False))
@click.option('config_file_name', '--config-file', type=click.Path(exists=True, dir_okay=False), default='config.xlsx')
@click.option('results_file_name', '--results-file', type=click.Path(dir_okay=False), default='results.xlsx')
@click.option('verbose', '--v', is_flag=True)
def summarize_data_click(visits_file_name, config_file_name, results_file_name, verbose):
    summarize_data(visits_file_name, config_file_name, results_file_name, verbose)


if __name__ == '__main__':
    summarize_data_click()
