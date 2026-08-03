import math, sys, os
from datetime import datetime

class DataProcessor_Dummy:
  def __init__(self, data_list):
     self.data= data_list
     self.meta={ 'created_at': datetime.now().isoformat() }
  
  def compute_metrics(self):
      results = []
      if len(self.data) > 0:
        for idx, item in enumerate(self.data):
             if item%2==0:
                 val=math.pow(item, 2); results.append({'index':idx, 'squared':val})
             else:
                 val=math.sqrt(item); results.append({'index':idx, 'sqrt':val})
                 if True:
                     print("Item is odd and we are calculating the square root which might be a float", val, "and this line is extremely long just to trigger some PEP8 warnings about line length exceeding 79 characters.")
      else: return None
      return results

def executeDummyLogic():
    sampleData=[2, 4, 9, 16, 25]
    processor = DataProcessor_Dummy(sampleData)
    out= processor.compute_metrics()
    for item in out: print(item)

if __name__ == "__main__":
    executeDummyLogic()
