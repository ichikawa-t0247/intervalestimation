import streamlit as st
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import seaborn as sns
from scipy.stats import beta
sns.set(font_scale=2)
st.sidebar.markdown('区間推定(母比率)対象のデータを入力してください')
visitors_a = st.sidebar.number_input('分母', value=100)
conversion_a = st.sidebar.number_input('分子', value=50)
alpha1 = st.sidebar.number_input('信頼度(%)', value=95)
sample1 = st.sidebar.number_input('(必要サンプル数を求めるために設定)求めたい母比率の幅(%)', value=5.00)
alpha=alpha1/100
sample=sample1/100
cvr_a = conversion_a / visitors_a
st.sidebar.markdown(f'比率: **{"{:.1%}".format(cvr_a)}**')


st.header('区間推定(母比率)アプリ')
st.markdown(r'''結果の分母と分子を入力''')
st.subheader('対象')
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

st.markdown('ベータ分布を利用した母比率の区間推定。(サンプル少ない場合に利用)')
lower_limit = beta.ppf((1-alpha)/2, conversion_a, visitors_a-conversion_a+1)
upper_limit = beta.ppf(1-(1-alpha)/2, conversion_a+1, visitors_a-conversion_a)
st.markdown(f'    <center><font size=7 color="#FF4B00"> {lower_limit:.3%}～{upper_limit:.3%}</font></center>', unsafe_allow_html=True)

import numpy as np
from matplotlib import pyplot as plt
import pymc3 as pm

plt.style.use('grayscale')
plt.style.use('seaborn-whitegrid')
np.random.seed(0)

with pm.Model() as model:
  theta = pm.Uniform('theta', lower=0, upper=1)
  # theta = pm.Beta('theta', alpha=1, beta=1)
  obs = pm.Binomial('a', p=theta, n=visitors_a, observed=conversion_a)
  trace = pm.sample(5000, chains=2)

with model:
  pm.plot_posterior(trace, hdi_prob=0.95)



st.markdown('正規分布を利用した母比率の区間推定。(サンプル数30以上で利用可能)')
bottom, up = sp.stats.binom.interval(alpha=alpha, n=visitors_a, p=conversion_a/visitors_a, loc=0)
st.markdown(f'<center><font size=7 color="#FF4B00"> {bottom/visitors_a:.3%}～{up/visitors_a:.3%}</font></center>', unsafe_allow_html=True)
p=conversion_a/visitors_a
st.markdown('必要サンプル数')
bottom, up = sp.stats.norm.interval(alpha, loc=0, scale=1)
st.markdown(f'<center><font size=7 color="#FF4B00"> {pow((2*up*np.sqrt(p*(1-p)))/sample, 2):.0f}</font></center>', unsafe_allow_html=True)
