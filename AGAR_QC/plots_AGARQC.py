import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

rootdir="/Users/petralenzini/work/datarequests/AGAR_QC/"
infile="AGAR_QC_2023.10.11.PL_PREPPED.csv"
figsout=rootdir+"pngs/"

QCver='ABCD_QA'
QCver='FBIRN_QA'
if QCver =='FBIRN_QA':
    isFBIRNQA=1
else:
    isFBIRNQA=0

AGARQCAll=pd.read_csv(rootdir+infile)

#not sure what this is doing:
AGARQC=AGARQCAll.loc[(AGARQCAll.SeriesDesc.str.contains(QCver)) & (~(AGARQCAll.SeriesDesc.str.contains("flip10")))]

#drop the ceresphere coil because low counts:
AGARQC=AGARQC.loc[~(AGARQC.Coil.str.contains("Cere32B"))].copy()

AGARQCnodup=AGARQC.drop_duplicates(subset=['SeriesDesc','Date','Coil','ScannerPerMRID']).copy()
varlist=['SNR']
def plot6(df=AGARQCnodup,varlist=['meanfwhmx','meanfwhmy','meanfwhmz'],yax=(),ytick=[],ylab=[]):
    melted=pd.melt(df,id_vars=['DateDec','Coil','ScannerPerMRID'],value_vars=varlist)
    with sns.axes_style("white"):
        g = sns.FacetGrid(melted, row="Coil", col="ScannerPerMRID", margin_titles=True, height=2.5)
    #manipulate marker sizes here.  note that hue is necessary for overlays
    g.map(sns.scatterplot, 'DateDec', 'value',hue=melted.variable,s=20)#,facecolor=None)
    g.map(sns.lineplot, 'DateDec', 'value',markersize=.01, hue=melted.variable)
    labelsx=['2019','2021','2023']
    xrange=np.array([2019,2021,2023])
    g.set(xticks=xrange)
    g.set_xticklabels(labelsx)
    if len(varlist)==1:
        g.set_ylabels(varlist[0])
    if len(varlist)>1:
        g.set_ylabels("")
    if len(yax)>0:
        g.set(ylim=yax)
    if len(ytick)>0:
        yrange = np.array(ytick)
        g.set(yticks=yrange)
    if len(ylab) > 0 and len(ylab) == len(ytick):
        labelsy = ylab
        g.set_yticklabels(labelsy)
    if len(varlist)>1:
        g.add_legend()
    g.figure.subplots_adjust(wspace=.02, hspace=.02)
    v4title = str(varlist).replace("[", "").replace("]", "").replace(",", "_").replace(" ", "").replace("'", "")
    plt.savefig(figsout+v4title)
    plt.show()
#Can we add small circle markers to each data point in the plots?

#tweak plots with yax (axis range), ytick (where you want ticks), ylab (labels for ticks)
plot6(varlist=['SNR'], ytick=[400, 800, 1200],ylab=[])
plot6(varlist=['tSNR'],yax=(0, 1000), ytick=[250, 500,750],ylab=[])
plot6(varlist=['mean'],yax=(0, 2000), ytick=[500,1000,1500],ylab=[])
plot6(varlist=['std'])
plot6(varlist=['PercentFluctuation'],yax=(0, .2))
plot6(varlist=['Drift','driftfit'])
plot6(varlist=['rdc'])
plot6(varlist=['meanghost','meanbrightghost'])
plot6(varlist=['BIRN_HUMAN_SFNR','BIRN_HUMAN_SNR'])#,yax=(0, 10000000))
plot6(varlist=['meanfwhmx','meanfwhmy','meanfwhmz'])

#write out the observations with high BIRN_HUMAN_SFNR
AGARQCnodup.loc[AGARQCnodup.BIRN_HUMAN_SFNR > 1e6][['Date','Coil','Scanner','SeriesDesc','BIRN_HUMAN_SFNR']].to_csv(rootdir+'High_BIRN_HUMAN_SFNR.csv',index=False)
