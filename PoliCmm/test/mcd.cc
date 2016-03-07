/* 
    Programa de prova 
    Jordi Petit, 2010
*/

#include <iostream>
#include <vector>
using namespace std;


// euclides
int mcd (int a, int b) { 
    while (a != b) {
        if (a > b) a = a - b;
        else b = b - a;
    }
    return a;
}

// principal

int main () {
    cout << "Give me two numbers: ";
    int x, y;
    cin >> x >> y;
    int m = mcd(x, y);
    cout << "The mcd of " << x << " and " << y << " is " << m << endl;
    cout << mcd(x, y) << endl;
}
