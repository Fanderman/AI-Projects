#include <iostream>
#include <fstream>
#include <vector>
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

int main()
{
    ifstream in;
    in.open("zad4_input.txt");
    ofstream out;
    out.open("zad4_output.txt");
    int tt;
    in >> tt;
    for(int t = 0; t != tt; t++){
        string x;
        in >> x;
        int n;
        in >> n;
        int y[x.size()];
        for(int i = 0; i != x.size(); i++){
            if(i < n)
                y[i] = 1;
            else
                y[i] = 0;
        }
        int mn = n;
        for(int i = 0; i != x.size()-n+1; i++){
            string a;
            a.resize(5,'0');
            for(int j = 0; j != x.size(); j++)
                a[j] = (char)(y[j])+48;
            int dif = edit_distance(x,a);
            if(dif < mn)
                mn = dif;
            y[i+n] = 1;
            y[i] = 0;
        }
        out << mn << endl;
    }
}
