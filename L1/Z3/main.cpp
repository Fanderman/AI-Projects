#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <algorithm>
using namespace std;

int main()
{
    srand(time(NULL));
    int bwin = 0;
    int fwin = 0;

    int blot[5];
    int fig[5];
    bool karty[52];

    for(int t = 0; t != 100000; t++){

        for(int i = 0; i != 52; i++){
            karty[i] = 0;
        }

        for(int i = 0; i != 5; i++){
            blot[i] = rand()%36;
            if(karty[blot[i]])
                i--;
            else
                karty[blot[i]] = 1;
        }

        for(int i = 0; i != 5; i++){
            fig[i] = rand()%16+36;
            if(karty[fig[i]])
                i--;
            else
                karty[fig[i]] = 1;
        }

        sort(blot,blot+5);
        sort(fig,fig+5);

        bool figwin = 1;

        for(int i = 0; i != 4; i++){
            if(blot[i]/4 == blot[i+1]/4)
                figwin = 0;
        }

        for(int i = 0; i != 4; i++){
            if(fig[i]/4 == fig[i+1]/4)
                figwin = 1;
        }

        int cnt = 0;
        int a = -1;
        for(int i = 0; i != 4; i++){
            if(blot[i]/4 == blot[i+1]/4 && blot[i]/4 != a){
                cnt++;
                a = blot[i]/4;
            }
        }
        if(cnt == 2)
            figwin = 0;

        cnt = 0;
        a = -1;
        for(int i = 0; i != 4; i++){
            if(fig[i]/4 == fig[i+1]/4 && fig[i]/4 != a){
                cnt++;
                a = fig[i]/4;
            }
        }
        if(cnt == 2)
            figwin = 1;

        for(int i = 0; i != 3; i++){
            if(blot[i]/4 == blot[i+1]/4 && blot[i+1]/4 == blot[i+2]/4)
                figwin = 0;
        }

        for(int i = 0; i != 3; i++){
            if(fig[i]/4 == fig[i+1]/4 && fig[i+1]/4 == fig[i+2]/4)
                figwin = 1;
        }

        bool win = 1;
        for(int i = 0; i != 4; i++){
            if(blot[i]/4 != blot[i+1]/4 +1)
                win = 0;
        }
        if(win)
            figwin = 0;

        win = 1;
        for(int i = 0; i != 4; i++){
            if(blot[i]%4 != blot[i+1]%4)
                win = 0;
        }
        if(win)
            figwin = 0;

        win = 1;
        for(int i = 0; i != 4; i++){
            if(fig[i]%4 != fig[i+1]%4)
                win = 0;
        }
        if(win)
            figwin = 1;

        a = -1;
        for(int i = 0; i != 3; i++){
            if(blot[i]/4 == blot[i+1]/4 && blot[i+1]/4 == blot[i+2]/4)
                a = blot[i]/4;
        }
        for(int i = 0; i != 4; i++){
            if(blot[i]/4 == blot[i+1]/4 && blot[i]/4 != a)
                figwin = 0;
        }

        a = -1;
        for(int i = 0; i != 3; i++){
            if(fig[i]/4 == fig[i+1]/4 && fig[i+1]/4 == fig[i+2]/4){
                a = fig[i]/4;
            }
        }
        for(int i = 0; i != 4; i++){
            if(fig[i]/4 == fig[i+1]/4 && fig[i]/4 != a)
                figwin = 1;
        }

        for(int i = 0; i != 2; i++){
            if(blot[i]/4 == blot[i+1]/4 && blot[i+1]/4 == blot[i+2]/4 && blot[i+2]/4 == blot[i+3]/4){
                figwin = 0;
            }
        }

        for(int i = 0; i != 2; i++){
            if(fig[i]/4 == fig[i+1]/4 && fig[i+1]/4  == fig[i+2]/4 && fig[i+2]/4 == fig[i+3]/4){
                figwin = 1;
            }
        }

        win = 1;
        for(int i = 0; i != 4; i++){
            if(blot[i+1] - blot[i] != 4)
                win = 0;
        }
        if(win)
            figwin = 0;

        if(figwin) fwin++;
        else bwin++;

    }

    cout << ((double)(fwin))/1000 << "%";
}
