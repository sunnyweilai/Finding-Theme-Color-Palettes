from numpy import *
import pandas as pd
import os.path
import numpy as np



def combine_dataframe(path_rgb, path_lab, output_path):
    files = os.listdir(path_rgb)
    files.sort()
    rgb_list = []
    for file in files:
        new_path = path_rgb + '/' + str(file)
        df = pd.read_csv(new_path,engine='python')
        df.drop('Unnamed: 0', axis=1, inplace=True)
        df.rename(columns=lambda x: str('#1_lab') + '_' + str(x[0]), inplace=True)
        df['NumberofColors'] = np.arange(1, 21)
        df.set_index('NumberofColors', inplace=True)
        (pic_name, pic_df) = (int(str(file)[:2]), df)
        rgb_list.append((pic_name, pic_df))

    files1 = os.listdir(path_lab)
    files1.sort()
    lab_list = []
    for file in files1:
        new_path1 = path_lab + '/' + str(file)
        df1 = pd.read_csv(new_path1,engine='python')
        df1.drop('Unnamed: 0', axis=1, inplace=True)
        df1.rename(columns=lambda x: str('#2_lab') + '_' + str(x[0]), inplace=True)
        df1['NumberofColors'] = np.arange(1, 21)
        df1.set_index('NumberofColors', inplace=True)
        (pic_name1, pic_df1) = (int(str(file)[:2]), df1)
        lab_list.append((pic_name1, pic_df1))

    r_l_list = []
    for namer, dfr in rgb_list:
        for namel, dfl in lab_list:
            if namer == namel:
                dfn = dfr.join(dfl)
                key_list = []
                for key in dfn:
                    key_list.append(key)
                dfn = dfn[[key_list[0], key_list[4], key_list[1], key_list[5],
                           key_list[2], key_list[6], key_list[3],
                           key_list[7]]]
                (pic_name2, pic_df2) = (namer, dfn)
                r_l_list.append((pic_name2, pic_df2))

    f = lambda x: '%.3f' % x
    for pic_name, pic_df in r_l_list:
        for key in pic_df:
            pic_df[key] = pic_df[key].apply(f)
        pic_df.to_csv(output_path + '/' + 'image%s.csv' % (pic_name))



path_rgb = 'lab_allIQAs/#1lab_results/lab_50'
path_lab = 'lab_allIQAs/#2lab_results/lab_50'
output_path = 'combine_2lab_50'

combine_dataframe(path_rgb, path_lab, output_path)

