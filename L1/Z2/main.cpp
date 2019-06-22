#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <windows.h>
#include <map>
#include <cmath>
#include <string>
using namespace std;

map < double, double > conv;
bool compare(string a, string b){

    unsigned int ai = 0;
    unsigned int bi = 0;
    do{
        double as = 0;
        double bs = 0;
        if((int)(a[ai]) < 0){
            as = conv[a[ai]*1000 + a[ai+1]];
            ai++;
        }
        else
            as = (int)(a[ai]);
        if((int)(b[bi]) < 0){
            bs = conv[b[bi]*1000 + b[bi+1]];
            bi++;
        }
        else
            bs = (int)(b[bi]);
        if(as < bs)
            return true;
        if(bs < as)
            return false;
        ai++;
        bi++;
    }
    while(ai <= a.size() || bi <= b.size());
    return false;
}

int main()
{
    conv[-60*1000 -123] = 97.5; //ą
    conv[-60*1000 -121] = 99.5; //ć
    conv[-60*1000 -103] = 101.5; //ę
    conv[-59*1000 -126] = 108.5; //ł
    conv[-59*1000 -124] = 110.5; //ń
    conv[-61*1000 -77] = 111.5; //ó
    conv[-59*1000 -101] = 115.5; //ś
    conv[-59*1000 -70] = 122.3; //ź
    conv[-59*1000 -68] = 122.7; //ż

    ifstream words;
    words.open("words_for_ai1.txt");
    vector < string > slownik;
    string word;
    while(words >> word)
        slownik.push_back(word);

    sort (slownik.begin(), slownik.end(), compare);

    //cout << binary_search(slownik.begin(),slownik.end(), "oczywista", compare) << endl;

    ifstream in;
    in.open("zad2_input.txt");

    string ile;
    in >> ile;
    int tt = stod(ile.substr(3));
    ofstream out;
    out.open("zad2_output.txt");

    for(int t = 0; t != tt; t++){
        string tekst;
        in >> tekst;

        vector < vector < int > > grupy;

        vector < int > grupa;
        grupa.push_back(0);
        grupy.push_back(grupa);

        for(int i = 0; i != tekst.size(); i++){
            if((int)(tekst[i]) < 0)
                i++;

            long long kol = grupy.size();
            for(long long j = 0; j != kol; j++){

                int last = grupy[j][grupy[j].size()-1];
                string check = tekst.substr(last,i-last+1);

                if(binary_search(slownik.begin(),slownik.end(),check,compare)){
                    vector < int > nowa_grupa;
                    for(int q = 0; q != grupy[j].size(); q++)
                        nowa_grupa.push_back(grupy[j][q]);
                    nowa_grupa.push_back(i+1);
                    grupy.push_back(nowa_grupa);
                }
            }
        }

        int mx = -1;
        int imx = 0;

        for(long long i = 0; i != grupy.size(); i++){
            int last = grupy[i][grupy[i].size()-1];
            if(tekst.size() - last == 0){
                int suma = 0;
                for(int j = 0; j != grupy[i].size()-1; j++)
                    suma = suma + (grupy[i][j+1]-grupy[i][j])*(grupy[i][j+1]-grupy[i][j]);
                if(suma > mx){
                    mx = suma;
                    imx = i;
                }
            }
        }

        for(int i = 0; i != grupy[imx].size()-1; i++)
            out << tekst.substr(grupy[imx][i], grupy[imx][i+1]-grupy[imx][i]) << " ";
        out << endl;

        /*for(int i = 0 ; i != grupy.size(); i++){
            for(int j = 0; j != grupy[i].size(); j++)
                cout << grupy[i][j] << " ";
            cout << endl;
        }*/

        out << mx << " " << grupy.size() << endl << endl;
    }
    return 0;
}
