/* CS261- Assignment 1A - Question 3
   Name: JuHyun Kim
   Date: 9/29/2022
   Solution description:
*/

#include <stdio.h>
#include <stdlib.h>

#define max_char_size 1000

char toUpperCase(char ch)
{
  // Convert ch to upper case, assuming it is in lower case currently
	char toReturn = ch;
    
    if(ch < 65 || ch > 90){
        toReturn = ch-32;
    }
        return toReturn;
}

char toLowerCase(char ch)
{
  // Convert ch to lower case, assuming it is in upper case currently                          
	char toReturn = ch;

    if(ch > 64 && ch < 91){
        toReturn = ch+32;
    }
    
    return toReturn;
}

int stringLength(char s[])
{
   // Return the length of the string
    int length = 0;
    while(length < max_char_size){
        if(s[length] == '\0')
        break;
        length++;
    }
    
    return length;
}

int checkIfAlpha(char c){
    if((c > 64 && c < 91) || (c > 96 && c < 123))
	return 1;
    return 0;
}

void removeCharAt (char* word, int index) {
    if(index >= 0 && index < stringLength(word)){
        int i;
        for(i = index; i < stringLength(word); i++){
            word[i] = word[i+1];
        }
    }
}

void cleanUnderscores (char* word){
    int i;
    
    for(i = 0; i < stringLength(word); i++){
        if(word[i] == 95 && word[i+1] == 95){
            removeCharAt(word, i+1);
            i--;
        }
    }
    
    if(word[0] == 95)
    	removeCharAt(word, 0);
    
    if(word[stringLength(word)-1] == 95)
    	removeCharAt(word, stringLength(word)-1);
}

int countUnderscore(char* word){
    
    int i;
    
    int numOfUnderscores = 0;
    
    for(i = 0; i < stringLength(word); i++){
        if(word[i] == 95)
        	numOfUnderscores++;
    }
	
	//return the number of underscores
    return numOfUnderscores;
}

void camelCase(char* word)
{
	// Convert to camelCase
	int i;  
    for (i = 0; i < stringLength(word); i++) {
        word[i] = toLowerCase(word[i]);
    }
    
    for(i = 0; i < stringLength(word); i++){
        if(word[i] == 95){
            word[i+1] = toUpperCase(word[i+1]);
            removeCharAt(word, i);
        }
    }
	
	
}

int main()
{
    char * word = (char*) malloc(sizeof(char)* max_char_size);	//Dynamically allocate char array so that the string is mutable.

	// Read the string from the keyboard
	printf("Enter String: ");
    scanf("%s", word);
	
	//Clean up the input by converting all nonletters to '_'
    int i;
    for(i = 0; i < stringLength(word); i++){
        if(!checkIfAlpha(word[i]))
        word[i] = 95;
    }
    
    //Remove multiple '_'
    cleanUnderscores(word);
    
    //We can safely count words at this point and determine if there are more than one word.
    if(countUnderscore(word) < 1){
    	printf("invalid input string\n");
    	free(word);
    	exit(1);
    }
	
	// Call camelCase
	camelCase(word);
	
	// Print the new string
	printf("%s\n",word);
    free(word);
	
	return 0;
}


