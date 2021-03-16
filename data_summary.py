from dateutil.parser._parser import ParserError

import click
import numpy as np
import pandas as pd


BIRTHDATE_COL = 'DDN'
VISITS_DATE_COL = 'Début Passage'
AGE_COL = 'Age'
OR_SPLIT = ';'
AND_SPLIT = '+'
NAN_SUMMARY_NAME = '<vide>'

def read_order_relationship(config_value):
    return config_value.strip().split(' ')

def date_parsing(series):
    return pd.to_datetime(series, dayfirst=True)

def parse_config(config_value, column_name):
    if AND_SPLIT in str(config_value):
        cfg_type = 'and'
    else:
        cfg_type = 'or'
    if isinstance(config_value, (np.int64, float, int, np.float64)):
        return [str(config_value)]
    config_value = config_value.split(AND_SPLIT if cfg_type == 'and' else OR_SPLIT)
    config_value = [cv.strip() for cv in config_value]
    if column_name not in [AGE_COL, VISITS_DATE_COL]:
        try:
            config_value = [str(cv) for cv in config_value]
        except ValueError:
            pass
    elif column_name == VISITS_DATE_COL:
        assert len(config_value) < 3, 'Date filtering should not have more than 2 elements'
        config_value = [pd.to_datetime(cv) for cv in config_value]
    else:
        config_value = [read_order_relationship(cv) for cv in config_value]
    return config_value, cfg_type

def normalize_str_series(series):
    normalized_series = series.str.normalize(
        'NFKD',
    ).str.encode(
        'ascii',
        errors='ignore',
    ).str.decode(
        'utf-8',
    ).str.strip().str.lower()
    return normalized_series

def build_query(config_value, column_name, df, cfg_type='or'):
    if column_name not in [AGE_COL, VISITS_DATE_COL]:
        normalized_column = normalize_str_series(df[column_name])
        new_query = None
        for cv in config_value:
            cv_query = normalized_column.str.contains(cv.lower().strip())
            if new_query is None:
                new_query = cv_query
            else:
                if cfg_type == 'or':
                    new_query = new_query | cv_query
                else:
                    new_query = new_query & cv_query
    elif column_name == VISITS_DATE_COL:
        lower_bound = config_value[0]
        new_query = date_parsing(df[column_name]) >= lower_bound
        if len(config_value) == 2:
            upper_bound = config_value[1]
            new_query = new_query & (date_parsing(df[column_name]) <= upper_bound)
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

def build_dict_query(dict_config, df):
    query = None
    for k, (config_value, cfg_type) in dict_config.items():
        # here we would have a function that builds a query from the column name
        # and the values passed
        new_query = build_query(config_value, k, df, cfg_type)
        if query is None:
            query = new_query
        else:
            query = (query & new_query)
    return query

def handle_float_value(float_value):
    if int(float_value) == float_value:
        return int(float_value)
    else:
        return f'{float_value:.2f}'

def format_value(value, col_name):
    if pd.isna(value) or value in ['nan', '<NA>']:
        return NAN_SUMMARY_NAME
    elif isinstance(value, float):
        handle_float_value(value)
    else:
        try:
            value = float(value)
        except ValueError:
            return value
        else:
            return handle_float_value(value)

def get_ordered_value_counts(series, col_name):
    vc = series.apply(str).value_counts(dropna=False)
    try:
        ovc = vc.sort_index(
            ascending=False
        ).sort_values(
            ascending=False,
            kind='mergesort',
        )
    except TypeError:
        try:
            ovc = get_ordered_value_counts(date_parsing(series), col_name)
        except (TypeError, ParserError):
            return vc
    return ovc

SEP = "*"*100

def summarize_data(visits_file_name, config_file_name, results_file_name, verbose=False):
    df_visits = pd.read_excel(
        visits_file_name,
        engine='openpyxl',
    )
    print(SEP)
    print('Raw data file looks like the following:')
    print(df_visits.head(10))

    # reformat df visits
    df_visits.dropna(how='all', inplace=True)
    df_visits[AGE_COL] = (date_parsing(df_visits[VISITS_DATE_COL]) - date_parsing(df_visits[BIRTHDATE_COL])) / np.timedelta64(1, 'Y')
    df_visits = df_visits.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df_visits_formatted = df_visits.copy()
    for col_name in df_visits.columns:
        if col_name not in [BIRTHDATE_COL, VISITS_DATE_COL, AGE_COL]:
            df_visits_formatted[col_name] = df_visits_formatted[col_name].apply(str).astype('string')
    print(SEP)
    print('Reformatted data file looks like the following:')
    print(df_visits_formatted.head(10))
    df_config = pd.read_excel(config_file_name, engine='openpyxl')
    assert len(df_config) in [1, 2], "Config has not exactly 1 or 2 line(s)"
    # config parsing
    dict_config = {
        k: parse_config(v, k)
        for k, v in df_config.loc[0].iteritems()
        if pd.notna(v)
    }
    if len(df_config) == 2:
        dict_config_neg = {
            k: parse_config(v, k)
            for k, v in df_config.loc[1].iteritems()
            if pd.notna(v)
        }
    print(SEP)
    print('Config has been read as the following:')
    print(dict_config)
    if len(df_config) == 2:
        print('Negative config has been read as the following:')
        print(dict_config_neg)
    # https://stackoverflow.com/a/17071908/4332585
    query = build_dict_query(dict_config, df_visits_formatted)
    if len(df_config) == 2:
        query_neg = build_dict_query(dict_config_neg, df_visits_formatted)
        query = query & (~ query_neg)
    df_queried = df_visits_formatted[query]
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
            for i, v in get_ordered_value_counts(df_queried_formatted[col_name], col_name).iteritems()
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
    df_visits[query].to_excel(writer, index=False, sheet_name='Results detail')
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
