import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

QCver='ABCD_QA'
QCver='FBIRN_QA'
if QCver =='FBIRN_QA':
    isFBIRNQA=1
else:
    isFBIRNQA=0

figsout="/Users/petralenzini/work/datarequests/MikeHarms/AABC_Agar_2023/AGAR_QC/pngs/"
AGARQCAll=pd.read_csv("AGAR_QC_2023.10.02.PL_PREPPED.csv")
#AGARQCAll['Date'] = pd.to_datetime(AGARQCAll['Date'])
#AGARQC=AGARQCAll.loc[AGARQCAll.Date>'2014-05-01']

#not sure what this is doing:
AGARQC=AGARQCAll.loc[(AGARQCAll.SeriesDesc.str.contains(QCver)) & (~(AGARQCAll.SeriesDesc.str.contains("flip10")))]

#drop the ceresphere coil because low counts:
AGARQC=AGARQC.loc[~(AGARQC.Coil.str.contains("Cere32B"))].copy()

AGARQCnodup=AGARQC.drop_duplicates(subset=['SeriesDesc','Date','Coil','ScannerPerMRID']).copy()
varlist=['SNR']
def plot6(varlist=['meanfwhmx','meanfwhmy','meanfwhmz']):
    melted=pd.melt(AGARQCnodup,id_vars=['Date','Coil','ScannerPerMRID'],value_vars=varlist)
    with sns.axes_style("white"):
        g = sns.FacetGrid(melted, row="Coil", col="ScannerPerMRID", margin_titles=True, height=2.5)
    g.map(sns.lineplot, 'Date', 'value',markersize=.25,hue=melted.variable)
    #g.set(yticks=np.arange(4,20,2))
    labelsx=['2016','2018','2020','2022']
    xrange=np.arange(42740,44932,730)
    g.set(xticks=xrange)
    g.set_xticklabels(labelsx)
    g.figure.subplots_adjust(wspace=.02, hspace=.02)
    v4title = str(varlist).replace("[", "").replace("]", "").replace(",", "_").replace(" ", "").replace("'", "")
    plt.savefig(figsout+v4title)
    #g.legend()
    #g.add_legend()
    plt.show()

plot6(varlist=['SNR'])

plot6(varlist=['tSNR'])
plot6(varlist=['mean'])
plot6(varlist=['std'])
plot6(varlist=['PercentFluctuation'])
plot6(varlist=['Drift','driftfit'])
plot6(varlist=['rdc'])
plot6(varlist=['meanghost','meanbrightghost'])
plot6(varlist=['BIRN_HUMAN_SFNR','BIRN_HUMAN_SNR'])
plot6(varlist=['meanfwhmx','meanfwhmy','meanfwhmz'])

#write out the observations with high BIRN_HUMAN_SFNR
AGARQCnodup.loc[AGARQCnodup.BIRN_HUMAN_SFNR > 1e6][['Date','Coil','Scanner','SeriesDesc','BIRN_HUMAN_SFNR']].to_csv('High_BIRN_HUMAN_SFNR.csv',index=False)
