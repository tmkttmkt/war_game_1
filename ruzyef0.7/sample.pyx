# cython: boundscheck=False, wraparound=False
# cython: cdivision=True
cimport numpy as np
import numpy as np
from moz import cldt,henkan
from time import time
from math import sqrt 
cimport cython
def argo_move(date,loc,pos):
    cdef:
        int wei,hei
        int loc_x,loc_y,pos_x,pos_y
        int et
        list list_tes
    start=time()
    loc_x=loc[0]
    loc_y=loc[1]
    pos_x=pos[0]
    pos_y=pos[1]
    dat=[[0 if cldt.mu==em else (1 if cldt.plains==em else (2 if cldt.river==em else (3 if cldt.rail==em else (4 if cldt.road==em else (5 if cldt.woods==em else 6))))) for em in lis] for lis in date]
    wei=len(date[0])
    hei=len(date)
    cdef int[:]array=np.array(dat, dtype=np.int32).flatten()
    print(" ",time()-start)
    start=time()
    et=cfunc(&array[0],wei,hei,loc_x,loc_y,pos_x,pos_y)
    print(" ",time()-start)
    start=time()
    if(et>0):
        lis=np.array(array[:et*2]).reshape(-1,2)
        lis=lis[::-1]
        lis=np.append(lis, [pos], axis=0)
        lis=np.delete(lis,0,0)
        return lis
    return []

        