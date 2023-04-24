import pandas as pd
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 14)

a=pd.read_csv('/Users/petralenzini/chpc3/datarequests/kayla/Vars19April24_ses-01.csv')
v=pd.read_csv('/Users/petralenzini/chpc3/datarequests/kayla/varlist19April23_ses-01_revised.txt',header=None)

kvars = [w.replace('-', '_') for w in list(v[0])]
kvars2 = ["x"+w.replace('.', '_') for w in kvars]
varlist=['eid']+kvars2
a.columns=varlist

a1=varlist[1:13]
a2=['x20532_0_0', 'x4631_2_0', 'x20446_0_0', 'x4598_2_0','x21003_2_0']
keeplist=a1+a2

bsub=a.copy()
print('orig count:',bsub.shape[0])
for i in keeplist:
    bsub=bsub.loc[bsub[i].isnull()==False]
    print(i,":",bsub.shape[0])
bsub=bsub.drop_duplicates(subset='eid').copy()
print("final count:",bsub.shape[0])

############################################################################

print("control:")
bsub['control']=0
bsub.loc[(bsub.x2090_2_0 == 0) & (bsub.x2100_2_0 == 0) & (bsub.x4598_2_0 == 0) & (bsub.x4631_2_0 == 0),'control']=1
print(bsub.control.value_counts())

############################################################################

print("Single episode probable MDD:")
bsub['SEPMDD']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 == 1) & ((bsub.x2090_2_0 == 1) | (bsub.x2100_2_0 == 1)))
         |
         ((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 == 1) & ((bsub.x2090_2_0 == 1) | (bsub.x2100_2_0 == 1))),'SEPMDD']=1

#SEPARATE THE OR:
bsub['SD']=0
bsub['SA']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 == 1) & ((bsub.x2090_2_0 == 1) | (bsub.x2100_2_0 == 1))),"SD"]=1
bsub.loc[((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 == 1) & ((bsub.x2090_2_0 == 1) | (bsub.x2100_2_0 == 1))),"SA"]=1

#####################################################################

# New Reccurent moderate probable MDD:
print("Reccurent moderate probable MDD:")
bsub['RMPMDD']=0

bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 >=2) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 == 0))
         |
         ((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 >=2) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 == 0)),'RMPMDD']=1
print(bsub.RMPMDD.value_counts())

#separate out the parts of the OR:
bsub['RMD']=0
bsub['RMA']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 >=2) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 == 0)),"RMD"]=1
bsub.loc[((bsub.x4631_2_0 == 1) & (bsub.x5375_2_0 >= 2) & (bsub.x5386_2_0 >=2) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 == 0)),'RMA']=1

############################################################################
# NEW SEVERE
print("Reccurent severe probable MDD:")
bsub['RSPMDD']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 >=2) & (bsub.x2100_2_0 ==1))
         |
         ((bsub.x4631_2_0 ==1) & (bsub.x5375_2_0 >=2) & (bsub.x5386_2_0 >=2) & (bsub.x2100_2_0 ==1) ),'RSPMDD']=1
#separate out the parts of the OR:
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

print(bsub.RSPMDD.value_counts())
print(bsub.RSD.value_counts())
print(bsub.RSA.value_counts())

#QCS
print("SEPMDD AND RMPMDD CROSSTAB",pd.crosstab(bsub.SEPMDD, columns=bsub.RMPMDD))
print("SEPMDD AND RSPMDD CROSSTAB",pd.crosstab(bsub.SEPMDD, columns=bsub.RSPMDD))

pd.crosstab(bsub.RMPMDD, columns=bsub.RSPMDD)

#WHY is SEP overlapping with RMP and RSP?
c=['x2090_2_0', 'x2100_2_0', 'x4598_2_0', 'x4609_2_0', 'x4620_2_0', 'x4631_2_0', 'x5375_2_0', 'x5386_2_0','control', 'SD','SA','RMD','RMA','RSA','RSD','SEPMDD', 'RMPMDD', 'RSPMDD']
qc=bsub[c]
check=qc.loc[(qc.SEPMDD==1) & (qc.RMPMDD==1)][['SD','SA','RMD','RMA']]
pd.crosstab(check.SA,check.RMA)
pd.crosstab(check.SD,check.RMD)
pd.crosstab(check.SD,check.RMA)
pd.crosstab(check.SA,check.RMD)

check2=qc.loc[(qc.SD==1) & (qc.RMPMDD==1)][['SD','SA','RMD','RMA','RMPMDD','RSA','RSD']]
pd.crosstab(check2.SD,check2.RMPMDD)
check2=qc.loc[(qc.SA==1) & (qc.RMPMDD==1)]
pd.crosstab(check2.SA,check2.RMPMDD)

check3=qc.loc[(qc.SEPMDD==1) & (qc.RSPMDD==1)][['SD','SA','RSD','RSA']]
pd.crosstab(check3.SA,check3.RSA)
pd.crosstab(check3.SD,check3.RSD)
pd.crosstab(check3.SD,check3.RSA)
pd.crosstab(check3.SA,check3.RSD)
