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

int opt(string x, int n){
    int y[x.size()];
    for(int i = 0; i != x.size(); i++){
        if(i < n)
            y[i] = 1;
        else
            y[i] = 0;
    }
    int mn = x.size();
    for(int i = 0; i != x.size()-n+1; i++){
        string a;
        a.resize(x.size(),'0');
        for(int j = 0; j != x.size(); j++)
            a[j] = (char)(y[j])+48;
        int dif = edit_distance(x,a);
        if(dif < mn)
            mn = dif;
        y[i+n] = 1;
        y[i] = 0;
    }
    return mn;
}

string conv(vector < int > x){
    string a = "";
    for(int i = 0; i != x.size(); i++){
        a = a + (char)(x[i]+48);
    }
    return a;
}

int main()
{
    srand(time(NULL));
    ifstream in;
    in.open("zad5_input.txt");
    ofstream out;
    out.open("zad5_output.txt");
    int width,height;
    vector < vector < int > > tabh;
    vector < vector < int > > tabw;
    vector < int > up;
    vector < int > left;
    in >> width >> height;
    for(int i = 0; i != width; i++){
        int a;
        in >> a;
        up.push_back(a);
    }
    for(int i = 0; i != height; i++){
        int a;
        in >> a;
        left.push_back(a);
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
            }
        }
    }
    return 0;
}
