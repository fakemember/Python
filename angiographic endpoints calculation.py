# -*- coding: utf-8 -*-
"""
Created on Sun May 17 09:33:09 2020

@author: CHAO
"""


#****************************************validation TVAL***************#

import pandas as pd
import numpy as np


angiocore=pd.read_excel('angiocore.xlsx')
revascpost=pd.read_excel('Revascpost.xlsx')
angiocore=angiocore[angiocore.PROCDATE.notna()]

angiocore.columns



UNSCHTLR=angiocore[(angiocore.VISITID==120) & (angiocore.FUTLR=='Y')]
UNSCHTLR

SUBLIST=angiocore[angiocore.SUBNUM.isin(UNSCHTLR.SUBNUM.unique())]

SUBLIST=SUBLIST.sort_values(['SUBNUM','VISITID','PROCDATE'])
 
SUBNUM=SUBLIST.drop_duplicates(['SUBNUM','VISITID'])

SUBLIST=SUBLIST[['SUBNUM','VISITID','PROCDATE']]

SUBLIST=SUBLIST[SUBLIST.VISITID!=30]



SUBLIST=SUBLIST.pivot(index='SUBNUM',columns='VISITID',values='PROCDATE')


unschelist=SUBLIST[(SUBLIST[70].isna() & SUBLIST[120].notna())|(SUBLIST[70]>SUBLIST[120])].index
unschelist=pd.Series(unschelist)



###create fu visit and earliest unscheduled visit with TLR
fu1=angiocore[angiocore.SUBNUM.isin(unschelist) & (angiocore.VISITID==120)]

fu2=angiocore[(~angiocore.SUBNUM.isin(unschelist)) & (angiocore.VISITID==70)]

fu=pd.concat([fu1,fu2],axis=0)  #fulist

fu=fu[['SUBNUM','VIEW1FU','VIEW2FU','TVAFUV1','TVAFUV2']]

fu['VIEW1FU']=fu.VIEW1FU.str.upper()
fu['VIEW1FU']=fu.VIEW1FU.str.split(expand=True)[0]

fu.loc[fu.VIEW1FU=='APVIEW','VIEW1FU']='AP'

fu['VIEW2FU']=fu.VIEW2FU.str.upper()
fu['VIEW2FU']=fu.VIEW2FU.str.split(expand=True)[0]


a=revascpost.columns[revascpost.columns.str.startswith('DEVICERULER')]
b=revascpost.columns[revascpost.columns.str.startswith('DIST')]
c=revascpost.columns[revascpost.columns.str.startswith('PROX')]
d=revascpost.columns[revascpost.columns.str.startswith('SUBNUM')]
ruler=revascpost[a.append(b).append(c).append(d)]


ruler=ruler.drop(revascpost.columns[revascpost.columns.str.endswith('DEC')&revascpost.columns.str.startswith('DEVICERULER')],axis=1)


baseline=angiocore[angiocore.VISITID==30]




p1=pd.merge(ruler,baseline,on='SUBNUM',how='inner')

p1=p1[['DEVICERULER1','DEVICERULER2','DEVICERULER3','DEVICERULER4',
'DISTMARKRBND1','DISTMARKRBND2','DISTMARKRBND3','DISTMARKRBND4','PROXMARKRBND1',
'PROXMARKRBND2','PROXMARKRBND3','PROXMARKRBND4','SUBNUM','LESNSTART','LESNEND']]

p1=p1[revascpost.NOREVASCPOST!='X']

p1.loc[p1.DEVICERULER1==1,'DISTMARKRBND1']=-p1.loc[p1.DEVICERULER1==1,'DISTMARKRBND1']
p1.loc[p1.DEVICERULER2==1,'DISTMARKRBND2']=-p1.loc[p1.DEVICERULER2==1,'DISTMARKRBND2']
p1.loc[p1.DEVICERULER3==1,'DISTMARKRBND3']=-p1.loc[p1.DEVICERULER3==1,'DISTMARKRBND3']
p1.loc[p1.DEVICERULER4==1,'DISTMARKRBND4']=-p1.loc[p1.DEVICERULER4==1,'DISTMARKRBND4']

p1.loc[p1.DEVICERULER1==1,'PROXMARKRBND1']=-p1.loc[p1.DEVICERULER1==1,'PROXMARKRBND1']
p1.loc[p1.DEVICERULER2==1,'PROXMARKRBND2']=-p1.loc[p1.DEVICERULER2==1,'PROXMARKRBND2']
p1.loc[p1.DEVICERULER3==1,'PROXMARKRBND3']=-p1.loc[p1.DEVICERULER3==1,'PROXMARKRBND3']
p1.loc[p1.DEVICERULER4==1,'PROXMARKRBND4']=-p1.loc[p1.DEVICERULER4==1,'PROXMARKRBND4']

c1=(p1[['DISTMARKRBND1','PROXMARKRBND1']].apply(np.max,axis=1)<p1['LESNSTART'] )|(p1[['DISTMARKRBND1','PROXMARKRBND1']].apply(np.min,axis=1)>p1['LESNEND'] )

c2=(p1[['DISTMARKRBND2','PROXMARKRBND2']].apply(np.min,axis=1)>p1.LESNEND )|(p1[['DISTMARKRBND2','PROXMARKRBND2']].apply(np.max,axis=1)<p1.LESNSTART )

c3=(p1[['DISTMARKRBND3','PROXMARKRBND3']].apply(np.min,axis=1)>p1.LESNEND )|(p1[['DISTMARKRBND3','PROXMARKRBND3']].apply(np.max,axis=1)<p1.LESNSTART )

c4=(p1[['DISTMARKRBND4','PROXMARKRBND4']].apply(np.min,axis=1)>p1.LESNEND )|(p1[['DISTMARKRBND4','PROXMARKRBND4']].apply(np.max,axis=1)<p1.LESNSTART )


condiall=(p1.DEVICERULER1.notna() &  ~c1) |(p1.DEVICERULER2.notna() &  ~c2 )|(p1.DEVICERULER3.notna() &  ~c3 )|(p1.DEVICERULER4.notna() &  ~c4)


###Post-Infusion Revascularization was performed within the Target Lesion
finalviewlist1=p1.loc[condiall,'SUBNUM']

prebfview=baseline[~baseline.SUBNUM.isin(finalviewlist1)]
temp=prebfview[['SUBNUM','TVAPREBFV1','TVAPREBFV2','VIEW1PREBF','VIEW2PREBF']]

#finalviewlist2=prebfview.loc[(temp.VIEW1PREBF=='NOT') & (temp.VIEW2PREBF=='NOT'),'SUBNUM']



##baseline PREBF subjects 
#PREBF=angiocore[(angiocore.VISITID==30) & (~angiocore.SUBNUM.isin(finalviewlist1.append(finalviewlist2)))]
PREBF=angiocore[(angiocore.VISITID==30) & (~angiocore.SUBNUM.isin(finalviewlist1))]


PREBF=PREBF[['SUBNUM','VIEW1PREBF','VIEW2PREBF','TVAPREBFV1','TVAPREBFV2']]

PREBF=PREBF.merge(fu,on='SUBNUM',how='inner')
PREBF['VIEW1PREBF']=PREBF.VIEW1PREBF.str.upper()
PREBF['VIEW2PREBF']=PREBF.VIEW2PREBF.str.upper()

PREBF.loc[PREBF.VIEW1PREBF=='AP','APPREBF']=PREBF.loc[PREBF.VIEW1PREBF=='AP','TVAPREBFV1']
PREBF.loc[PREBF.VIEW1PREBF=='LAT','LATPREBF']=PREBF.loc[PREBF.VIEW1PREBF=='LAT','TVAPREBFV1']

PREBF.loc[PREBF.VIEW2PREBF=='AP','APPREBF']=PREBF.loc[PREBF.VIEW2PREBF=='AP','TVAPREBFV2']
PREBF.loc[PREBF.VIEW2PREBF=='LAT','LATPREBF']=PREBF.loc[PREBF.VIEW2PREBF=='LAT','TVAPREBFV2']


PREBF.loc[PREBF.VIEW1FU=='AP','APFU']=PREBF.loc[PREBF.VIEW1FU=='AP','TVAFUV1']
PREBF.loc[PREBF.VIEW1FU=='LAT','LATFU']=PREBF.loc[PREBF.VIEW1FU=='LAT','TVAFUV1']

PREBF.loc[PREBF.VIEW2FU=='AP','APFU']=PREBF.loc[PREBF.VIEW2FU=='AP','TVAFUV2']
PREBF.loc[PREBF.VIEW2FU=='LAT','LATFU']=PREBF.loc[PREBF.VIEW2FU=='LAT','TVAFUV2']

###no matching view
finalviewlist3=PREBF.SUBNUM[(PREBF.APPREBF.isna() | PREBF.APFU.isna()) & (PREBF.LATPREBF.isna() | PREBF.LATFU.isna())]

#finalviewlist=finalviewlist1.append(finalviewlist2).append(finalviewlist3).sort_values()

finalviewlist=finalviewlist1.append(finalviewlist3).sort_values()


PREBF=PREBF[~PREBF.SUBNUM.isin(finalviewlist)]


finalview=angiocore.loc[(angiocore.VISITID==30 )& angiocore.SUBNUM.isin(finalviewlist),['VIEW1POST','VIEW2POST','SUBNUM','TVAPOSTV1','TVAPOSTV2']]
finalview=finalview.merge(fu,on='SUBNUM',how='inner')

finalview.loc[finalview.VIEW1POST=='AP','APPREBF']=finalview.loc[finalview.VIEW1POST=='AP','TVAPOSTV1']
finalview.loc[finalview.VIEW1POST=='LAT','LATPREBF']=finalview.loc[finalview.VIEW1POST=='LAT','TVAPOSTV1']

finalview.loc[finalview.VIEW2POST=='AP','APPREBF']=finalview.loc[finalview.VIEW2POST=='AP','TVAPOSTV2']
finalview.loc[finalview.VIEW2POST=='LAT','LATPREBF']=finalview.loc[finalview.VIEW2POST=='LAT','TVAPOSTV2']

finalview.loc[finalview.VIEW1FU=='AP','APFU']=finalview.loc[finalview.VIEW1FU=='AP','TVAFUV1']
finalview.loc[finalview.VIEW1FU=='LAT','LATFU']=finalview.loc[finalview.VIEW1FU=='LAT','TVAFUV1']

finalview.loc[finalview.VIEW2FU=='AP','APFU']=finalview.loc[finalview.VIEW2FU=='AP','TVAFUV2']
finalview.loc[finalview.VIEW2FU=='LAT','LATFU']=finalview.loc[finalview.VIEW2FU=='LAT','TVAFUV2']


finalview=finalview[~((finalview.APPREBF.isna() | finalview.APFU.isna()) & (finalview.LATPREBF.isna() | finalview.LATFU.isna()))]




PREBF=PREBF[['SUBNUM','APPREBF', 'LATPREBF'  ,  'APFU'  , 'LATFU']]

finalview=  finalview[['SUBNUM','APPREBF', 'LATPREBF'  ,  'APFU'  , 'LATFU']]

TVAL=pd.concat([PREBF,finalview],axis=0  )

condition1=~TVAL.isna().apply(any,axis=1)
TVAL.loc[condition1,'baseline']=TVAL.loc[condition1,['APPREBF', 'LATPREBF']].apply(np.mean,axis=1)
TVAL.loc[condition1,'fu']=TVAL.loc[condition1,['APFU'  , 'LATFU']].apply(np.mean,axis=1)

condition2=(~TVAL[['APPREBF','APFU']].isna().apply(any,axis=1))& ~condition1

TVAL.loc[condition2,'baseline']=TVAL.loc[condition2,'APPREBF']
TVAL.loc[condition2,'fu']=TVAL.loc[condition2,'APFU' ]

condition3=(~TVAL[['LATPREBF','LATFU']].isna().apply(any,axis=1))& ~condition1 &~condition2

TVAL.loc[condition3,'baseline']=TVAL.loc[condition3,'LATPREBF']
TVAL.loc[condition3,'fu']=TVAL.loc[condition3,'LATFU' ]

TVAL['TVAL']=1-TVAL.fu/TVAL.baseline


############################%Diameter Stenosis#########################
fu=pd.concat([fu1,fu2],axis=0)  #fulist
fu=fu[['SUBNUM','MLDFUVIEW1','MLDFUVIEW2','RVDFUV1','RVDFUV2']]

fu.loc[(fu.MLDFUVIEW1==0) |(fu.MLDFUVIEW2==0 ),'fu%DS']=1
fu.loc[fu.RVDFUV1=='NOT','RVDFUV1']=np.nan
fu.loc[fu.RVDFUV2=='NOT','RVDFUV2']=np.nan
fu['RVDFUV1']=pd.to_numeric(fu.RVDFUV1)
fu['RVDFUV2']=pd.to_numeric(fu.RVDFUV2)
fu.loc[~((fu.MLDFUVIEW1==0) |(fu.MLDFUVIEW2==0 )),'fu%DS1']=1-fu.MLDFUVIEW1/fu.RVDFUV1
fu.loc[~((fu.MLDFUVIEW1==0) |(fu.MLDFUVIEW2==0 )),'fu%DS2']=1-fu.MLDFUVIEW2/fu.RVDFUV2

fu.loc[~((fu.MLDFUVIEW1==0) |(fu.MLDFUVIEW2==0 )),'fu%DS']=fu.loc[~((fu.MLDFUVIEW1==0) |(fu.MLDFUVIEW2==0 )),['fu%DS1','fu%DS2']].apply(np.max,axis=1)

baseline=baseline.merge(revascpost[['SUBNUM','NOREVASCPOST']],on='SUBNUM',how='inner')

c1=baseline.SUBNUM.isin(finalviewlist1) 
c2=baseline.NOREVASCPOST!='X'
c3=baseline[['MLDVIEW1PREBF','MLDVIEW2PREBF']].isna().apply(all,axis=1)

finalds=baseline[(c1 & c2)|c3]
finalds.loc[(finalds.MLDVIEW1POST==0) |(finalds.MLDVIEW2POST==0 ),'fu%DS']=1
finalds.loc[~((finalds.MLDVIEW1POST==0) |(finalds.MLDVIEW2POST==0 )),'fu%DS1']=1-finalds.MLDVIEW1POST/finalds.RVDV1POST
finalds.loc[~((finalds.MLDVIEW1POST==0) |(finalds.MLDVIEW2POST==0 )),'fu%DS2']=1-finalds.MLDVIEW2POST/finalds.RVDV2POST
finalds.loc[~((finalds.MLDVIEW1POST==0) |(finalds.MLDVIEW2POST==0 )),'fu%DS']=finalds.loc[~((finalds.MLDVIEW1POST==0) |(finalds.MLDVIEW2POST==0 )),['fu%DS1','fu%DS2']].apply(np.max,axis=1)


prebfds=baseline[baseline.SUBNUM.isin(fu.SUBNUM[~fu.SUBNUM.isin(finalds.SUBNUM)])]

prebfds.loc[(prebfds.MLDVIEW1PREBF==0) |(prebfds.MLDVIEW2PREBF==0 ),'fu%DS']=1
prebfds.loc[~((prebfds.MLDVIEW1PREBF==0) |(prebfds.MLDVIEW2PREBF==0 )),'fu%DS1']=1-prebfds.MLDVIEW1PREBF/prebfds.RVDV1PREBF
prebfds.loc[~((prebfds.MLDVIEW1PREBF==0) |(prebfds.MLDVIEW2PREBF==0 )),'fu%DS2']=1-prebfds.MLDVIEW2PREBF/prebfds.RVDV2PREBF
prebfds.loc[~((prebfds.MLDVIEW1PREBF==0) |(prebfds.MLDVIEW2PREBF==0 )),'fu%DS']=prebfds.loc[~((prebfds.MLDVIEW1PREBF==0) |(prebfds.MLDVIEW2PREBF==0 )),['fu%DS1','fu%DS2']].apply(np.max,axis=1)

finalds=finalds[['SUBNUM','fu%DS']]
prebfds=prebfds[['SUBNUM','fu%DS']]

base=pd.concat([finalds,prebfds],axis=0)

fu=fu.merge(base,how='left',on='SUBNUM')

fu['%diameter stenosis']=fu['fu%DS_x']-fu['fu%DS_y']

################################late lumen loss########################3

fu=pd.concat([fu1,fu2],axis=0)  #fulist
fu=fu[['SUBNUM','VIEW1FU','VIEW2FU','MLDFUVIEW1','MLDFUVIEW2']]

fu['VIEW1FU']=fu.VIEW1FU.str.upper()
fu['VIEW1FU']=fu.VIEW1FU.str.split(expand=True)[0]

fu.loc[fu.VIEW1FU=='APVIEW','VIEW1FU']='AP'

fu['VIEW2FU']=fu.VIEW2FU.str.upper()
fu['VIEW2FU']=fu.VIEW2FU.str.split(expand=True)[0]



PREBF=angiocore[(angiocore.VISITID==30) & (~angiocore.SUBNUM.isin(finalviewlist1))]


PREBF=PREBF[['SUBNUM','VIEW1PREBF','VIEW2PREBF','MLDVIEW1PREBF','MLDVIEW2PREBF']]

PREBF=PREBF.merge(fu,on='SUBNUM',how='inner')
PREBF['VIEW1PREBF']=PREBF.VIEW1PREBF.str.upper()
PREBF['VIEW2PREBF']=PREBF.VIEW2PREBF.str.upper()

PREBF.loc[PREBF.VIEW1PREBF=='AP','APPREBF']=PREBF.loc[PREBF.VIEW1PREBF=='AP','MLDVIEW1PREBF']
PREBF.loc[PREBF.VIEW1PREBF=='LAT','LATPREBF']=PREBF.loc[PREBF.VIEW1PREBF=='LAT','MLDVIEW1PREBF']

PREBF.loc[PREBF.VIEW2PREBF=='AP','APPREBF']=PREBF.loc[PREBF.VIEW2PREBF=='AP','MLDVIEW2PREBF']
PREBF.loc[PREBF.VIEW2PREBF=='LAT','LATPREBF']=PREBF.loc[PREBF.VIEW2PREBF=='LAT','MLDVIEW2PREBF']


PREBF.loc[PREBF.VIEW1FU=='AP','APFU']=PREBF.loc[PREBF.VIEW1FU=='AP','MLDFUVIEW1']
PREBF.loc[PREBF.VIEW1FU=='LAT','LATFU']=PREBF.loc[PREBF.VIEW1FU=='LAT','MLDFUVIEW1']

PREBF.loc[PREBF.VIEW2FU=='AP','APFU']=PREBF.loc[PREBF.VIEW2FU=='AP','MLDFUVIEW2']
PREBF.loc[PREBF.VIEW2FU=='LAT','LATFU']=PREBF.loc[PREBF.VIEW2FU=='LAT','MLDFUVIEW2']

###no matching view
finalviewlist3=PREBF.SUBNUM[(PREBF.APPREBF.isna() | PREBF.APFU.isna()) & (PREBF.LATPREBF.isna() | PREBF.LATFU.isna())]

finalviewlist=finalviewlist1.append(finalviewlist3).sort_values()


PREBF=PREBF[~PREBF.SUBNUM.isin(finalviewlist)]


finalview=angiocore.loc[(angiocore.VISITID==30 )& angiocore.SUBNUM.isin(finalviewlist),['VIEW1POST','VIEW2POST','SUBNUM','MLDVIEW1POST','MLDVIEW2POST']]
finalview=finalview.merge(fu,on='SUBNUM',how='inner')

finalview.loc[finalview.VIEW1POST=='AP','APPREBF']=finalview.loc[finalview.VIEW1POST=='AP','MLDVIEW1POST']
finalview.loc[finalview.VIEW1POST=='LAT','LATPREBF']=finalview.loc[finalview.VIEW1POST=='LAT','MLDVIEW1POST']

finalview.loc[finalview.VIEW2POST=='AP','APPREBF']=finalview.loc[finalview.VIEW2POST=='AP','MLDVIEW2POST']
finalview.loc[finalview.VIEW2POST=='LAT','LATPREBF']=finalview.loc[finalview.VIEW2POST=='LAT','MLDVIEW2POST']

finalview.loc[finalview.VIEW1FU=='AP','APFU']=finalview.loc[finalview.VIEW1FU=='AP','MLDFUVIEW1']
finalview.loc[finalview.VIEW1FU=='LAT','LATFU']=finalview.loc[finalview.VIEW1FU=='LAT','MLDFUVIEW1']

finalview.loc[finalview.VIEW2FU=='AP','APFU']=finalview.loc[finalview.VIEW2FU=='AP','MLDFUVIEW2']
finalview.loc[finalview.VIEW2FU=='LAT','LATFU']=finalview.loc[finalview.VIEW2FU=='LAT','MLDFUVIEW2']


finalview=finalview[~((finalview.APPREBF.isna() | finalview.APFU.isna()) & (finalview.LATPREBF.isna() | finalview.LATFU.isna()))]




PREBF=PREBF[['SUBNUM','APPREBF', 'LATPREBF'  ,  'APFU'  , 'LATFU']]

finalview=  finalview[['SUBNUM','APPREBF', 'LATPREBF'  ,  'APFU'  , 'LATFU']]

LLL=pd.concat([PREBF,finalview],axis=0  )

condition1=~LLL.isna().apply(any,axis=1)
LLL.loc[condition1,'baseline']=LLL.loc[condition1,['APPREBF', 'LATPREBF']].apply(np.mean,axis=1)
LLL.loc[condition1,'fu']=LLL.loc[condition1,['APFU'  , 'LATFU']].apply(np.mean,axis=1)

condition2=(~LLL[['APPREBF','APFU']].isna().apply(any,axis=1))& ~condition1

LLL.loc[condition2,'baseline']=LLL.loc[condition2,'APPREBF']
LLL.loc[condition2,'fu']=LLL.loc[condition2,'APFU' ]

condition3=(~TVAL[['LATPREBF','LATFU']].isna().apply(any,axis=1))& ~condition1 &~condition2

LLL.loc[condition3,'baseline']=LLL.loc[condition3,'LATPREBF']
LLL.loc[condition3,'fu']=LLL.loc[condition3,'LATFU' ]

LLL['LLL']=LLL.baseline-LLL.fu



