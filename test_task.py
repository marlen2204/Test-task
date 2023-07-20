import pandas as pd
import json


def load_data(file):
    with open(file, 'r', encoding='utf-8') as file:
        text = json.load(file)
    return text


def task_1(data):
    shipping_cost = []
    warehouse = set()
    sum_highway_cost = {}
    for i in range(len(data)):
        if data[i]['warehouse_name'] not in warehouse:
            warehouse.add(data[i]['warehouse_name'])
            product_count = 0
            sum_highway_cost[data[i]['warehouse_name']] = data[i]['highway_cost']
            for j in data[i]['products']:
                product_count += j['quantity']
            shipping_cost.append({'warehouse_name': data[i]['warehouse_name'],
                                  'product_count': product_count})
        else:
            sum_highway_cost[data[i]['warehouse_name']] += data[i]['highway_cost']
            for j in range(len(shipping_cost[:i])):
                if data[i]['warehouse_name'] == shipping_cost[j]['warehouse_name']:
                    for k in data[i]['products']:
                        shipping_cost[j]['product_count'] += k['quantity']
    for i in range(len(shipping_cost)):
        shipping_cost[i]['price'] = sum_highway_cost[shipping_cost[i][
            'warehouse_name']] // shipping_cost[i]['product_count']

    warehouses = []
    product_count = []
    price = []
    for i in range(len(shipping_cost)):
        warehouses.append(shipping_cost[i]['warehouse_name'])
        product_count.append(shipping_cost[i]['product_count'])
        price.append(shipping_cost[i]['price'])

    highway_cost_table = {'warehouses': warehouses,
                          'product_count': product_count,
                          'price': price
                          }
    df = pd.DataFrame(highway_cost_table)
    return df


def task_2(data):
    products = data['products']

    df = pd.DataFrame({'product': [],
                       'quantity': [],
                       'income': [],
                       'expenses': [],
                       'profit': []})

    for i in range(len(products)):

        for j in products[i]:
            if j['product'] not in df['product']:
                quantity = j['quantity']
                df.loc[len(df.index)] = [
                    j['product'],
                    quantity,
                    quantity * j['price'],
                    quantity * data.iloc[i]['highway_cost'],
                    quantity * j['price'] -
                    - quantity * data.iloc[i]['highway_cost']]
    return pd.pivot_table(df,
                          index=['product'],
                          values=['quantity', 'income', 'expenses', 'profit'],
                          aggfunc='sum')


def task_3(data, result_task_1):
    df = pd.DataFrame({'order_id': [],
                       'order_profit': []})
    for i in range(len(data)):

        quantity = 0
        warehouse = data.loc[i]['warehouse_name']
        cost = 0
        for k in range(len(result_task_1)):
            if result_task_1.loc[k]['warehouses'] == warehouse:
                cost = result_task_1.loc[k]['price']
        for j in data.loc[i]['products']:
            quantity += j['quantity']
            df.loc[len(df.index)] = [
                data.loc[i]['order_id'],
                quantity * cost
            ]

    return pd.pivot_table(df,
                          index=['order_id'],
                          values=['order_profit'],
                          aggfunc='sum'), df['order_profit'].mean()


def task_4(data, result_task_1):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    df = pd.DataFrame({'warehouse_name': [],
                       'product': [],
                       'quantity': [],
                       'profit': [],
                       'percent_profit_product_of_warehouse': []})

    for i in range(len(data)):
        warehouse = data.loc[i]['warehouse_name']
        count_item = {}
        price = result_task_1.loc[result_task_1['warehouses'] ==
                                  warehouse]['price'].to_string().split()[1]

        for j in data.loc[i]['products']:
            if f'{warehouse}' + f'{j["product"]}' not in count_item:
                count_item[f'{warehouse}' + f'{j["product"]}'] = j['quantity']
                df.loc[len(df.index)] = [
                    warehouse,
                    j['product'],
                    j['quantity'],
                    count_item[f'{warehouse}' + f'{j["product"]}'] * j['price'] -
                    count_item[f'{warehouse}' + f'{j["product"]}'] * int(price),
                    (j['quantity'] * j['price'] /
                     count_item[f'{warehouse}'f'{j["product"]}']) / 100]

            else:
                count_item[f'{warehouse}' + f'{j["product"]}'] += j['quantity']

    return df.groupby(['warehouse_name', 'product']). \
        agg({'quantity': ['sum'],
             'profit': ['sum'],
             'percent_profit_product_of_warehouse': ['sum']}).reset_index()


def task_6(result_task_4):
    category = []
    # cut_labels = ['A', 'B', 'C']
    # cut_bins = [0, 70, 90, 100]
    #
    # result_task_4['category'] = pd.cut(result_task_4['percent_profit_product_of_warehouse'],
    #                                    bins=cut_bins,
    #                                    labels=cut_labels)

    for row in result_task_4.itertuples():
        if row[4] <= 70:
            category.append('A')
        elif 70 < row[4] <= 90:
            category.append('B')
        else:
            category.append('C')
    result_task_4['category'] = category
    return result_task_4.head()


if __name__ == '__main__':
    data = pd.read_json('trial_task.json')
    print('Task 1'.center(60))
    task1 = task_1(load_data('trial_task.json'))
    print(task1)
    print('Task 2'.center(60))
    t2 = task_2(data)
    print(t2)
    print('Task 3'.center(60))
    task3 = task_3(data, task1)
    print(task3[0])
    print(f'Average value = {task3[1]}')
    task4 = task_4(data, task1)
    print('Task 4'.center(60))
    print(task4)
    print('Task 6'.center(60))
    print(task_6(task4))
