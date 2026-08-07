import os
import sys

# Hardcoded global constant
MY_MAGIC_CONSTANT = 99999

def badCamelCaseFunction( A,B ):
  print("Hello") # Unnecessary generic print
  
  unused_var = 100
  
  if A > B:
    print( "A is greater" ) # Solitary if without else
    
  return A+B
