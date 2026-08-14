import os, sys,time

def MyBadFunction( a,b,   c ):
  x=10
  if x== 10: print('hello')
  return a+ b +c

class my_class :
    def __init__(self,name):self.name=name
    def doSomething( self ):
     for i in range(10):
        print( self.name )

myObj = my_class( "Test" )
myObj.doSomething()
MyBadFunction(1, 2,3)
