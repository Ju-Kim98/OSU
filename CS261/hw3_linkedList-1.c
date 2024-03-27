/***********************************************************
* Author: JuHyun Kim
* Email: 
* Date Created: 
* Filename: linkedList.c
*
* Overview:
*	This program is a linked list implementation of the deque and bag ADTs. 
*	Note that both implementations utilize a linked list with
*	both a front and back sentinel and double links (links with
*	next and prev pointers).
************************************************************/

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include "linkedList.h"

#ifndef FORMAT_SPECIFIER
#define FORMAT_SPECIFIER "%d"
#endif


/* ************************************************************************
	Structs Link and LinkedList
************************************************************************ */

//Double Link
struct Link{
	TYPE value;
	struct Link* prev;
	struct Link* next;
};

//Doule linked list with front and vack sentinels
struct LinkedList{
	int size; 
	struct Link* head;
	struct Link* tail;
};


/* ************************************************************************
	Linked List Functions
************************************************************************ */

// Allocates and initializes a linked list
LinkedList* linkedListCreate()
{
	LinkedList* newlist = (LinkedList*)malloc(sizeof(Link));
	Link* newlink_A = (Link*)malloc(sizeof(Link));
	Link* newlink_B = (Link*)malloc(sizeof(Link));
	
	newlist->head = newlink_A;
	newlist->tail = newlink_B;
	newlist->size = 0;
	
	newlink_A->next = newlink_B;
	newlink_A->prev = NULL;
	newlink_A->value = 0;
	
	newlink_B->next = NULL;
	newlink_B->prev = newlink_A;
	newlink_B->value = 0;
	
	return newlist;

}										

//Deallocates every link in the list including the sentinels and deletes the list itself
void deletelinkedList(LinkedList* list)
{
	assert(list != NULL);
	Link* temp = list->head;
	
	while(list->tail != list->head){
		temp=temp->next;
		free(list->head);
		list->head = temp;
	}
	free(list->head);
	free(list);
}							

// Returns the size of the list
int sizelinkedList(LinkedList* myList)
{	
	assert(myList != NULL);
	return myList->size;								
}								


// Returns 1 if the list is empty and 0 otherwise
int isEmptyLinkedList(LinkedList* myList)
{
	int empty = 0;
	if(myList->head->next == myList->tail)
		empty = 1;
	if(myList->size == 0)
		empty = 1;
	
	return empty;
}


					
// Adds a new Link with the given value before the fiven link and increments the list's size
void addLinkBefore(LinkedList* list, TYPE value){
	assert(list != NULL);
	Link* newLink = (Link*)malloc(sizeof(Link));
	
	newLink->next = list->head->next;
	newLink->prev = list->head;
	newLink->value = value;
	
	list->head->next = newLink;
	newLink->next->prev = newLink;
	
	list->size++;
	
}	


// Removes the given link from the list and decrements the list's size
void removeLink(LinkedList* list, TYPE value){

	assert(list != NULL);

	Link* nextLink = list->head->next;
	Link* currentLink = list->head;
	
	int tempSize = list->size;
	int i;
	for(i=0; i<tempSize; i++) {
		currentLink = nextLink;
		nextLink = nextLink->next;
		if(currentLink->value == value){
			currentLink->prev->next = nextLink;
			nextLink->prev = currentLink->prev;
			free(currentLink);
			list->size--;
		}
	}	
	
}


// Prints the values of the links in the list from front to back
void printLinkedList(LinkedList* list){
	assert(list != NULL);
	Link* currentLink = list->head;
	int i;
	for(i=0; i<list->size; i++){
		currentLink = currentLink->next;
		printf("%i ", currentLink->value);
	}
	
}


/* ************************************************************************
	Deque Functions
************************************************************************ */

/* Note that the linked list is the data structure to use for the deque and bag, therefore linked list functions may be the 
	used for the deque and bag implementations.*/
	
// Alloates and initializes the deque, 
Deque* dequeCreate(){
	return linkedListCreate();
}


// Deallocates the data and deletes the deque
void deleteDeque(Deque* myDeque) {
    deletelinkedList(myDeque);
}


// Returns the size of the deque
int sizeDeque(Deque* myDeque) {
	return sizelinkedList(myDeque);
}


// Returns 1 if the deque is empty and 0 otherwise
int isEmptyDeque(Deque* myDeque) {
	isEmptyLinkedList(myDeque);
}


// Adds a new link with the given value to the front of the deque
void addFrontDeque(Deque* myDeque, TYPE value) {
	addLinkBefore(myDeque,value);
}


// Adds a new link with the given value to the back of the deque
void addBackDeque(Deque* myDeque, TYPE value) {
	
	assert(myDeque != NULL);
    Link* newLink = (Link*)malloc(sizeof(Link));
    
    newLink->next = myDeque->tail;
    newLink->prev = myDeque->tail->prev;
    newLink->value = value;
    
    myDeque->tail->prev = newLink;
    newLink->prev->next = newLink;
    
    myDeque->size++;
}


// Returns the value of the link at the front of the deque
TYPE frontDeque(Deque* myDeque) {
	
	assert(myDeque != NULL);
    return myDeque->head->next->value ;
    
}


// Returns the value of the link at the back of the deque
TYPE backDeque(Deque* myDeque) {
	
	assert(myDeque != NULL);
    return myDeque->tail->prev->value ;

}


// Removes the link at the front of the deque
void removeFrontDeque(Deque* myDeque) {
	
/*	struct Link * some_link = myDeque->head->next->next ;
    free( myDeque->head->next ) ;
    some_link->prev = myDeque->head ;
    myDeque->head->next = some_link ;	*/
	
	assert(myDeque != NULL);
    struct Link* deleteLink = (Link*)malloc(sizeof(Link));
    deleteLink = myDeque->head->next;
    myDeque->head->next = myDeque->head->next->next;
    myDeque->head->next->next->prev = myDeque->head;
    free(deleteLink);
    myDeque->size--;
    

}


// Removes the link at the back of the deque
void removeBackDeque(Deque* myDeque) {

/*    struct Link * link = myDeque->tail->prev->prev ;
    free( myDeque->tail->prev ) ;
    link->next = myDeque->tail ;
    myDeque->tail->prev = link ;	*/
    
    assert(myDeque != NULL);
	struct Link* deleteLink = (Link*)malloc(sizeof(Link));
	deleteLink = myDeque->tail->prev;
	myDeque->tail->prev = myDeque->tail->prev->prev;
	myDeque->tail->prev->prev->next = myDeque->tail;
	free(deleteLink);
	myDeque->size --; 

}


// Prints the values of the links in the deque from front to back
void printDeque(Deque* myDeque) {

    assert(myDeque != NULL);
	printLinkedList(myDeque);

}


/* ************************************************************************
	Bag Functions
************************************************************************ */

// Allocates and initializes the bag.
Bag* bagCreate(){
	return linkedListCreate();
}

// Deallocates the data and deletes the bag							
void deleteBag(Bag* myBag){
	assert(myBag != NULL);
	deletelinkedList(myBag);
}				

// Returns the size of the bag
int sizeBag(Bag* myBag){
	return sizelinkedList(myBag); 
}					

// Returns "1" if the bag is empty or "0" if not 
int isBagEmpty(Bag* myBag){
	return isEmptyLinkedList(myBag);
}					

// Adds an element into the bag
void addBag(Bag* myBag, TYPE value){
	addLinkBefore(myBag,value);
}		

// Returns "1" if the bag contains the specified element or "0" if not 
int containsBag(Bag* myBag, TYPE value){
	assert(myBag != NULL);
	//assert(value != NULL);
	Link* currentLink = myBag->head;
	int ifContain = 0;
	int i;
	for(i=0; i<myBag->size; i++){
		currentLink = currentLink->next;
		if(currentLink->value == value){
			ifContain = 1;
		}
	}
	return ifContain;
}	

// Removes the specific element from the bag
void removeBag(Bag* myBag, TYPE value){
	removeLink(myBag,value);
}		

// Prints the values of the links in the bag from front to back
void printBag(Bag* myBag){
	printLinkedList(myBag);
}




