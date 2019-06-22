#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>
using namespace std;

ifstream in;
ofstream out;
short px[3];
short py[3];

bool way(int f, bool o){
    if(o){
        if(py[0] == py[1] && ((px[1] < px[0] && px[0] < f) || (f < px[0] && px[0] < px[1])))
            return 0;
        return 1;
    }
    if(px[0] == px[1] && ((py[1] < py[0] && py[0] < f) || (f < py[0] && py[0] < py[1])))
        return 0;
    return 1;
}

bool check_mat(bool b){
    if(b){
        if((px[2] == px[1] && !(py[2] == py[1]) && !(px[1] == px[0] &&((py[1] < py[0] && py[0] < py[2])||(py[1] > py[0] && py[0] > py[2])))) ||
           (py[2] == py[1] && !(px[2] == px[1]) && !(py[1] == py[0] &&((px[1] < px[0] && px[0] < px[2])||(px[1] > px[0] && px[0] > px[2])))) ||
            (abs(px[2]-px[0]) <= 1 && abs(py[2]-py[0]) <= 1))
            return 1;
        return 0;
    }
    else{
        if(abs(px[2]-px[0]) <= 1 && abs(py[2]-py[0]) <= 1)
            return 1;
        return 0;
    }
}

bool correct(int x){
    if(x >= 0 && x <= 7)
        return 1;
    return 0;
}

bool taken(int n, int x, int y){
    int a = (n+1)%3;
    int b = (n+2)%3;
    if((px[a] == x && py[a] == y) || (px[b] == x && py[b] == y))
        return 1;
    return 0;
}

bool check_mate(){
    for(int i = -1; i != 2; i++){
        for(int j = -1; j != 2; j++){
            px[2] = px[2] + i;
            py[2] = py[2] + j;
            if(correct(px[2]) && correct(py[2])){
                if(!check_mat(1)){
                    px[2] = px[2] - i;
                    py[2] = py[2] - j;
                    return 0;
               }
            }
            px[2] = px[2] - i;
            py[2] = py[2] - j;
        }
    }
    return 1;
}

void print_state(int n,int deep){
    out << endl << n << ", " << deep << ": " << endl;
    for(int j = 7; j != -1; j--){
        for(int i = 0; i != 8; i++){
            out << "|";
            int an = 0;
            for(int q = 0; q != 3; q++){
                if(px[q] == i && py[q] == j)
                    an = q+1;
            }
            out << an;
        }
        out << "|" << endl;
        for(int j = 0; j != 8; j++)
            out << "--";
        out << "-" << endl;
    }
}

int main()
{
    int tt;
    in.open("zad1_input.txt");
    in >> tt;
    out.open("zad1_output.txt");
    for(int t = 0; t != tt; t++)
    {
        string a;
        in >> a;
        int base = 0;
        if(a == "white")
            base = 1;

        for(int i = 0; i != 3; i++){
            in >> a;
            int x = (int)(a[0])-97;
            int y = (int)(a[1])-49;
            px[i] = x;
            py[i] = y;
        }

        vector < int > tab[8];
        for(int i = 0; i != 3; i++){
            tab[i*2].push_back(px[i]);
            tab[i*2+1].push_back(py[i]);
        }
        tab[6].push_back(0);
        tab[7].push_back(-1);

        int index = 0;
        bool found = 0;
        int deep = 0;
        while(!found){
            for(int i = 0; i != 3; i++){
                px[i] = tab[i*2][index];
                py[i] = tab[i*2+1][index];
            }
            deep = tab[6][index];
            int turn = (base + deep)%2;
            //print_state(index,deep);
            if(check_mate()){
                found = 1;
            }
            if(turn == 0){
                for(int i = -1; i != 2; i++){
                    for(int j = -1; j != 2; j++){
                        if((i != 0 || j != 0) && correct(px[2]+i) && correct(py[2]+j) && !taken(2,px[2]+i,py[2]+j)){
                            px[2] = px[2] + i;
                            py[2] = py[2] + j;
                            if(!check_mat(1)){
                                for(int i = 0; i != 3; i++){
                                    tab[i*2].push_back(px[i]);
                                    tab[i*2+1].push_back(py[i]);
                                }
                                tab[6].push_back(deep+1);
                                tab[7].push_back(index);
                            }
                            px[2] = px[2] - i;
                            py[2] = py[2] - j;
                        }
                    }
                }
            }
            else{
                for(int i = -1; i != 2; i++){
                    for(int j = -1; j != 2; j++){
                        if((i != 0 || j != 0) && correct(px[0]+i) && correct(py[0]+j) && !taken(0,px[0]+i,py[0]+j)){
                            px[0] = px[0] + i;
                            py[0] = py[0] + j;
                            if(!check_mat(0)){
                                for(int i = 0; i != 3; i++){
                                    tab[i*2].push_back(px[i]);
                                    tab[i*2+1].push_back(py[i]);
                                }
                                tab[6].push_back(deep+1);
                                tab[7].push_back(index);
                            }
                            px[0] = px[0] - i;
                            py[0] = py[0] - j;
                        }
                    }
                }
                for(int i = 0; i != 2; i++){
                    int k;
                    if(i == 0)
                        k = 0;
                    else
                        k = 7;
                    if(px[1] != k && !taken(1,k,py[1]) && way(k,1)){
                        int r = px[1];
                        px[1] = k;
                        for(int i = 0; i != 3; i++){
                            tab[i*2].push_back(px[i]);
                            tab[i*2+1].push_back(py[i]);
                        }
                        tab[6].push_back(deep+1);
                        tab[7].push_back(index);
                        px[1] = r;
                    }
                }
                for(int i = 0; i != 2; i++){
                    int k;
                    if(i == 0)
                        k = 0;
                    else
                        k = 7;
                    if(py[1] != k && !taken(1,px[1],k) && way(k,0)){
                        int r = py[1];
                        py[1] = k;
                        for(int i = 0; i != 3; i++){
                            tab[i*2].push_back(px[i]);
                            tab[i*2+1].push_back(py[i]);
                        }
                        tab[6].push_back(deep+1);
                        tab[7].push_back(index);
                        py[1] = r;
                    }
                }
            }
            index++;
        }
        index--;
        out << t << ": " << endl;
        while(index != -1){
            for(int i = 0; i != 3; i++){
                px[i] = tab[i*2][index];
                py[i] = tab[i*2+1][index];
            }
            deep = tab[6][index];
            print_state(index, deep);
            index = tab[7][index];
        }
    }
    in.close();
    out.close();
}
