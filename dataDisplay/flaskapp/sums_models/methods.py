# coding=utf-8
'''
    1.数据库的增、删、改工作
    2.个性化的查询要求
'''

from dataDisplay.flaskapp.sums_models.models import *
from dataDisplay.flaskapp.sums_models.analysis.models import *
from dataDisplay.flaskapp.models import *


def delet_data(table_name, id):
    '''
    删除对应id行的数据
    :param table_name:
    :param id:
    :return:
    '''
    exec(table_name+ '.query.filter_by(id = id).delete()')
    db.session.commit()


def find_id(table_name, year):
    '''
    根据年份信息寻找总结表中，对应年份数据对应的id
    :param table_name:
    :param year:
    :return:
    '''
    result = None
    exec ('result=' + table_name + '.query.filter_by(year = year).first()')
    id = result.id
    return id


def update_data(tale_name, id, new_data, columns):
    '''
    更新表中的某行数据, 以id（主键）为索引目标
    :param tale_name:
    :param id:
    :param new_data:
    :param columns:
    :return:
    '''
    values = []
    for index in range(len(new_data)):
        # 如果new_Data[index]中包含换行符，会报错, 需要保持字符串为raw string（repr, eval）
        # 接受更新值长度比原栏目长度短的情况
        data = str(new_data[index]).replace('\n', ' ')
        value = tale_name + '.' + columns[index] + ':' + "'" + data + "'"
        values.append(value)

    values = '{' + ', '.join(values) + '}'
    # print 'values', values
    exec( tale_name+'.query.filter_by(id = id).update(' + values + ')')
    db.session.commit()


def insert(table_name, xls_data, columns):
    '''
    全表格查找，匹配表格中的所有栏目
    :param table_name:
    :param xls_data:
    :param columns:
    :return:
    '''
    # 没有成功插入的数据
    fail_lists = []

    for data in xls_data:
        content = None
        try:
            exec('content = '+ table_name + '(columns, data)')
            db.session.add(content)
        except Exception, e:
            # models没有成功初始化
            print u'数据插入失败：', table_name, u'——', data
            print u'属性数目：', len(columns), u' 数据列数：', len(data)
            fail_lists.append(data)
            print e

        try:
            db.session.commit()
        except Exception, e:
            # print 'ERROR:', e
            db.session.rollback()

    return fail_lists


def extract_table(table_name, column_value):
    '''
    抽取数据库中对应表，对应栏目的数据
    :param table_name:
    :param column_value:
    :return:
    '''
    columns = column_value[0]
    values = column_value[1]
    ks_name = column_value[2]
    extract_list = []
    result = None
    exec('result = ' + table_name + '.query.all()')

    # 读取对应的table
    for data in result:
        temp = []
        for index in range(len(columns)):
            column = columns[index]
            value = values[index]
            if column:
                # 考虑一个单元格中包含的多个属性
                column = column.split(',')
                cell = []
                for e in column:
                    cell.append(eval('data.' + e))
                try:
                    temp.append(','.join(cell))
                except:
                    # cell = [None, None ]的情况
                    temp.append('')
            elif not column and value:
                temp.append(value)
            else:
                temp.append('')

        temp.append(ks_name)
        temp.append(table_name + '.' + str(eval('data.id')))
        extract_list.append(temp)

    return extract_list



