#include <iostream>
#include <fstream>
#include <vector>
#include <time.h>
#include <stdlib.h>
using namespace std;

unsigned int edit_distance(const string& s1, const string& s2)
{
	const size_t len1 = s1.size(), len2 = s2.size();
	vector< vector < unsigned int> > d(len1 + 1, vector<unsigned int>(len2 + 1));

	d[0][0] = 0;
	for(unsigned int i = 1; i <= len1; i++)
        d[i][0] = i;
	for(unsigned int i = 1; i <= len2; i++)
        d[0][i] = i;

	for(unsigned int i = 1; i <= len1; i++)
		for(unsigned int j = 1; j <= len2; j++)
            d[i][j] = min(min(d[i - 1][j] + 1, d[i][j - 1] + 1), d[i - 1][j - 1] + (s1[i - 1] == s2[j - 1] ? 0 : 1));

	return d[len1][len2];
}

string conv(vector < int > x){
    string a = "";
    for(int i = 0; i != x.size(); i++){
        a = a + (char)(x[i]+48);
    }
    return a;
}

int opt2(string x, vector < int > y, vector < int > n, int ind, int rek){
    int mn = x.size()*2;
    if(ind < n.size()){
        if(rek + n[ind] <= x.size()){
            for(int i = rek; i != x.size()-n[ind]+1; i++){
                for(int j = 0; j != n[ind]; j++){
                    y[j+i] = 1;
                }
                int dif = opt2(x,y,n,ind+1,i+n[ind]+1);
                if(dif < mn)
                    mn = dif;
                for(int j = 0; j != n[ind]; j++){
                    y[j+i] = 0;
                }
            }
            return mn;
        }
    }
    else{
        mn = edit_distance(x,conv(y));
    }
    return mn;
}

int opt(string x, vector < int > n){
    vector < int > y;
    for(int i = 0; i != x.size(); i++){
        y.push_back(0);
    }
    return opt2(x,y,n,0,0);
}



int main()
{
    srand(time(NULL));
    ifstream in;
    in.open("zad1_input.txt");
    ofstream out;
    out.open("zad1_output.txt");
    int width,height;
    vector < vector < int > > tabh;
    vector < vector < int > > tabw;
    vector < vector < int > > up;
    vector < vector < int > > left;
    in >> width >> height;
    for(int i = 0; i != width; i++){
        int a;
        in >> a;
        vector < int > help;
        help.clear();
        for(int j = 0; j != a; j++){
            int aa;
            in >> aa;
            help.push_back(aa);
        }
        up.push_back(help);
    }
    for(int i = 0; i != height; i++){
        int a;
        in >> a;
        vector < int > help;
        help.clear();
        for(int j = 0; j != a; j++){
            int aa;
            in >> aa;
            help.push_back(aa);
        }
        left.push_back(help);
    }
    while(true){
        tabw.clear();
        tabh.clear();
        for(int i = 0; i != width; i++){
            vector < int > h;
            h.resize(height,0);
            tabw.push_back(h);
        }
        for(int i = 0; i != height; i++){
            vector < int > h;
            h.resize(width,0);
            tabh.push_back(h);
        }
        for(int i = 0; i != width; i++){
            for(int j = 0; j != height; j++){
                tabw[i][j] = rand()%2;
                tabh[j][i] = tabw[i][j];
            }
        }
        int wrong = 0;
        vector < int > wrongu;
        vector < int > wrongl;
        wrongu.clear();
        wrongl.clear();
        for(int i = 0; i != width; i++){
            wrongu.push_back(opt(conv(tabw[i]),up[i]));
            if(wrongu[i] > 0)
                wrong++;
        }
        for(int i = 0; i != height; i++){
            wrongl.push_back(opt(conv(tabh[i]),left[i]));
            if(wrongl[i] > 0)
                wrong++;
        }
        int limit = width*height*20;
        for(int q = limit; q > 0; q--){
            /*for(int i = 0; i != width; i++){
                    for(int j = 0; j != height; j++){
                        if(tabw[i][j] == 1)
                            cout << '#';
                        else
                            cout << 'X';
                    }
                    cout << endl;
                }
            cout << endl;*/
            //sprawdzanie poprawnosci wierszy i kolumn
            if(wrong == 0){
                for(int i = 0; i != width; i++){
                    for(int j = 0; j != height; j++){
                        if(tabw[i][j] == 1)
                            out << (char)(35);
                        else
                            out << '.';
                    }
                    out << endl;
                }
                return 0;
            }
            int nbest = 0;
            //wybor kolumny/wiersza
            if(rand()%10 == 0){
                nbest = rand()%(width+height);
            }
            else{
                int best = -1;
                for(int i = 0; i != width; i++){
                    if(wrongu[i] > best){
                        nbest = i;
                        best = wrongu[i];
                    }
                    if(wrongu[i] == best && rand()%2 == 0){
                        nbest = i;
                    }
                }
                for(int i = 0; i != height; i++){
                    if(wrongl[i] > best){
                        nbest = i+width;
                        best = wrongl[i];
                    }
                    if(wrongl[i] == best && rand()%2 == 0){
                        nbest = i+width;
                    }
                }
            }
            //zmiana bitu
            if(nbest < width){
                int mnn = 0;
                int mn = height*2;
                for(int i = 0; i != height; i++){
                    if(tabw[nbest][i] == 1)
                        tabw[nbest][i] = 0;
                    else
                        tabw[nbest][i] = 1;
                    int res = opt(conv(tabw[nbest]),up[nbest]);
                    if(res < mn){
                        mnn = i;
                        mn = res;
                    }
                    if(res == mn && rand()%2 == 0){
                        mnn = i;
                    }
                    if(tabw[nbest][i] == 1)
                        tabw[nbest][i] = 0;
                    else
                        tabw[nbest][i] = 1;
                }
                if(tabw[nbest][mnn] == 0){
                    tabw[nbest][mnn] = 1;
                    tabh[mnn][nbest] = 1;
                }
                else{
                    tabw[nbest][mnn] = 0;
                    tabh[mnn][nbest] = 0;
                }

                int nwu = opt(conv(tabw[nbest]),up[nbest]);
                if(nwu < wrongu[nbest] && nwu == 0)
                    wrong--;
                if(nwu > wrongu[nbest] && wrongu[nbest] == 0)
                    wrong++;
                wrongu[nbest] = nwu;

                int nwl = opt(conv(tabh[mnn]),left[mnn]);
                if(nwl < wrongl[mnn] && nwl == 0)
                    wrong--;
                if(nwl > wrongl[mnn] && wrongl[mnn] == 0)
                    wrong++;
                wrongl[mnn] = nwl;
            }
            else{
                nbest = nbest - width;
                int mnn = 0;
                int mn = width*2;
                for(int i = 0; i != width; i++){
                    if(tabh[nbest][i] == 1)
                        tabh[nbest][i] = 0;
                    else
                        tabh[nbest][i] = 1;
                    int res = opt(conv(tabh[nbest]),left[nbest]);
                    if(res < mn){
                        mnn = i;
                        mn = res;
                    }
                    if(res == mn && rand()%2 == 0){
                        mnn = i;
                    }
                    if(tabh[nbest][i] == 1)
                        tabh[nbest][i] = 0;
                    else
                        tabh[nbest][i] = 1;
                }
                if(tabh[nbest][mnn] == 0){
                    tabh[nbest][mnn] = 1;
                    tabw[mnn][nbest] = 1;
                }
                else{
                    tabh[nbest][mnn] = 0;
                    tabw[mnn][nbest] = 0;
                }

                int nwu = opt(conv(tabw[mnn]),up[mnn]);
                if(nwu < wrongu[mnn] && nwu == 0)
                    wrong--;
                if(nwu > wrongu[mnn] && wrongu[mnn] == 0)
                    wrong++;
                wrongu[mnn] = nwu;

                int nwl = opt(conv(tabh[nbest]),left[nbest]);
                if(nwl < wrongl[nbest] && nwl == 0)
                    wrong--;
                if(nwl > wrongl[nbest] && wrongl[nbest] == 0)
                    wrong++;
                wrongl[nbest] = nwl;
            }
        }
    }
    return 0;
}
