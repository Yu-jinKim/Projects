#include <iostream>
#include "ZFraction.cpp"
using namespace std;

int main()
{
    ZFraction a(4,5);      //Declare a fraction egal to 4/5
    ZFraction e(8,10);
    ZFraction b(2);        //Declare a fraction egal to 2/1 (egal 2)
    ZFraction c,d;         //Declare two fractions egal to 0

    c = a+b;               //Calculate 4/5 + 2/1 = 14/5

    c.display();
    cout << endl;
    e.display();
    cout << endl;
    d = a*b;               //Calculate 4/5 * 2/1 = 8/5

    d.display();
//
//    cout << a << " + " << b << " = " << c << endl;
//
//    cout << a << " * " << b << " = " << d << endl;
//
//    if(a > b)
//        cout << "a is greater than b." << endl;
//    else if(a==b)
//        cout << "a is egal to b." << endl;
//    else
//        cout << "a is smaller than b." << endl;

    return 0;
}
