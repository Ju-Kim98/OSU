// DA_Stack_Bag.c: Dynamic Array, Stack and Bag implementations
#include <assert.h>
#include <stdlib.h>
#include "DA_Stack_Bag.h"


/* ************************************************************************
	Struct DynArr
************************************************************************ */

struct DynArr{
	TYPE* data; //our type can be any data type. Points to the element on the heap.
	int size; //the amount of elements currently in the array
	int capacity; //the maximum amount of elements the array can fit	
};


/* ************************************************************************
	Dynamic Array Functions
************************************************************************ */

/* This function initializes the dynamic array
pre - a capacity exists. post - an empty dynamic array of capacity capacity is declared*/
DynArr* newDynArr(int capacity){
	assert (capacity>= 0); //this makes sure that the capacity is a valid integer basically
	DynArr* my_arr = (DynArr*)malloc(sizeof(DynArr)); //this line initializes the actual array
	assert (my_arr != NULL); //makes sure that it is actually allocated
	my_arr->capacity = capacity; 
	my_arr->size = 0; //this is because there is nothing in the array right now. This will also act like an index value
	my_arr->data = (TYPE*)malloc(sizeof(TYPE) * capacity); //this is what initializes the actual data on the array
	assert (my_arr->data != NULL);// makes sure that the data was actually assigned
	return my_arr;

}	

/* This function completely deallocates the data and 
frees all the memory of the dynamic array.
pre - a dynamic array exists. post - the dynamic array no longer exists.*/
void deleteDynArr(DynArr *myDA){
	assert(myDA != NULL && myDA->data != NULL); //just some additional checks to make sure we don't get any seg faults
	free(myDA->data); //frees up the memory of the data in the array
	free(myDA); //frees the actual array memory.
}						

/* this function simply returns the size of the dynamic array
pre - the dynamic array exists. post - n/a*/
int sizeDynArr(DynArr *myDA){
	assert(myDA != NULL && myDA->data != NULL); //just some additional checks to make sure we don't get any seg faults
	return myDA->size;
}							

/* This function will add an element to the dynamic array.
There is no set capacity function in the header file and we aren't allowed
to change it so we can assume that there is always enough capacity I guess.
pre - a dynamic array exists as well as a new value. post - the value is added to the next available spot in the dynamic array*/
void addDynArr(DynArr *myDA, TYPE value){
	assert(myDA != NULL && myDA->data != NULL); //just some additional checks to make sure we don't get any seg faults
	myDA->data[sizeDynArr(myDA)] = value; //using size (the amount of elements currently in the array) as an index
	myDA->size++; //increasing the size so as to keep track of the next empty index.
}	

/* This function returns the value at a specific index
of the dynamic array.
pre - a dynamic array exists and has data in it. post - n/a. The value gets returned*/
TYPE getDynArr(DynArr *myDA, int position){
	assert(myDA != NULL && myDA->data != NULL); //just some additional checks to make sure we don't get any seg faults
	assert(position >= 0 && position < myDA->size); //makes sure the position value you're giving is greater than zero and that it actually has data in it.
	return myDA->data[position];
}	

/* This function inserts a value into the array, and then
moves all the other elements down the array to make room for it.
pre - an array exists, the position value given is valid. post - the array is updated with the new value in the specified position and all the previous values shifted down to make room.*/
void putDynArr(DynArr *myDA, int position, TYPE value){
	assert(myDA != NULL && myDA->data != NULL); //just some additional checks to make sure we don't get any seg faults
	assert(position >= 0 && position < myDA->size); //makes sure the position value you're giving is greater than zero and that it actually has data in it.
/*	DynArr* temp_arr = newDynArr(myDA->capacity); //creates a temp array with the same capacity as the current array.
	temp_arr = myDA;
	myDA->data[position] = value; //this line inserts the value at the given index
	int pos_counter = 0;
	for(int j = position+1; j<sizeDynArr(myDA)-position; j++){ //starts on the index right after the replaced one
		myDA->data[j] = temp_arr->data[position + pos_counter];
		pos_counter++;	
	}
	deleteDynArr(temp_arr); //deletes the temp array
	*/
	myDA->data[position] = value;
}


void swapDynArr(DynArr *myDA, int idx_i, int  idx_j){
	assert(myDA != NULL && myDA->data != NULL); //just some additional checks to make sure we don't get any seg faults
	int temp = 0; //holds a value
	temp = myDA->data[idx_i];
	myDA->data[idx_i] = myDA->data[idx_j];
	myDA->data[idx_j] = temp;
}


void removeAtDynArr(DynArr *myDA, int idx_i){
	assert(myDA != NULL && myDA->data != NULL); //just some additional checks to make sure we don't get any seg faults
	DynArr* temp_arr = newDynArr(myDA->capacity); //creates a temp array with the same capacity as the current array.
	temp_arr = myDA; //sets the temp array equal to the dynamic array
	//myDA->data[idx_i] = NULL; //sets the index equal to NULL, but I don't think we need this because it will be overwritten anyways
	for (int j = idx_i; j < sizeDynArr(myDA) - idx_i; j++){
		myDA->data[j] = temp_arr->data[j+1];
	}
	myDA->size--;
}


/* ************************************************************************
	Stack Interface Functions
************************************************************************ */


/*struct Stack{
	DynArr* stackArray;
};*/

Stack *newStack(int capacity){
	Stack* myStack = (Stack*) malloc(sizeof(Stack));
	assert(myStack != NULL); //make sure that the stack variable exists.
	myStack = newDynArr(capacity); //the data type of a stack struct is a dynamic array, so we are initializing that.
	return myStack;
}


void deleteStack(Stack *myStack){
	assert(myStack != NULL && myStack->data != NULL); //just some additional checks to make sure we don't get any seg faults
	free(myStack->data);
	free(myStack);
}


int sizeStack(Stack *myStack){
	assert(myStack != NULL && myStack->data != NULL); //just some additional checks to make sure we don't get any seg faults
	return myStack->size;
}


int isStackEmpty(Stack *myStack){
	if (myStack->data != NULL){ //checks to see if the first element is empty. If it is empty we can assume the whole things is empty.
		return 0;
	}
	else{
		return 1;
	}
}


void pushStack(Stack *myStack, TYPE value){
	assert(myStack != NULL && myStack->data != NULL); //just some additional checks to make sure we don't get any seg faults
	if(isStackEmpty(myStack) == 1){
		myStack->data[0] = value;
		myStack->size++;
	}
	else{
		for (int i = myStack->size-1; i > 0; i--){ //starts at the final element and moves it down. Keeps going until the top spot in the stack is open.
			myStack->data[i+1] = myStack->data[i];
		}
		myStack->data[0] = value; //replaces the top item of the stack with the value that was passed into the function.
		myStack->size++;
	}

}


TYPE topStack(Stack *myStack){
	assert(myStack != NULL && myStack->data != NULL); //just some additional checks to make sure we don't get any seg faults
	printf("\nThe top item in the stack is %d\n", myStack->data[0]); //this is here for error handling purposes
	return myStack->data[0]; //returns the zeroeth item on the stack (the top item)
}


void popStack(Stack *myStack){
	assert(myStack != NULL && myStack->data != NULL); //just some additional checks to make sure we don't get any seg faults
	assert(isStackEmpty(myStack) == 0);
	//now we have to move everything else up.
	for (int i = 0; i < myStack->size -1; i++){
		myStack->data[i] = temp_stack->data[i+1];
	}
	
	myStack->size--;
}
	
/* ************************************************************************
	Bag Interface Functions
************************************************************************ */

Bag *newBag(int capacity){
	Bag* myBag = (Bag*)malloc(sizeof(Bag));
	assert(myBag != NULL); //make sure that the Bag exists.
	myBag = newDynArr(capacity);
	return myBag;
}


void deleteBag(Bag *myBag){
	assert(myBag != NULL && myBag->data != NULL); //just some additional checks to make sure we don't get any seg faults
	free(myBag->data);
	free(myBag);
}


int sizeBag(Bag *myBag){
	assert(myBag != NULL && myBag->data != NULL); //just some additional checks to make sure we don't get any seg faults
	return myBag->size;
}


int isBagEmpty(Bag *myBag){
	if (myBag->data != NULL){ //checks to see if the first element is empty. If it is empty we can assume the whole things is empty.
		return 0;
	}
	else{
		return 1;
	}	
}


void addBag(Bag *myBag, TYPE value){
	assert(myBag != NULL && myBag->data != NULL); //just some additional checks to make sure we don't get any seg faults
	myBag->data[sizeBag(myBag)] = value; 
	myBag->size++;
}


int containsBag(Bag *myBag, TYPE value){
	assert(myBag != NULL && myBag->data != NULL); //just some additional checks to make sure we don't get any seg faults
	for(int i = 0; i < sizeBag(myBag); i ++){
		if (myBag->data[i] == value){
			return 1;
		}
	}

	return 0;

}


void removeBag(Bag *myBag, TYPE value){
	assert(myBag != NULL && myBag->data != NULL); //just some additional checks to make sure we don't get any seg faults
	assert(containsBag(myBag, value) == 1); //makes sure that the value is actually contained somewhere in the bag.
	int counter = 0;
	while(myBag->data[counter] != value){ //loops until it can find the value in the bag
		counter++;
	} //once the while loop quits out, we'll have the exact index number that the value is located at so we can delete it.
	
	//now time to rewrite that value and then shift everything back
	for (int i = counter; i < sizeBag(myBag) - counter; i++){
		myBag->data[i] = myBag->data[i+1];
	}

}