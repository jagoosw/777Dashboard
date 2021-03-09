import streamlit as st
import time, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from requests import HTTPError

st.title("The Redboy's 777 Laps of St Legends in memory of Sam Fitzsimmons")
#try:
if (time.time()-os.stat("data.dat").st_mtime)>600:
    try:
        data=pd.read_excel('https://drive.google.com/uc?id=1KOAFOCxiyeom2XjN7aDW4Sys1NYxjXqk&export=download',sheet_name='data_input',engine='openpyxl').iloc[4:].drop(["Unnamed: 22","Unnamed: 23"],axis=1).fillna(0)
        data.to_pickle("data.dat")
    except:
        data=pd.read_pickle("data.dat")
        st.markdown("Warning: this plot is quite old because Google is rate limiting how often the app can fetch the data")
else:
    data=pd.read_pickle("data.dat")
    
total=[0,]+data.sum(axis=0).to_list()[1:]
cumtot=[sum(total[:ind+1]) for ind,v in enumerate(total)]
day=int(datetime.utcnow().strftime("%d"))

d2={"name":[],"day":[],"distance":[]}
people={k[1]:0 for k in data.itertuples()}
for row in data.itertuples():
        for ind,dist in enumerate(row[2:]):
            if ind+1<=day:
                if isinstance(dist,str):
                    dist=0
                d2["name"].append(row[1])
                d2["day"].append(ind+1)
                d2["distance"].append(dist+people[row[1]])
                people[row[1]]+=dist
people={k:v for k,v in sorted(people.items(),key=lambda item:item[1])}
d2=pd.DataFrame.from_dict(d2)

df_unstack=d2.groupby(["day","name"]).sum().unstack()
df_unstack=df_unstack.sort_values([df_unstack.index[-1]],axis=1,ascending=False)

names=[item[1] for item in df_unstack.keys().to_list()]
dist=df_unstack.iloc[8].to_list()
dists=[(name,dist[ind]) for ind,name in enumerate(names)]

plot=df_unstack.plot(kind='area',y='distance', stacked = True,legend=False, figsize=(9,16), cmap="gist_heat")
ax2=plot.twinx()
c=len(dists)
adj=0 if cumtot[day]!=cumtot[day-1] else 1
for bear in dists:
        x=c*(day-adj)/len(dists)
        ax2.plot([x,x],[0,bear[1]],linewidth=5)
        c-=1
ax2.set_ylim(0)
ax2.legend([p[1] for p in df_unstack.keys()[:20]], title="Leaderboard (right to left)")
plot.set_xlim(1,day-adj+.2)
plot.set_xlabel("Day")
plot.set_ylabel("Total distance/m")
ax2.set_ylabel("Individual distance/m")
plot.set_title("The Redboy's 777 Laps of St Legends in memory of Sam Fitzsimmons: Our progress")

fig = plot.get_figure()
st.pyplot(fig)

st.markdown("""In May of last year our beloved Captain EEE, Sam Fitzsimmons, passed away in May last year with Ewing's Sarcoma - a rare form of bone cancer.
To raise money for the Bone Cancer Research Trust, the Garcons are undertaking a grueling challenge, bear crawling a cumulative 777 laps of the St. Legends pitch in 20+1 days begining the 1st of March.""")
st.markdown("""To read our story, and for more details about the challenge, please see the link below:
[https://uk.virginmoneygiving.com/StJohnsRedboys](https://uk.virginmoneygiving.com/StJohnsRedboys)""")
st.markdown("""For source code and licence please see [GitHub](https://github.com/jagoosw/777Dashboard). Copyright 2021 Jago Strong-Wright [MIT Licence](https://github.com/jagoosw/777Dashboard/blob/master/LICENCE.md)""",unsafe_allow_html=True)