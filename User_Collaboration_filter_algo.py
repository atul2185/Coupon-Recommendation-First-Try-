# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:45:22 2015

@author: z078739
"""

import pandas as pd
from math import sqrt
user=pd.read_csv("C:\\Users\\z078739\\Downloads\\Coupon Prediction\\coupon_visit_train.csv")
user=user.drop(["I_DATE","PAGE_SERIAL","REFERRER_hash","SESSION_ID_hash","PURCHASEID_hash"],1)
user=user[["USER_ID_hash","VIEW_COUPON_ID_hash","PURCHASE_FLG"]]
def recur_dictify(frame):
    if len(frame.columns) == 1:
        if frame.values.size == 1: return frame.values[0][0]
        return frame.values.squeeze()
    grouped = frame.groupby(frame.columns[0])
    d = {k: recur_dictify(g.ix[:,1:]) for k,g in grouped}
    return d
group=user.groupby(["USER_ID_hash","VIEW_COUPON_ID_hash"]).sum()
df=group.reset_index()
def change(row):
    if row["PURCHASE_FLG"]==0:
        return 1
    elif row["PURCHASE_FLG"]==1:
        return 2
    else:
        return 3
df["PURCHASE"]=df.apply(lambda row:change (row),axis=1)
df=df.drop("PURCHASE_FLG",1)
dict1=recur_dictify(df)

def sim_pearson(prefs,p1,p2):
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    n=len(si)
    if n==0: return 0
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    sum1sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2sq=sum([pow(prefs[p2][it],2) for it in si])
    psum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
    num=psum-(sum1*sum2/n)
    den=sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
    if den==0: return 0
    r=num/den
    return r
    
def sim_distance(prefs,person1,person2):
   si={}
   for item in prefs[person1]:
       if item in prefs[person2]:
          si[item]=1
   if len(si)==0: return 0

   sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                       for item in prefs[person1] if item in prefs[person2]])
   return 1/(1+sum_of_squares)
def topmatches(prefs,person,n=10,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
               for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]
sample=pd.read_csv("C:\\Users\\z078739\\Downloads\\sample_submission1.csv")
#sample1=sample[sample.USER_ID_hash !="0596477fcb70cc48e4ffae2e3c25143d"]
#sample2=sample1[sample1.USER_ID_hash !="07919377d3368ca9c3868a48f3470444"]
#sample3=sample2[sample2.USER_ID_hash!="0aa3ad3ad9f8f5455d94d10f711f340c"]

def getrecommendations(prefs,similarity=sim_pearson):
    w=pd.DataFrame()
    for index,row in sample.iterrows():
        person=row["USER_ID_hash"]
        totals={}
        simsums={}
        for other in prefs:
            if other==person: continue
            sim=similarity(prefs,person,other)
            if sim<=0: continue
            for item in prefs[other]:
                if item not in prefs[person] or prefs[person][item]==0:
                    totals.setdefault(item,0)
                    totals[item]+=prefs[other][item]*sim
                    simsums.setdefault(item,0)
                    simsums[item]+=sim
        rankings=[(person,total/simsums[item],item) for item,total in totals.items()]
        rankings=[(i,j,k) for i,j,k in rankings if j>=3]
        rankings.sort()
        rankings.reverse()
        name=pd.DataFrame(rankings)
        w=w.append(name)
    return w
user_recomendation=getrecommendations(dict1)
import itertools as it
user_recom=pd.read_csv("C:\\Users\\z078739\\Downloads\\user_recomendation_sept.csv",sep="\t")
user_recom.columns=["User_Id","Rating","COUPON_ID_hash"]
couponsimilar=pd.read_csv("C:\\Users\\z078739\\Downloads\\Coupon Prediction\\Result\\CouponSimilarity50.csv",sep="\t")
couponsimilar2=list(it.chain(*couponsimilar.values))
couponsimilar3=pd.DataFrame(couponsimilar2)
combinecoupon=pd.read_csv("C:\\Users\\z078739\\Downloads\\couponcombine1.csv")
couponsimilar4=pd.concat([couponsimilar3,combinecoupon],axis=1)
couponsimilar4.columns=["coupon_number","coupon"]
coupon_test_train=pd.read_csv("C:\\Users\\z078739\\Downloads\\Coupon Prediction\\combined_coupons_test_train.csv")
coupon_test_train=coupon_test_train.ix[:,23:]
user_recom_coupon=pd.merge(user_recom,coupon_test_train,on=["COUPON_ID_hash"])
check23=pd.merge(user_recom_coupon,couponsimilar4,on=["coupon_number"])
check23.to_csv("C:\Users\z078739\Downloads\prelimcouponresultsept.csv",sep="\t",index=False)
#check=pd.read_csv("C:\Users\z078739\Downloads\prelimcouponresultsept.csv",sep="\t")
#coupon_merging=pd.read_csv("C:\Users\z078739\Downloads\coupon_merging.csv")
#check_final=pd.merge(check,coupon_merging,on=["coupon"])
#check_final=check_final.drop("coupon",1)
#check_final.columns=["USER_ID_hash","PURCHASED_COUPONS"]
#check_final1=check_final.sort(["USER_ID_hash"],ascending=True)
"""
Unique User
"""
check34=pd.unique(check23.User_Id.ravel())
check45=pd.DataFrame(check34)
check56=check45.sort(["USER_ID_hash"],ascending=True)
check56.to_csv("C:\Users\z078739\Downloads\uniqueuser.csv",sep="\t",index=False)










"""
Below Code only for generating Cartesian Product
"""
user_recom_coupon_1=user_recom_coupon_1.set_index([[0]*len(user_recom_coupon_1)])
couponsimilar1=couponsimilar1.set_index([[0]*len(couponsimilar1)])
cartesian=user_recom_coupon_1.join(couponsimilar1,how="outer")
cartesian=cartesian.drop(["Rating","COUPON_ID_hash"],1)
cartesian["coupon_coupon1"]=cartesian["coupon_number"]-cartesian["Coupon1"]
cartesian["coupon_coupon28"]=cartesian["coupon_number"]-cartesian["Coupon28"]
cartesian[cartesian.coupon_coupon28==0]



