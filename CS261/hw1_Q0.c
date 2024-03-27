/* CS261- Assignment 1A - Question 0
   Name: JuHyun Kim
   Date: 9/27/2022
   Solution description:
*/
 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fooA(int* iptr)
{   
    printf("%d %p\n", *iptr, iptr);  // Print the value and address of the integer pointed to by iptr
    
    (*iptr) += 5;   // Increment the value of the integer pointed to by iptr by 5
    
    printf("%p\n", &iptr); 	// Print the address of iptr itself
  
}


void fooB(int* jptr)
{
    printf("%d %p\n", *jptr, jptr);   // Print the value and address of the integer pointed to by jptr
    
    (*jptr) -= 1;         // Decrement jptr by 1
      
     printf("%p\n", &jptr); 	// Print the address of jptr itself
}


int main()
{
    int x = rand() % 11;  	// Declare an integer x and initialize it randomly to a value in [0,10]
    
    printf("%d %p\n", x, &x); 	// Print the value and address of x
    
    fooA(&x); 		// Call fooA() with the address of x   
    
    printf("%d\n", x);   // Print the value of x
    
    /*
	Is the value of x different than the value that was printed at first? Why or why not? 
		The value of x was different from first time. Pointer iptr at fooA function points value and address of x.
		The code increase the value of iptr by 5, so the x value also increase 5. that's why the output of x agfer call fooA is different.	*/
    
        
    fooB(&x);		// Call fooB() with the address of x
    
    printf("%d", x);	// Print the value and address of x
 
    /*
     Are the value and address of x different than the value and address that were printed before the call to fooB( )? Why or why not?
     	The address of x was same but the value of x was different. We decrease the value of jptr by 1 but it just change the value of it, not change the address.
		 so the address of jptr was priented.
	*/
    
    return 0;
}





