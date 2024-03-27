/* CS261- Assignment 1A - Question 1
   Name: JuHyun Kim	
   Date: 9/27/2022
   Solution description:
*/
 
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

struct student
{
	int id;
	int score;
};

struct student* allocate()
{
    struct student* students =  malloc(10 * sizeof(struct student));      // Allocate memory for ten students*/
     
     return students;  // Return the pointer*/
}

void generate(struct student* students)
{
     /* Generate random and unique IDs and random scores for ten students, 
		IDs being between 1 and 10, scores between 0 and 100 */
   
    int i,j;
     for (i =0; i<10; i++)
    {
    	students[i].id = rand() %11;
    	
		for (j=0; j < i; j++)
		{
			if (students[i].id == students[j].id)
			{ 	
			    students[i].id = ( rand() %11 );  
				j = -1 ;		
			    
			}
		}
		    
		students[i].score = rand() %101;	//just random score like id
		
	}
    
}

void output(struct student* students)
{
     /* Output information about the ten students in the format:
        ID1 Score1
        ID2 score2
        ID3 score3
        ...
        ID10 score10*/
        
    int i;
     for (i =0; i<10; i++)
     {
         printf("%d,%d\n", students[i].id, students[i].score);
     }
      

}

void summary(struct student* students)
{
    /* Compute and print the minimum, maximum and average scores of the ten students */
    int max = students[0].score;
    int min = students[0].score;
    
    int tot=0;
    int avg=0;
    int i;
    
    for (i=0; i<10; i++) {
        if (students[i].score > max) max = students[i].score;
        if (students[i].score < min) min = students[i].score;
        
        tot += students[i].score;
        avg = tot / 10;
    }
    printf("max = %d\n", max);
    printf("min = %d\n", min);
    printf("tot= %d , avg = %d\n", tot, avg);
    
    

}

void deallocate(struct student* stud)
{
     // Deallocate memory from stud
     if (stud != NULL){
         free(stud);
     }
}

int main()
{
    struct student* stud = NULL;
    
    stud = allocate(stud);	// Call allocate
    
    generate(stud);		// Call generate
    
    output(stud);		// Call output
    
    summary(stud);		// Call summary
        
   deallocate(stud);	// Call deallocate

    return 0;
}


