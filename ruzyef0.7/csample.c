#define AR 24
#define MA 99999.9
#define DE 100000000
#include <time.h>
#include "csample.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
struct pas
{
        int pos[2];
        float cost;
        float yte;
        struct pas *memo;
        
};
//[[0 if cldt.mu==em else (1 if cldt.plains==em else (2 if cldt.rail==em else (3 if cldt.road==em else(4 if cldt.woods==em else 6)))) for em in lis] for lis in date]
int cfunc(int *date,int wei,int hei,int loc_x,int loc_y,int pos_x,int pos_y){
    struct pas *sen;
    struct pas box;
    struct pas* mae,* usi,* sor,* ato;
    float cost=0.0,yte=99999.1,co;
    int tot_x,tot_y;
    int i,j;
    int nokori=1;
    float *map_dat;
    float *at;
    int *et;
    time_t t = time(NULL);
    map_dat=(float *)malloc(sizeof(float) * wei * hei);
    sen = (struct pas*)malloc(sizeof(struct pas) * DE);
    if(sen==NULL ||  map_dat==NULL)return -3;
    usi=mae=sen;
    at=map_dat;
    et=date;
    const int arry[AR][2]={{1,1},{-1,1},{1,-1},{-1,-1},{1,0},{-1,0},{0,1},{0,-1},
                        {3,1},{1,3},{-3,1},{-1,3},{3,-1},{1,-3},{-3,-1},{-1,-3},
                        {2,1},{1,2},{-2,1},{-1,2},{2,-1},{1,-2},{-2,-1},{-1,-2}};
    if(loc_x==pos_x&&loc_y==pos_y){
        free(sen);
        return -1;
    }
    for(i=0;i<hei*wei;i++){
        *map_dat=MA;
        map_dat++;
    }
    map_dat=at;
    mae->pos[0]=loc_x;
    mae->pos[1]=loc_y;
    mae->cost=cost;
    mae->yte=sqrtf(loc_x-pos_x*loc_x-pos_x+loc_y-pos_y*loc_y-pos_y);
    mae++;
    t=time(NULL);
    while(nokori>0){
        sor=usi;
        ato=usi;
        for(i=0;i<nokori-1;i++){
            usi++;
            if(sor->yte+sor->cost > usi->yte+usi->cost){
                sor=usi;
            }
            else if(sor->yte+sor->cost == usi->yte+usi->cost){
                if(sor->yte > usi->yte)sor=usi;
            }
        }
        usi=ato;
        if(usi!=sor){
            box=*sor;
            *sor=*usi;
            *usi=box;
        }
        tot_x=usi->pos[0];
        tot_y=usi->pos[1];
        cost=usi->cost;
        usi++;
        nokori--;
        //printf(" %d ",mae-sen);
        for(i=0;i<AR;i++){
            tot_x+=arry[i][0];
            tot_y+=arry[i][1];
            map_dat+=tot_x+tot_y*wei;
            date+=tot_x+tot_y*wei;
            co=1.0;
            if(*date==4)co=0.5;
            else if(*date==2)co=10.0;
            cost+=sqrtf(arry[i][1]*arry[i][1]+arry[i][0]*arry[i][0])*co;
            if(tot_x==pos_x && tot_y==pos_y){
                nokori=0;
                break;
            }// && *date!=2
            if(*map_dat>cost && *date!=0){
                *map_dat=cost*co;
                mae->pos[0]=tot_x;
                mae->pos[1]=tot_y;
                mae->cost=cost*co;
                mae->yte=sqrtf((tot_x-pos_x)*(tot_x-pos_x)+(tot_y-pos_y)*(tot_y-pos_y));
                mae->memo=usi-1;
                mae++;
                
                if(mae==sen+DE-1){
                    free(sen);
                    return -2;
                }
                nokori++;
            }
            cost-=sqrtf(arry[i][1]*arry[i][1]+arry[i][0]*arry[i][0])*co;
            tot_x-=arry[i][0];
            tot_y-=arry[i][1];

            map_dat=at;
            date=et;
        }
    }
    printf("|%f|", difftime(time(NULL),t));
    t=time(NULL);
    i=0;
    mae=usi-1;
    date=et;
    do{
        *date=mae->pos[0];
        date++;
        *date=mae->pos[1];
        date++;
        i++;
        mae=mae->memo;
    }while(mae != sen);
    free(sen);
    return i;
}