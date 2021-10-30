import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
from scipy import stats as st

df = pd.read_excel("./data/20211026_gonogo.xlsx")  # エクセルデータをデータフレーム化を行い、読み込み

df_all = df.iloc[:, 5:]  # 全体の記述統計量用のデータの抽出
df_preprocess = df_all.iloc[:, 3]  # RTタイムの列だけ抽出
all_describe_data = df_all.describe()  # 全体の記述統計量
all_describe_data.to_excel("./data/all_describe_data.xlsx")  # 全体の記述統計量をエクセルデータとして出力しデータファイルに格納
df_encoding_session = pd.get_dummies(df.loc[:, "Session"], prefix="Session")  # セッション番号についてOne_Hotエンコーディング
df_preprocessed = pd.concat([df_encoding_session, df_preprocess], axis=1)  # RTの列ととOne_Hot# エンコーディングしたデータを結合
df_preprocessed.to_excel("./data/df_preprocessed.xlsx")  # 前処理したデータをエクセルデータとして出力

# 反応時間における記述統計の作成
a = df_preprocessed[df_preprocessed["Session_1"] == True]
a_1 = a.iloc[:, -1].mean()
a_2 = a.iloc[:, -1].sem()
b = df_preprocessed[df_preprocessed["Session_2"] == True]
b_1 = b.iloc[:, -1].mean()
b_2 = b.iloc[:, -1].sem()
c = df_preprocessed[df_preprocessed["Session_3"] == True]
c_1 = c.iloc[:, -1].mean()
c_2 = c.iloc[:, -1].sem()
topic_describe = pd.DataFrame([[a_1, b_1, c_1],
                               [a_2, b_2, c_2]])
topic_describe.index = ["平均値", "標準誤差"]
topic_describe.columns = ["Long条件", "Medium条件", "Short条件"]
topic_describe.to_excel("./data/topic_describe.xlsx")


print(topic_describe)