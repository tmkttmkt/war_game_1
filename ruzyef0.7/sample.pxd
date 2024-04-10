

cdef extern from "csample.h":
    int cfunc(int *date,int wei,int hei,int loc_x,int loc_y,int pos_x,int pos_y)