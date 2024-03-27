
#include <stdlib.h>
#include <assert.h>
#include <stdio.h>

#include "pq.h"
#include "dynarray.h"


/*
 * This is the structure that represents a priority queue
 */

struct pq
{
    
  struct dynarray* dyn_array;

};


/*
* Struct to store the elements of the priority queue
*/

typedef struct node
{

    void* value;
    int priority;

}node;

/*
 * This function should allocate and initialize an empty priority queue and
 * return a pointer to it.
 */

pq* createPq()
{
    pq* new_queue = malloc(sizeof(pq));
	assert(new_queue);
	new_queue->dyn_array = dynarray_create();
    return new_queue;
}


/*
 * This function should free the memory allocated to a given priority queue
 */

void freePq(pq* myPq)
{
	assert(myPq);
	dynarray_free(myPq->dyn_array);
	free(myPq);
}


/*
 * This function should return 1 if the specified priority queue is empty and
 * 0 otherwise.
 */
//myPq - the priority queue whose emptiness is to be checked. mat not be null

int isemptyPq(pq* myPq)
{
	assert(myPq);
	return dynarray_size(myPq->dyn_array)==0;		// give the size of the array so show if it is empty or not	
}


struct pq_value{		// struct to actually access an element in the priority queue
	int prior;
	void* val;
};


/*
 * This function should add a given element into a priority queue with a
 * specified priority value.
 */
 

void addPq(pq* myPq, void* value, int priority)
{
	assert(myPq);
	struct pq_value *pv = malloc(sizeof(struct pq_value));		//creates the srtuct to access the elements
	pv->val = value; 									//gets the value
	pv->prior = priority; 								//gets the priority num
	dynarray_insert(myPq->dyn_array, -1, pv);			//insets the element into the heap array
	int element = dynarray_size(myPq->dyn_array)-1;		// gets where in the heap to inser the next element
	int par = 0; 										// parent value
	struct pq_value* temp;
	while(par>=0){
		par=(elem-1)/2;					// how to get the correct parent . where to start
		temp=dynarray_set(myPq->dyn_array, par, pv);	// the temp gets the parents value so it acts the parent
		if(temp->prior > pv->prior){					//percolates?? the newly added elemnt in order to make sure that every parent has a smaller priority than children
			dynarray_set(pq->dyn_array, par, pv);		//at the parent indes, set the index with the inserted value
			dynarray_set(pq->dyn_array, elem, temp);	// set with the parent original information
			elem = par; 								// get the new parent information
		}
		else{
				break;
		}
	}
	temp = NULL;	//set to null if the parent value is less than 0
  
  
}


/*
 * This function should return the value of the item with lowest priority
 *
 */

void* getPq(pq* myPq)
{
  assert(myPq);
  pq_value* first = NULL; 	// creats a struct to access the first element
  first = dynarray_get(myPq->dyn_array,0);	//gets the actual element in the first position
  if(first!=NULL){
  		return first->val;		//return the value
  }
  else{
  		return NULL;
  }
}


/*
 * This function should remove the value with lowest priority 
 */

void removePq(struct pq* myPq)
{
	assert(myPq);
	struct pq_value* first=NULL;
	struct pq_value* last=NULL;
	first=dynarray_get(myPq->dyn_array,0);
	last=dynarray_get(myPq->dyn_array,-1);
	  
	dynarray_set(myPq->dyn_array,0,last);
	dynarray_remove(myPq->dyn_array,-1);
	last=NULL;
	  
  	int elem=0; 
	int left=0;//left child element
	int right=0; //right child element
	int min=0;
	
	struct pq_value* t1; //temp to get an element
	struct pq_value* t2; //temp to get an element 
	
	while(1){ //while true
		left=(2*elem)+1; //set to left
		right=(2*elem)+2; //set to right
	
		if(left>dynarray_size(myPq->dyn)-1) 
			break;
		else if(left==dynarray_size(myPq->dyn)-1)
			min=left;
		else{
			if(((struct pq_value*)dynarray_get(myPq->dyn, left))->prior >((struct pq_value*)dynarray_get(myPq->dyn, right))->prior)//makes sure every node's priority value is smaller than the children (percolate)
				min=right; //if left is bigger than right, the minimum is the right
			else
				min=left; //if right is bigger than left, the minimum is the left
		}
		if((((struct pq_value*)dynarray_get(myPq->dyn, elem))->prior)>(((struct pq_value*)dynarray_get(myPq->dyn, min))->prior)){ //continues percolation
			t1=dynarray_get(myPq->dyn,min); //temp gets the min information
			t2=dynarray_get(myPq->dyn, elem); //temp 2 gets the element information
			dynarray_set(myPq->dyn, min, t2);
			dynarray_set(myPq->dyn, elem, t1);
			elem=min;
		}
		else
			break;
	}
	if(first!=NULL){
		void*val=first->val;
		free(first); //frees memory
		return val;
	}
	else{
		return NULL;
	}
  
  
}


/*
 * This function should print the values that are in the pq
 * and their priorities on the screen
 * from the queue.
 */

void printPq(struct pq* myPq)
{
   pq* myPq = (pq*)value;
    printf("(%d, %s)", myPq->priority, myPq->name);
}


