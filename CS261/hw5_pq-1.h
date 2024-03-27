/*
 * This file contains the definition of the interface for the priority queue
 * you'll implement. 
*/
#ifndef __PQ_H
#define __PQ_H
#define TASK_NAME_SIZE 128

/*
 * Structure used to represent a priority queue.
 */
 
typedef struct pq pq;


/*
 * Priority queue interface function prototypes.  Refer to pq.c for
 * documentation about each of these functions.
 */
 
pq* createPq();
void freePq(pq* myPq);
int isemptyPq(pq* myPq);
void addPq(pq* myPq, void* value, int priority);
void* getPq(pq* myPq);
void removePq(pq* myPq);
void printPq(pq* myPq);

#endif

/*
#ifndef TASK_H
#define TASK_H

#define TASK_NAME_SIZE 128

typedef struct Task Task;

struct Task
{
    int priority;
    char name[TASK_NAME_SIZE];
};

Task* taskNew(int priority, char* name);
void taskDelete(Task* task);
int taskCompare(void* left, void* right);
void taskPrint(void* value);

#endif 
*/

