import pandas as pd
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 14)

outdir='/Users/petralenzini/work/datarequests/kayla2023a/'
#These two files should be reachable by you via /home/plenzini/ on the chpc.  Let me know if you can't find them.
a=pd.read_csv('/Users/petralenzini/chpc3/datarequests/kayla/Vars19April24_ses-01.csv')
v=pd.read_csv('/Users/petralenzini/chpc3/datarequests/kayla/varlist19April23_ses-01_revised.txt',header=None)

#just changing some variable names
kvars = [w.replace('-', '_') for w in list(v[0])]
kvars2 = ["x"+w.replace('.', '_') for w in kvars]
varlist=['eid']+kvars2
a.columns=varlist

a1=varlist[1:13]
a2=['x20532_0_0', 'x4631_2_0', 'x20446_0_0', 'x4598_2_0','x21003_2_0']
keeplist=a1+a2

#remove missing values.  You'll want to extend this to isna() and negatives
bsub=a.copy()
print('orig count:',bsub.shape[0])
for i in keeplist:
    bsub=bsub.loc[bsub[i].isnull()==False]
    print(i,":",bsub.shape[0])
bsub=bsub.drop_duplicates(subset='eid').copy()



#THIS IS WHERE YOU WOULD WANT TO DROP ANY SUBJECT IN THE LIST ATTACHED TO THE GENERAL CHANNEL
#actually nevermind.  There aren't any people who withdrew in our sample.
withdrawns="/Users/petralenzini/work/McDonnell/datas/w47267_2023-04-25.csv"
wd=list(pd.read_csv(withdrawns,header=None)[0])
bsub=bsub.loc[~(bsub.eid.isin(wd))]
bsub.to_csv(outdir+"AllSubjectsCovariates4KaylaLuca_30May2023.csv",index=False)
################

print("final count:",bsub.shape[0])

############################################################################
#BREAK IT DOWN - get some Ns
print("control:")
bsub['control']=0
bsub.loc[(bsub.x2090_2_0 == 0) & (bsub.x2100_2_0 == 0) & (bsub.x4598_2_0 == 0) & (bsub.x4631_2_0 == 0),'control']=1
print(bsub.control.value_counts())
bsub.loc[bsub.control==1][['eid']].to_csv(outdir+'Controls.csv',index=False)

############################################################################

print("Single episode probable MDD:")
bsub['SEPMDD']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 == 1) & ((bsub.x2090_2_0 == 1) | (bsub.x2100_2_0 == 1)))
         |
         ((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 == 1) & ((bsub.x2090_2_0 == 1) | (bsub.x2100_2_0 == 1))),'SEPMDD']=1

bsub['SD']=0
bsub['SA']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 == 1) & ((bsub.x2090_2_0 == 1) | (bsub.x2100_2_0 == 1))),"SD"]=1
bsub.loc[((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 == 1) & ((bsub.x2090_2_0 == 1) | (bsub.x2100_2_0 == 1))),"SA"]=1

#####################################################################

print("Reccurent moderate probable MDD:")
bsub['RMPMDD']=0

bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 >=2) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 == 0))
         |
         ((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 >=2) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 == 0)),'RMPMDD']=1
print(bsub.RMPMDD.value_counts())

bsub['RMD']=0
bsub['RMA']=0

bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 >=2) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 == 0)),"RMD"]=1
bsub.loc[((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 >=2) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 == 0)),'RMA']=1

############################################################################
print("Reccurent severe probable MDD:")
bsub['RSPMDD']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 >=2) & (bsub.x2100_2_0 ==1))
         |
         ((bsub.x4631_2_0 ==1) & (bsub.x5375_2_0 >=2) & (bsub.x5386_2_0 >=2) & (bsub.x2100_2_0 ==1) ),'RSPMDD']=1

bsub['RSD']=0
bsub['RSA']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 >=2) & (bsub.x2100_2_0 ==1)),'RSD']=1
bsub.loc[((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 >=2) & (bsub.x2100_2_0 ==1)),'RSA']=1

############################################################################

#COUNTS
print(bsub.SEPMDD.value_counts())
print(bsub.SD.value_counts())
print(bsub.SA.value_counts())

print(bsub.RMPMDD.value_counts())
print(bsub.RMD.value_counts())
print(bsub.RMA.value_counts())
print("RMA AND RMD CROSSTAB",pd.crosstab(bsub.RMA, columns=bsub.RMD))

print(bsub.RSPMDD.value_counts())
print(bsub.RSD.value_counts())
print(bsub.RSA.value_counts())
print("RSD AND RSA CROSSTAB",pd.crosstab(bsub.RSD, columns=bsub.RSA))

#RSMDD and RMPMDD together
bsub.loc[(bsub.RSPMDD==1) | (bsub.RMPMDD==1)][['eid']].to_csv(outdir+"ModerateOrSevere.csv",index=False)


#QCS
print("SEPMDD AND RMPMDD CROSSTAB",pd.crosstab(bsub.SEPMDD, columns=bsub.RMPMDD))
print("SEPMDD AND RSPMDD CROSSTAB",pd.crosstab(bsub.SEPMDD, columns=bsub.RSPMDD))
pd.crosstab(bsub.RMPMDD, columns=bsub.RSPMDD)

c=['x2090_2_0', 'x2100_2_0', 'x4598_2_0', 'x4609_2_0', 'x4620_2_0', 'x4631_2_0', 'x5375_2_0', 'x5386_2_0','control', 'SD','SA','RMD','RMA','RSA','RSD','SEPMDD', 'RMPMDD', 'RSPMDD']
qc=bsub[c]
check=qc.loc[(qc.SEPMDD==1) & (qc.RMPMDD==1)][['SD','SA','RMD','RMA']]
print(pd.crosstab(check.SA,check.RMA))
print(pd.crosstab(check.SD,check.RMD))
print(pd.crosstab(check.SD,check.RMA))
print(pd.crosstab(check.SA,check.RMD))


check2=qc.loc[(qc.SD==1) & (qc.RMPMDD==1)][['SD','SA','RMD','RMA','RMPMDD','RSA','RSD']]
print(pd.crosstab(check2.SD,check2.RMPMDD))
check2=qc.loc[(qc.SA==1) & (qc.RMPMDD==1)]
print(pd.crosstab(check2.SA,check2.RMPMDD))

check3=qc.loc[(qc.SEPMDD==1) & (qc.RSPMDD==1)][['SD','SA','RSD','RSA']]
print(pd.crosstab(check3.SA,check3.RSA))
print(pd.crosstab(check3.SD,check3.RSD))
print(pd.crosstab(check3.SD,check3.RSA))
print(pd.crosstab(check3.SA,check3.RSD))
