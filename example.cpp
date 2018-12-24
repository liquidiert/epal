#include <iostream>
using namespace std;
class myfirstepalclass  {
private:
int privatevar1 = 0;

public:
string var1 = "hallo";
};
//example comment
int main() {
int scur = 5;
int i = 40;
for (int i = 0; i < 20; i++) {
if (i % 2  ==  0) {
scur = scur + 1;
cout << scur << endl;
try{
cout << scur << endl;
} catch (exception lulzerror) {
cout << "nope" << endl;
}
}
}
myfirstepalclass scurclass = myfirstepalclass();
scurclass.var1  = "lol";
string ***ex_ptr = &scurclass.var1;
cout << *ex_ptr << endl;
cout << scurclass.var1 << endl;
switch (scur) {
case 15:
cout << "sucess" << endl;
break;
case 1:
cout << "noooo" << endl;
break;
default:
	cout << "Switch case error" << endl;
}
cout << scur << endl;
/* a neatly block comment
*/
	return 0;
}