#include "queue.h"

queue::queue(int max)
{
  size = 0;
  this->max = max; //max size of list
  head = tail = nullptr;
}

//default max 100 if no user input
queue::queue(){
  size = 0;
  this->max = 100;
  head = tail = nullptr;
}


void print(queue q)
{
  node *temp = q.head;
  
  while (temp != nullptr)
  {
    std::cout << temp->data << "_";
    temp = temp->next;
  }
  std::cout << std::endl;
}


int queue::elements()
{
  return this->size;
}

queue& queue::enqueue(int value)
{
  if (size == max)
  {
    std::cout << "queue overflow." << std::endl;
  }
  else
  {
    node *newnode = new node;
    newnode->data = value;
    newnode->next = nullptr;
    
    if (head != tail)
    {
      tail->next = newnode;
      tail = newnode;
    }
    else //if (head = tail)
    {
      head = newnode;
      tail = newnode;
    }
    //newnode = nullptr;
  }
  return *this;
}

int queue::dequeue()
{
  if (size == 0)
  {
    std::cout << "attempt to remove element from empty queue." << std::endl;
  }
  else
  {
    node *temp = head;
    head = head->next;
    return temp->data;
    delete temp;
  }
}

bool queue::queueEmpty()
{
  return size == 0;
}

queue queue::operator+(int e)
{
  return this->enqueue(e);
  //this->enqueue(e);
}

int queue::operator-()
{
  this->dequeue();
}

