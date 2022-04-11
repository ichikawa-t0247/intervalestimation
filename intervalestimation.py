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

def hmv(xs, ps, alpha=0.95):
  xps = sorted(zip(xs, ps), key=lambda xp: xp[1], reverse=True)
  xps = np.array(xps)
  xs = xps[:, 0]
  ps = xps[:, 1]
  return np.sort(xs[np.cumsum(ps) <= alpha])
thetas = np.linspace(0, 1, 1001)

def posterior(a, N):
  alpha = a + 1
  beta = N - a + 1
  numerator = thetas ** (alpha - 1) * (1 - thetas) ** (beta - 1)
  return numerator / numerator.sum()

ps = posterior(conversion_a, visitors_a)

hm_thetas = hmv(thetas, ps, alpha=0.95)
plt.plot(thetas, ps)
plt.annotate('', xy=(hm_thetas.min(), 0),
              xytext=(hm_thetas.max(), 0),
              arrowprops=dict(color='black', shrinkA=0, shrinkB=0,
                              arrowstyle='<->', linewidth=2))
plt.annotate('%.3f' % hm_thetas.min(), xy=(hm_thetas.min(), 0),
              ha='right', va='bottom')
plt.annotate('%.3f' % hm_thetas.max(), xy=(hm_thetas.max(), 0),
              ha='left', va='bottom')
plt.annotate('95% HDI', xy=(hm_thetas.mean(), 0),
              ha='center', va='bottom')
hm_region = (hm_thetas.min() < thetas) & (thetas < hm_thetas.max())
plt.fill_between(thetas[hm_region], ps[hm_region], 0, alpha=0.3)
plt.xlabel(r'$\theta$')
plt.ylabel(r'$p(\theta)$')
plt.xlim(0, 0.3)
plt.tight_layout()
plt.show()


st.markdown('正規分布を利用した母比率の区間推定。(サンプル数30以上で利用可能)')
bottom, up = sp.stats.binom.interval(alpha=alpha, n=visitors_a, p=conversion_a/visitors_a, loc=0)
st.markdown(f'<center><font size=7 color="#FF4B00"> {bottom/visitors_a:.3%}～{up/visitors_a:.3%}</font></center>', unsafe_allow_html=True)
p=conversion_a/visitors_a
st.markdown('必要サンプル数')
bottom, up = sp.stats.norm.interval(alpha, loc=0, scale=1)
st.markdown(f'<center><font size=7 color="#FF4B00"> {pow((2*up*np.sqrt(p*(1-p)))/sample, 2):.0f}</font></center>', unsafe_allow_html=True)
