#ifndef queue_H
#define queue_H

#include <iostream>
#include <stdlib.h>
#include <stdio.h>

//using namespace std;

struct node
{
  int data;
  node *next;
};


class queue
{
  public:
    queue(int);                 //CONSTRUCTOR
    queue();                    //prototype for default max = 100
    queue& enqueue(int);    //add to list
    int dequeue();              //delete last element in list
    bool queueEmpty();          //check if list is empty
    
    int elements();             //ex2 get size
    friend void print(queue);        //print values divided by space, after: endl
    
    queue operator+ (int);     //overloading + operator (e.g. q + e q.enqueue(e))
    int operator- ();           //overloading - operator (e.g. e = -q e = q.dequeue())

  
  protected:
    int size;
    int max;
    node *tail;
    node *head;
};

#endif
