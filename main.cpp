#include "queue.h"

int main( )  {
  const int max = 100;
  queue myQueue ( max );
  myQueue + 4 + 7 + 1 + 1 + 4 + 2;
  print(myQueue);
  int limit = myQueue.elements( );
  for (int i = 0;  i < limit;  ++i) {
    int a = -myQueue;
    for (int j = 0;  j < limit - 1;  ++j) {
      int b = -myQueue;
      if (a < b)
        myQueue + b;
      else
        myQueue + a, a = b;
    }
    myQueue + a;
  }
  print(myQueue);
  return 0;
}
