import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import beta
sns.set(font_scale=2)
st.sidebar.markdown('区間推定(母比率)対象のデータを入力してください')
visitors_a = st.sidebar.number_input('分母', value=100)
conversion_a = st.sidebar.number_input('分子', value=50)
alpha = st.sidebar.number_input('信頼度', value=0.95)
cvr_a = conversion_a / visitors_a
st.sidebar.markdown(f'比率: **{"{:.1%}".format(cvr_a)}**')


st.header('区間推定(母比率)アプリ')
st.markdown(r'''結果の分母と分子を入力''')
st.subheader('テスト対象')
st.markdown(rf'''
    <table>
      <tr>
        <th>パターン</th><th>分母</th><th>分子</th><th>比率</th>
      </tr>
      <tr>
        <td>A</td><td>{visitors_a}</td><td>{conversion_a}</td><td>{"{:.1%}".format(cvr_a)}</td>
      </tr>
    </table>
    ''', unsafe_allow_html=True)
st.subheader('ABテスト')
st.markdown('統計的仮説検定のABテスト(統計的仮説検定)の結果。（分散不均等を仮定したt検定）')
a = np.zeros(visitors_a)
a[:conversion_a] = 1
b = np.zeros(visitors_ｂ)
b[:conversion_ｂ] = 1
res = stats.ttest_ind(a, b, equal_var=False)
st.markdown(f'p値: **{"{:.4}".format(res[1])}**')
if res[1] <= 0.05:
  st.markdown(r'''
    <center><font size=7 color="#00B06B">95%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
elif res[1] <= 0.1:
  st.markdown(r'''
    <center><font size=7 color="#F2E700">90%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
elif res[1] <= 0.2:
  st.markdown(r'''
    <center><font size=7 color="#F2E700">80%の信頼度で有意差あり</font></center>
    ''', unsafe_allow_html=True)
else:
  st.markdown(r'''
    <center><font size=7 color="#FF4B00">有意差なし</font></center>
    ''', unsafe_allow_html=True)

st.markdown('ベータ分布を利用した母比率の区間推定。(サンプル少ない場合に利用)')
alpha = 0.05 # 95%信頼区間
visitors_a = 17        # 試行回数　
conversion_a = 17        # 成功回数

lower_limit = beta.ppf((1-alpha)/2, visitors_a, conversion_a-visitors_a+1)
upper_limit = beta.ppf(1-(1-alpha)/2, visitors_a+1, conversion_a-visitors_a)
print(f'95% Confidence interval: [{lower_limit:.5f}, {upper_limit:.5f}]')

st.markdown(f'95% Confidence interval: [{lower_limit:.5f}, {upper_limit:.5f}]')
