import numpy as np
cimport numpy as np
from time import time
cdef extern from "move.c":
    int move_func(int *,int,int,int,int)
cdef extern from "withdrawal.c":
    int withdrawal_func(int *,int,int,int,int *,int)

def call_move_func(np.ndarray[np.int32_t, ndim=2] date,loc,pos,pov):
    cdef:
        int loc_x,loc_y,pos_x,pos_y
    start=time()
    loc_x=loc[0]-pov[0]
    loc_y=loc[1]-pov[1]
    pos_x=pos[0]-pov[0]
    pos_y=pos[1]-pov[1]
    cdef int[:] date_list1= date[pov[0]:pov[0]+900, pov[1]:pov[1]+900].ravel()
    print(" ",time()-start)
    start=time()
    num=move_func(&date_list1[0],loc_x,loc_y,pos_x,pos_y)
    print(" ",time()-start)
    start=time()
    lis=[]
    if num>0:
        lis=np.flipud(np.array(date_list1[:num*2]).reshape(-1,2))
        print(lis)
        ind=len(lis)-1
        while ind>0:
            lis[ind][0]-=lis[ind-1][0]
            lis[ind][1]-=lis[ind-1][1]
            ind-=1
        lis[0][0]-=loc_x
        lis[0][1]-=loc_y
    print(lis)
    #print(num)
    print(" ",time()-start)
    return list(lis)

def call_withdrawal_fnuc(np.ndarray[np.int32_t, ndim=2] date2,loc,np.ndarray[np.int32_t, ndim=2] out,int i):
    cdef:
        int loc_x,loc_y,y_lan
        int n
    n=0
    start=time()
    loc_x=loc[0]
    loc_y=loc[1]
    y_lan=date2.shape[0]
    cdef int[:] date_list2= date2.ravel()
    cdef int[:] outli = out.ravel()
    print(" ",time()-start)
    start=time()
    num=withdrawal_func(&date_list2[0],y_lan,loc_x,loc_y,&outli[0],i)
    print(" ",time()-start)
    start=time()
    lis=[]
    if num>0:
        lis=np.flipud(np.array(date_list2[:num*2]).reshape(-1,2))
        print(lis)
        ind=len(lis)-1
        while ind>0:
            lis[ind][0]-=lis[ind-1][0]
            lis[ind][1]-=lis[ind-1][1]
            ind-=1
        lis[0][0]-=loc_x
        lis[0][1]-=loc_y
    print(lis)
    #print(num)
    print(" ",time()-start)
    return list(lis)
