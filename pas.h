#ifndef PAS_H
#define PAS_H

#include <stdio.h>
#include <time.h>
#include <math.h>
struct pas
{
        int pos[2];
        float cost;
        float yte;
        struct pas *R_ko;
        struct pas *L_ko;
        struct pas *mae;
        
        
};




// プロトタイプ宣言
void tree(struct pas *nw,struct pas *top){
    struct pas *point=top;
    while(1){
        if(point->cost+point->yte > nw->cost+nw->yte){
            if(point->R_ko!=NULL){
                point=point->R_ko;
            }
            else{
                point->R_ko=nw;
                break;
            }
        }
        else if(point->cost+point->yte == nw->cost+nw->yte){
            if(point->yte > nw->yte){
                if(point->R_ko!=NULL){
                    point=point->R_ko;
                }
                else{
                    point->R_ko=nw;
                    break;
                }
            }
            else{
                if(point->L_ko!=NULL){
                    point=point->L_ko;
                }
                else{
                    point->L_ko=nw;
                    break;
                }
            }
        }
        else{
            if(point->L_ko!=NULL){
            point=point->L_ko;
            }
            else{
                point->L_ko=nw;
                break;
            }
        }
    }

}
struct pas *next_point_tree(struct pas **top){
    int i=0;
    struct pas *exm,*oya;
    struct pas *point=*top;
    if((*top)->R_ko==NULL){
        exm=*top;
        if((*top)->L_ko!=NULL){
            *top=((*top)->L_ko);
            return exm;
        }
        return *top;
    }
    while(point->R_ko!=NULL){
        oya=point;
        point=point->R_ko;
        i++;
    }
    if(point->L_ko!=NULL){
        oya->R_ko=point->L_ko;
    }
    else{
        oya->R_ko=NULL;
    }
    return point;
}
struct pas *next_point(struct pas *last,int num){
    struct pas *point=last,*exm=last;
    struct pas box;
    for(int i=1;i<num;i++){
        point++;
        if(point->yte+point->cost < exm->yte+exm->cost){
            exm=point;
        }
        else if(point->yte+point->cost == exm->yte+exm->cost){
            if(point->yte < exm->yte)exm=point;
        }
    }
    box=*last;
    *last=*exm;
    *exm=box;
    return last;
}
// 定数の宣言





#endif // MYMODULE_H