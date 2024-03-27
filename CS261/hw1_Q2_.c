/* CS261- Assignment 1A - Question 2
   Name:JuHyun Kim
   Date:9/28/2022
   Solution description:
*/
 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int foo(int *a, int *b, int c)
{
    // Swap the addresses stored in the pointer variables a and b
    
    int temp = *a;
    *a = *b;
    *b = temp;
    
    --c;	 // Decrement the value of integer variable c
    
    return c;
}

int main()
{
    // Declare three integers x,y and z and initialize them randomly to values in [0,10]
    
    int x = rand()%11; 
    int y = rand()%11;
    int z = rand()%11;
   
    printf("x=%d y=%d z=%d\n", x,y,z);		// Print the values of x, y and z
    
    foo(&x,&y,z);		// Call foo() appropriately, passing x,y,z as parameters
    
    printf("%d %d %p \n", x,y,z);  // Print the values of x, y and z
  
	printf("%d \n", foo);  // Print the value returned by foo
    
    return 0;
}

/*
(1) Is the return value different than the value of integer z? Why or why not?
	The value of int z was same with before and after return value. 
	But I think that the value of z should be different than the first one, because of --c; line.
	
(2) Are the values of integers x and y different before and after calling the function foo( )? Why or why not?
	The values of x and y are different before and after calling the foo( ) function.
	Because at foo( ) function, we switch each value.
	Therefore, the values of x and y are replaced and output.
	
*/
    
    



