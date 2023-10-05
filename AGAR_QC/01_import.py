import pandas as pd

#read the data into a pandas dataframe
csvfile="/Users/petralenzini/work/datarequests/MikeHarms/AABC_Agar_2023/AGAR_QC/AGAR_QC_2023.10.02.csv";
AGARQC=pd.read_csv(csvfile)
AGARQC=AGARQC.drop(columns=['Subject'])#Default 'Subject' variable is in form of IntraDB UID;

#ANY MR_date filters????????
#rename some columns
renamefields={'MR ID':'MR_ID','MR Date':'Date','stat_snr':'SNR','stat_mean':'mean','stat_stddev':'std','AGAR_SFNR':'tSNR','Subject_Label':'Subject'}
AGARQC=AGARQC.rename(columns=renamefields).copy()

#replace some of the scanner names with Bays
AGARQC.loc[AGARQC.Scanner=='MRC35177','Scanner']= 'Bay3'
AGARQC.loc[AGARQC.Scanner=='AWP166038','Scanner']= 'Bay2'

#REGULAR AGARS
#Parse subject and coil from MR_ID (the cere exception will overwrite this)
AGARQC['SubjPerMRID']=AGARQC['MR_ID'].str.split("_",expand=True)[0]+'_'+AGARQC['MR_ID'].str.split("_",expand=True)[1]#cats(scan(MR_ID,1,'_'),'_',scan(MR_ID,2,'_'));
AGARQC['Coil']=AGARQC['MR_ID'].str.split("_",expand=True)[2]#scan(MR_ID,3,'_'); ** Have to trust that Coil portion of MR_ID was entered correctl

#Coil currently has Coil AND scanner (TMI), but some Coils aren't specified at all, per MR ID.
#set missing BAY to BAY 0 in the coil string so that stringlength is uniform, and then to whatever is in the Scanner column
AGARQC.loc[AGARQC.Coil.str.upper().str.contains("BAY")==False,'Coil']=AGARQC.Coil.str.replace("ch","chBay0")
#now parse down Coil string further in to Scanner and Coil.
AGARQC['ScannerPerMRID']=AGARQC['Coil'].str[4:] #substr(Coil,5);
AGARQC['Coil']=AGARQC['Coil'].str[0:4]#Coil = substr(Coil,1,4);
#lastly replace tenoirart 'Bay0' with whatever was in the scanner column
AGARQC.loc[AGARQC.ScannerPerMRID=='Bay0','ScannerPerMRID']=AGARQC['Scanner']

#CERESPHERE AGARS need to be parsed differently
#parse out SubjPerMRID
AGARQC.loc[(AGARQC.Coil.str.contains('C')),'SubjPerMRID']=AGARQC['MR_ID'].str.split("_",expand=True)[0]#,"Coil",'SubjPerMRID''ScannerPerMRID']]
#parse out Coil and Scanner
AGARQC.loc[(AGARQC.Coil.str.contains('C')),'Coil']=AGARQC['MR_ID'].str.split("_",expand=True)[1]#,"Coil",'SubjPerMRID''ScannerPerMRID']]
AGARQC.loc[(AGARQC.Coil.str.contains('C')),'ScannerPerMRID']=AGARQC['Coil'].str[6:] #substr(Coil,5);
AGARQC.loc[(AGARQC.Coil.str.contains('C')),'Coil']=AGARQC['Coil'].str[0:7]#Coil = substr(Coil,1,4);

inconsistent=AGARQC.loc[((AGARQC.Scanner != AGARQC.ScannerPerMRID))][['MR_ID','Date','SeriesDesc','Scanner','Subject Label','SubjPerMRID','Coil','ScannerPerMRID']]# & (AGARQC.ScannerPerMRID != '')) | (AGARQC['Subject Label'] != AGARQC.SubjPerMRID)]
inconsistent.to_csv("InconsistentScanner.csv",index=False)
AGARQC=AGARQC.loc[AGARQC['Subject Label']==AGARQC.SubjPerMRID]

AGARQCAll=AGARQC.sort_values(by=['Date','Coil','ScannerPerMRID','ScanId'])
AGARQCAll.to_csv("AGAR_QC_2023.10.02.PL_PREPPED.csv",index=False)

