import pandas as pd
import xml.etree.ElementTree as ET
import boto3
import botocore
import os
from functions import xml_to_dict


s3 = boto3.resource('s3')
bucket = s3.Bucket('payability-uploads-test')
objects = list(bucket.objects.filter(Prefix='peterc'))

for path_ in objects:
    key_ = path_.key
    if '.xml' in key_:
        seller, date = str.split(key_, '/')[1:3]
        local_path = 'data/{}_{}'.format(seller, date)
        try:
            bucket.download_file(key_, local_path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

files = os.listdir('data')
file = [file for file in files if '2019-01-15' in file]


dict_list = []

for xml_file in file:
    seller, date = str.split(xml_file, '_')
    path_xml = 'data/' + xml_file
    tree = ET.parse(path_xml)
    root_file = tree.getroot()
    d = xml_to_dict(root=root_file)
    d['supplier_key'] = seller
    d['date'] = date
    dict_list.append(d)


df_list = []
for dict_ in dict_list:
    df_row = pd.DataFrame(dict_, index=[0])
    df_list.append(df_row)

df = pd.concat(df_list)


df.set_index(['supplier_key', 'date'], inplace=True)


def replace_percante_sign(col): return col.str.replace('%', "")


def remove_whitespace(col): return col.str.strip()


df = df.apply(replace_percante_sign)
df = df.apply(remove_whitespace)

float_columns = [col for col in df.columns if '_status' not in col]


for i in range(len(float_columns)):
    df[float_columns[i]] = pd.to_numeric(df[float_columns[i]])

df.to_csv('pandas_df_from_api.csv')
