# coding=utf-8

from dataDisplay.flaskapp.rules import sums_rules, methods
from dataDisplay.flaskapp.calculation.auto_cal import select_table
from dataDisplay.flaskapp.sums_models import update


def sums_update(table_name, start_y, end_y):
    '''
    更新总结表中的统计信息，前提是总结表在数据库中有对应表
    只能更新自动统计的部分，手动统计部分更新不在此处
    :param table_name:
    :param start_y:
    :param end_y:
    :return:
    '''
    all_rules = sums_rules.get_sums_rule('datadisplay/flaskapp/data/sums.xlsx')
    conditions = all_rules[table_name]
    columns = methods.show_columns()

    # 获取一段时间内的统计信息
    datas = []
    for year in range(start_y, end_y+1):
        data = select_table(table_name, conditions, year)
        datas.append(data)

    # 更新到对应的table_name中
    column = columns[table_name][1]
    update.update_sums(table_name, datas, column)

    return datas