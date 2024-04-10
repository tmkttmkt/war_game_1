#include "pas.h"
#define HABA 600

int withdrawal_func(int * date,int y_lan,int loc_x,int loc_y,int *out,int n) {
    const int arry[16][2]={{1,1},{2,1},{1,2},
                        {-1,1},{-2,1},{-1,2},
                        {1,-1},{2,-1},{1,-2},
                        {-1,-1},{-2,-1},{-1,-2},
                        {1,0},{-1,0},{0,1},{0,-1},};
    int nokori=1;
    struct pas *sen;
    struct pas *naw,*new,*last;
    struct pas *top;
    float cost=0;
    float point_cost;
    int tot_x,tot_y;
    int i,m=0;
    float pos_x=0,pos_y=0;
    int *date_start=date;
    float *cost_map,*at_cost_map;
    double time1,time2;
    time1=(double)clock() / CLOCKS_PER_SEC;
    cost_map=(float *)malloc(sizeof(float) * (HABA+1) * (HABA+1));
    sen = (struct pas*)malloc(sizeof(struct pas) * (HABA+1) * (HABA+1)*2);
    if(sen==NULL ||  cost_map==NULL){
        free(sen);
        free(cost_map);
        return -3;
    }
    at_cost_map=cost_map;
    for(i=0;i<(HABA+1) * (HABA+1);i++){
        *at_cost_map=9999.9;
        at_cost_map++;
    }
    at_cost_map=cost_map;
    naw=new=last=top=sen;
    while(n>m){
        pos_x+=(float)*out;
        out++;
        pos_y+=(float)*out;
        out++;
        m++;
    }
    pos_x/=n;
    pos_y/=n;
    printf("(%f,%f)\n",pos_x,pos_y);
    naw->pos[0]=loc_x;
    naw->pos[1]=loc_y;
    naw->cost=cost;
    naw->yte=-1.1*sqrtf((loc_x-pos_x)*(loc_x-pos_x)+(loc_y-pos_y)*(loc_y-pos_y));
    time2=(double)clock() / CLOCKS_PER_SEC;
    printf("c %f\n",time2-time1);
    time1=(double)clock() / CLOCKS_PER_SEC;
    while(nokori>0){
        naw=next_point_tree(&top);
        //printf("\n|%f,%f!!%d|%d,%d|\n",naw->cost,naw->yte,nokori,naw->pos[0],naw->pos[1]);
        //printf("\n%d",nokori);
        cost=naw->cost;
        tot_x=naw->pos[0];
        tot_y=naw->pos[1];
        last++;
        nokori--;
        for(i=0;i<16;i++){
            tot_x+=arry[i][0];
            tot_y+=arry[i][1];
            
            //printf("(%d,%d)",tot_x,tot_y);
            if(tot_x<0+10 || tot_y<0+10 || tot_x>=900-10 || tot_y>=900-10){
                tot_x-=arry[i][0];
                tot_y-=arry[i][1];
                continue;
            }
            if(tot_x-loc_x<-HABA/2 || tot_y-loc_y<-HABA/2 || tot_x-loc_x>HABA/2 || tot_y-loc_y>HABA/2){
                tot_x-=arry[i][0];
                tot_y-=arry[i][1];
                //printf("[%d,%d]",tot_x-loc_x,tot_y-loc_y);
                continue;
            }
            date=date_start+tot_x+tot_y*y_lan;
            cost_map=at_cost_map+(tot_x-loc_x+HABA/2)+(tot_y-loc_y+HABA/2)*(HABA+1);
            //printf("!%d,%d!",*date,(tot_x-loc_x+HABA/2)+(tot_y-loc_y+HABA/2)*(HABA+1));

            //0mu 1heiya 2kawa 3tetudou 4douro 5mori 6mati
            point_cost=1.0;
            if(*date==1)point_cost=1.0;
            else if(*date==2)point_cost=50.0;
            else if(*date==3)point_cost=0.5;
            else if(*date==4)point_cost=0.5;
            else if(*date==5){
                    new->pos[0]=tot_x;
                    new->pos[1]=tot_y;
                    new->mae=naw;
                    nokori=0;
                    printf("z");
                    break;
            }
            else if(*date==6){
                    new->pos[0]=tot_x;
                    new->pos[1]=tot_y;
                    new->mae=naw;
                    nokori=0;
                    printf("z");
                    break;
            }
            else continue;
            cost+=sqrtf(arry[i][1]*arry[i][1]+arry[i][0]*arry[i][0])*point_cost;
            if(new==sen+(HABA/2+1)*(HABA/2+1)*10-1){
                free(sen);
                free(cost_map);
                return -2;
            }
            if(*cost_map>cost){
                *cost_map=cost;
                new++;
                new->pos[0]=tot_x;
                new->pos[1]=tot_y;
                new->cost=cost;
                new->mae=naw;
                new->yte=-1.1*sqrtf((tot_x-pos_x)*(tot_x-pos_x)+(tot_y-pos_y)*(tot_y-pos_y));
                if (sqrtf((tot_x-pos_x)*(tot_x-pos_x)+(tot_y-pos_y)*(tot_y-pos_y))>300){
                    nokori=0;
                    printf("a");
                    break;
                }
                tree(new,top);
                nokori++;
            }
            cost-=sqrtf(arry[i][1]*arry[i][1]+arry[i][0]*arry[i][0])*point_cost;
            tot_x-=arry[i][0];
            tot_y-=arry[i][1];
        }
    }
    time2=(double)clock() / CLOCKS_PER_SEC;
    printf("c %f\n",time2-time1);
    time1=(double)clock() / CLOCKS_PER_SEC;
    i=0;
    date=date_start;
    cost_map=at_cost_map;
    do{
        *date=new->pos[0];
        date++;
        *date=new->pos[1];
        date++;
        i++;
        new=new->mae;
    }while(new != sen);
    free(cost_map);
    free(sen);
    time2=(double)clock() / CLOCKS_PER_SEC;
    printf("c %f\n",time2-time1);
    return i;
}
