#include <iostream>
using namespace std;


int main()  {
    int d, m, a;
    while (cin >> d >> m >> a) {
        bool traspas = a%4 == 0 and (a%100 != 0 or a%400 == 0);
        bool corr = true;
        if (d < 1 or d > 31 or m < 1 or m > 12
            or ((m == 4 or m == 6 or m == 9 or m == 11) and d > 30)
            or (m == 2 and (d > 29 or (d == 29 and not traspas)))) corr = false;

        if (corr) cout << "Correct Date" << endl;
        else cout << "Incorrect Date" << endl;
    }
}
