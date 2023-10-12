import pandas as pd

#read the data into a pandas dataframe
csvfile="/Users/petralenzini/work/datarequests/AGAR_QC/AGAR_QC_2023.10.02.csv";
AGARQC=pd.read_csv(csvfile)
AGARQC=AGARQC.drop(columns=['Subject'])#Default 'Subject' variable is in form of IntraDB UID;

#rename some columns
renamefields={'MR ID':'MR_ID','MR Date':'Date','stat_snr':'SNR','stat_mean':'mean','stat_stddev':'std','AGAR_SFNR':'tSNR','Subject Label':'Subject','Scanner':'Station'}
AGARQC=AGARQC.rename(columns=renamefields).copy()

# Add variable with more intuitive 'Scanner' name
AGARQC.loc[AGARQC.Station=='AWP166158','Scanner'] = 'Bay1'
AGARQC.loc[AGARQC.Station=='AWP166038','Scanner'] = 'Bay2'
AGARQC.loc[AGARQC.Station=='MRC35177','Scanner'] = 'Bay3'

# Drop Subject = CereSphere entries
AGARQC = AGARQC.loc[AGARQC.Subject != 'CereSphere']

# Assumed form of MR_ID is: AGAR_<id>_{20,32,64}chBay{1,2,3}_YYYYMMDD
# Extract some additional variables
AGARQC['SubjPerMRID']=AGARQC['MR_ID'].str.split("_",expand=True)[0]+'_'+AGARQC['MR_ID'].str.split("_",expand=True)[1]#cats(scan(MR_ID,1,'_'),'_',scan(MR_ID,2,'_'));
AGARQC['Coil']=AGARQC['MR_ID'].str.split("_",expand=True)[2]#scan(MR_ID,3,'_'); ** Have to trust that Coil portion of MR_ID was entered correctl

AGARQC['ScannerPerMRID']=AGARQC['Coil'].str[4:] #substr(Coil,5);
AGARQC['Coil']=AGARQC['Coil'].str[0:4]#Coil = substr(Coil,1,4);

# If order of AGAR_<id> was swapped when entering Session ID, fix it here
AGARQC.loc[AGARQC.SubjPerMRID=='ABCD_AGAR07','SubjPerMRID'] = 'AGAR_ABCD07'

# List the cases where either Subject or SubjPerMRID are not 'AGAR_ABCD07'
exclude = (AGARQC.Subject != 'AGAR_ABCD07') | (AGARQC.SubjPerMRID != 'AGAR_ABCD07')
print('Cases with either Subject or SubjPerMRID not equal to AGAR_ABCD07 (to be excluded):')
AGARQC[exclude]
# And having listed those, now exclude them
AGARQC = AGARQC.loc[~exclude]

# List instances were Coil doesn't match expectation
print('Cases where derived Coil variable is not 20ch, 32ch, or 64ch (to be excluded):')
AGARQC[~AGARQC['Coil'].isin(['20ch','32ch','64ch'])]
# And them exclude them
AGARQC = AGARQC.loc[AGARQC['Coil'].isin(['20ch','32ch','64ch'])]

# Check what we have for ScannerPerMRID
# There will be some with empty string, since old sessions did not embed Scanner info into the MR_ID
# But we know the Scanner from the Station field (in the DICOM) so don't need to do any subsetting of
# the data here
AGARQC.ScannerPerMRID.unique()
ind=AGARQC[AGARQC.ScannerPerMRID == ''].index
AGARQC.iloc[ind]

#format date as decimal year for plotting
AGARQC['Date']=pd.to_datetime(AGARQC.Date)
AGARQC['DateDec']=AGARQC.Date.dt.year + (AGARQC.Date.dt.dayofyear -1)/365

# At this point we should have the data prepped
AGARQCAll=AGARQC.sort_values(by=['Date','Coil','Scanner','ScanId'])
AGARQCAll.to_csv("/Users/petralenzini/work/datarequests/AGAR_QC/AGAR_QC_2023.10.11.PL_PREPPED.csv",index=False)



