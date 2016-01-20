# -*- coding: utf-8 -*-
"""
Created on Tue Sep 01 16:10:54 2015

@author: z078739
"""
check=pd.read_csv("C:\Users\z078739\Downloads\prelimcouponresultsept.csv",sep="\t")
check=check.drop(["Rating","COUPON_ID_hash","coupon_number"],1)
coupon_merging=pd.read_csv("C:\Users\z078739\Downloads\coupon_merging.csv")
check_final=pd.merge(check,coupon_merging,on=["coupon"])
check_final=check_final.drop("coupon",1)
check_final1=check_final.sort(["USER_ID_hash"],ascending=True)
check1=(check_final1.groupby("USER_ID_hash").apply(lambda x:x["PURCHASED_COUPONS"].tolist()).reset_index())
check2=pd.DataFrame(check1[0].tolist(),)
check1=check1.drop(0,axis=1)
final=pd.concat([check1,check2],axis=1)
final1=final.drop("USER_ID_hash",1)
final2=pd.DataFrame()
final2["new_col"]=final1.apply(lambda x: ','.join(x.dropna().values.tolist()), axis=1)
writer=pd.ExcelWriter("C:\Users\z078739\Downloads\coupontran.xlsx",engine="xlsxwriter")
final2.to_excel(writer,sheet_name="sheet1")
writer.save()
"""
Code for converting Japense charachter in default format to actual format 
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
writer=pd.ExcelWriter("C:\Users\z078739\Downloads\coupontext1.xlsx",engine="xlsxwriter")
old_coupon.to_excel(writer,sheet_name="Sheet1")
writer.save()
