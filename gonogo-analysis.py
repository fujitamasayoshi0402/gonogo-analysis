import pandas as pd
from scipy import stats as st

from statsmodels.stats.multicomp import pairwise_tukeyhsd

df = pd.read_excel("./data/20211026_gonogo.xlsx")  # エクセルデータをデータフレーム化を行い、読み込み

df_all = df.iloc[:, 5:]  # 全体の記述統計量用のデータの抽出
df_preprocess = df_all.iloc[:, 3]  # RTタイムの列だけ抽出
all_describe_data = df_all.describe()  # 全体の記述統計量
all_describe_data.to_excel("./data/all_describe_data.xlsx")  # 全体の記述統計量をエクセルデータとして出力しデータファイルに格納
df_encoding_session = pd.get_dummies(df.loc[:, "Session"], prefix="Session")  # セッション番号についてOne_Hotエンコーディング
df_preprocessed = pd.concat([df_encoding_session, df_preprocess], axis=1)  # RTの列ととOne_Hot# エンコーディングしたデータを結合
df_preprocessed.to_excel("./data/df_preprocessed.xlsx")  # 前処理したデータをエクセルデータとして出力

# 反応時間における記述統計の作成
a = df_preprocessed[df_preprocessed["Session_1"] == True]  # 各セッションにおけるデータのみ抽出
a_1 = a.iloc[:, -1].mean()  # 各セッションのnogoのRTの平均
a_2 = a.iloc[:, -1].sem()   # 各セッションのnogoのRTの標準誤差
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


# １要因参加者間の分散分析

# SS_total 全体平方和
SS_total = 0
whole_mean = df_preprocess.mean()  # nogoのRTの全体平均

for i in range(3):
    if i == 0:
        for j in a.iloc[:, -1]:
            SS_total += (j - whole_mean) ** 2
    elif i == 1:
        for j in b.iloc[:, -1]:
            SS_total += (j - whole_mean) ** 2
    else:
        for j in c.iloc[:, -1]:
            SS_total += (j - whole_mean) ** 2

# SS_A 群間平方和
SS_A = 0

for k in range(3):
    if k == 0:
        SS_A += (a_1 - whole_mean) ** 2
    elif k == 1:
        SS_A += (b_1 - whole_mean) ** 2
    else:
        SS_A += (c_1 - whole_mean) ** 2
    SS_A *= 3

# η_2値の計算と分散分析

η_2 = SS_A/SS_total
f, p = st.f_oneway(a.iloc[:, -1], b.iloc[:, -1], c.iloc[:, -1])

# Tukey法へチャレンジしたけど無理そう間に合わない
# p_1 = pairwise_tukeyhsd(a.iloc[:, -1], b.iloc[:, -1])
# p_2 = pairwise_tukeyhsd(a.iloc[:, -1].mean(), c.iloc[:, -1].mean())
# p_3 = pairwise_tukeyhsd(b.iloc[:, -1].mean(), c.iloc[:, -1].mean())
print(η_2, f, p)

