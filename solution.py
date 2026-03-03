import pandas as pd
import re


def add_virtual_column(df: pd.DataFrame, rule: str, new_column: str) -> pd.DataFrame:
    if not re.match(r'^[a-zA-Z_]+$', new_column):
        return pd.DataFrame()

    rule = rule.strip()

    if not re.match(r'^[a-zA-Z_\s\+\-\*]+$', rule):
        return pd.DataFrame()

    tokens = re.split(r'\s*([+\-*])\s*', rule)
    tokens = [t.strip() for t in tokens if t.strip()]

    columns = []
    operators = []
    for i, token in enumerate(tokens):
        if i % 2 == 0:
            if not re.match(r'^[a-zA-Z_]+$', token):
                return pd.DataFrame()
            if token not in df.columns:
                return pd.DataFrame()
            columns.append(token)
        else:
            if token not in ('+', '-', '*'):
                return pd.DataFrame()
            operators.append(token)

    if not columns:
        return pd.DataFrame()

    result = df[columns[0]].copy()
    for i, op in enumerate(operators):
        if op == '+':
            result = result + df[columns[i + 1]]
        elif op == '-':
            result = result - df[columns[i + 1]]
        elif op == '*':
            result = result * df[columns[i + 1]]

    df_result = df.copy()
    df_result[new_column] = result
    return df_result
