#include <iostream>
#include <string>
#include <vector>
using namespace std;


char traduit(char c, string taula) {
    if (c == '_') return ' ';
    int j = 0;
    while (taula[j] != c) ++j;
    return 'a' + j;
}


int main() {
    string taula;
    int n;
    while (cin >> taula >> n) {
        while (n > 0) {
            --n;
            string linia;
            cin >> linia;
            for (int i = 0; i < linia.size(); ++i) {
                cout << traduit(linia[i], taula);
            }
            cout << endl;
        }
        cout << endl;
    }
}

