import pandas as pd
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

print("control:")
bsub['control']=0
bsub.loc[(bsub.x2090_2_0 == 0) & (bsub.x2100_2_0 == 0) & (bsub.x4598_2_0 == 0) & (bsub.x4631_2_0 == 0),'control']=1
print(bsub.control.value_counts())

print("Single episode probable MDD:")
bsub['SEPMDD']=0
bsub.loc[((bsub.x4598_2_0 == 1) & (bsub.x4609_2_0 >= 2) & (bsub.x4620_2_0 == 1) & ((bsub.x2090_2_0 ==1) | (bsub.x2100_2_0 == 1)))
         |
         ((bsub.x4631_2_0 ==1) & (bsub.x5375_2_0 >=2) & (bsub.x5386_2_0 ==1) & ((bsub.x2090_2_0 ==1) | (bsub.x2100_2_0==1))),'SEPMOD']=1
print(bsub.SEPMDD.value_counts())

print("Reccurent moderate probable MDD:")
bsub['RMPMDD']=0
bsub.loc[((bsub.x4598_2_0 == 1) | (bsub.x4631_2_0 == 1)) & ((bsub.x4620_2_0 >= 2) | (bsub.x5386_2_0 >= 2)) & ((bsub.x4609_2_0 >= 2) | (bsub.x5375_2_0 >=2)) & (bsub.x2090_2_0 == 1) & (bsub.x2100_2_0 != 1),'RMPMDD']=1
print(bsub.RMPMDD.value_counts())

print("Reccurent severe probable MDD:")
bsub['RSPMDD']=0
bsub.loc[((bsub.x4598_2_0 == 1) | (bsub.x4631_2_0 == 1)) &
         ((bsub.x4620_2_0 >= 2) | (bsub.x5386_2_0 >= 2)) &
         ((bsub.x4609_2_0 >= 2) | (bsub.x5375_2_0 >= 2)) &
         (bsub.x2100_2_0 == 1),"RSPMDD"]=1
print(bsub.RSPMDD.value_counts())


