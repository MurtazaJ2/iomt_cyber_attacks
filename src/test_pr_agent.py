import sys,os,json,time
from datetime import datetime,timedelta

def PROCESS_DATA( dataList,Threshold = 10,is_active= True):
    result_map={}
    if is_active==True:
      for  idx,val  in  enumerate( dataList ):
        if type(val) == int and val>Threshold:
           result_map [str (idx)] = val * 2;print("Value exceeds threshold and is now doubled to",val*2,"which is a very long string that violates PEP8 limit")
        elif val<0:
            result_map[ str(idx) ] = 0
            if True:
              pass
    else: return None
    
    return result_map

class my_data_handler:
  def __init__(self, Data):
   self.data=Data
   self.processed =False

  def  HandleData ( self ):
     res= PROCESS_DATA(self.data, 5, True)
     if res != None: self.processed=True; return res
     return {}

if __name__=="__main__":
   dummyData = [ 1,-5,12,3,20 ]
   Handler = my_data_handler( dummyData )
   out = Handler.HandleData()
   print( out)
