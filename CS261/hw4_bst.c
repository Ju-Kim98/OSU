#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "bst.h"
#include "structs.h"
#pragma warning(disable : 4996)

struct Node
{
    TYPE value;
	struct Node* left;
	struct Node* right;
};

struct BSTree
{
	struct Node* root;
	int          count;
};


void preOrder(struct Node* root);

struct Node* findParent(BSTree* myTree, TYPE value);

void preOrder(struct Node* root) {
    if (root == NULL) {
        return;
    }
    print_type(root->value);
    preOrder(root->left);
    preOrder(root->right);
}



struct Node* findParent(BSTree* myTree, TYPE value) {
    assert(myTree != NULL);
    struct Node* tmp = myTree->root;
    struct Node* parent = NULL;
    while (compare(tmp->value, value) != 0) {
        if (compare(tmp->value, value) == 1) {
            parent = tmp;
            tmp = tmp->left;
        }
        else {
            parent = tmp;
            tmp = tmp->right;
        }
    }
    return parent;
}
/*----------------------------------------------------------------------------*/
//BINARY SEARCH TREE FUNCTIONS GO HERE
/*----------------------------------------------------------------------------*/

struct BSTree* newBSTree()						// Allocates and initializes the BST
{
    BSTree* newTree = (BSTree*)malloc(sizeof(BSTree));
    assert(newTree != NULL);
    newTree->root = NULL;
    newTree->count = 0;
    return newTree;
}

void deleteBSTree(BSTree* myTree)				// Deallocate nodes in BST and deallocate the BST structure
{
    assert(myTree != NULL);
    if (myTree->root == NULL) {
        free(myTree);
        return;
    }
    struct Node* tmp = myTree->root;
    while (myTree->count > 0) {
        removeBSTree(myTree, myTree->root->value);
    }
    free(myTree);
    
}

int isEmptyBSTree(BSTree* myTree)				// Returns "1" if the BST is empty or "0" if not 
{
    assert(myTree != NULL);
    if (myTree->count == 0) {
        return 1;
    }
    return 0;
}

int sizeBBSTree(BSTree* myTree)				// Returns the size of the BST
{
    assert(myTree != NULL);
    return myTree->count;
}

void addBSTree(BSTree* myTree, TYPE value)		// Adds an element into the BST
{
    assert(myTree != NULL);
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    assert(newNode != 0);
    newNode->value = value;
    newNode->left = NULL;
    newNode->right = NULL;
    if (myTree->root == NULL) {
        myTree->root = newNode;
        myTree->count++;
        return;
    }
    struct Node* tmp = myTree->root;
    while (1) {
        if (compare(tmp->value, value) == 1) {
            if (tmp->left != NULL) {
                tmp = tmp->left;
            }
            else {
                tmp->left = newNode;
                myTree->count++;
                return;
            }
        }
        else if (compare(tmp->value, value) == -1) {
            if (tmp->right != NULL) {
                tmp = tmp->right;
            }
            else {
                tmp->right = newNode;
                myTree->count++;
                return;
            }
        }
    }
}

int containsBSTree(BSTree* myTree, TYPE value)	// Returns "1" if the BST contains the specified element or "0" if not
{
    assert(myTree != NULL);
    struct Node* tmp = myTree->root;
    while (tmp != NULL) {
        if (compare(tmp->value, value) == 0) {
            return 1;
        }
        else {
            if (compare(tmp->value, value) == -1) {
                tmp = tmp->right;
            }
            else if(compare(tmp->value, value) == 1) {
                tmp = tmp->left;
            }
        }
    }
    return 0;
}

TYPE minBSTree(BSTree* myTree)					// Returns the minimum value in the BST 
{

    assert(myTree != NULL);
    assert(myTree->root != NULL);
    struct Node* minNode = myTree->root;
    while (minNode->left != NULL) {
        minNode = minNode->left;
    }
    return minNode->value;
}
TYPE maxBSTree(BSTree* myTree)					// Returns the maximum value in the BST  
{
    assert(myTree != NULL);
    assert(myTree->root != NULL);
    struct Node* maxNode = myTree->root;
    while (maxNode->right != NULL) {
        maxNode = maxNode->right;
    }
    return maxNode->value;
}

void removeBSTree(BSTree *tree, TYPE value)	// Remove the specific element from the BST
{
    assert(tree != NULL);
    assert(tree->root != NULL);
    struct Node* tmp = tree->root;
    struct Node* parent = NULL;
    while (1) {
        if (compare(tmp->value, value) == 1) {
            parent = tmp;
            tmp = tmp->left;
        }
        else if (compare(tmp->value, value) == -1) {
            parent = tmp;
            tmp = tmp->right;
        }
        else {
            if (tmp->left == NULL && tmp->right == NULL) {
                if (parent == NULL) {
                    tree->root = NULL;
                }
                else {
                    if (compare(parent->value, tmp->value) == 1) {
                        parent->left = NULL;
                    }
                    else
                    {
                        parent->right = NULL;
                    }
                }
                tmp = NULL;
                tree->count--;
                return;
            }
            else if (tmp->left != NULL && tmp->right == NULL) {
                tmp = tmp->left;
                tree->count--;
                return;
            }
            else if (tmp->left == NULL && tmp->right != NULL) {
                tmp = tmp->right;
                tree->count--;
                return;
            }
            else if (tmp->left != NULL && tmp->right != NULL) {
                struct Node* minRightNode = tmp;
                struct Node* minNodeParent = NULL;
                while (minRightNode->left != NULL) {
                    minNodeParent = minRightNode;
                    minRightNode = minRightNode->left;
                }
                minNodeParent->left = NULL;
                tree->root = minRightNode;
                minRightNode->left = tmp->left;
                minRightNode->right = tmp->right;
                tmp = NULL;
                tree->count--;
                return;
            }
        }
    }

}

void printBSTree(BSTree* myTree)				// Prints the values in the BST.
{
    assert(myTree != NULL);
    preOrder(myTree->root);
    printf("\n");
}





/*----------------------------------------------------------------------------*/

// Test value stuff -----

struct TestValues
{
    struct data* values;
    int n; //size of TestValues
};

void initValue(struct data* value, int number, const char* name)
{
    value->number = number;
    value->name = malloc((strlen(name) + 1) * sizeof(char));
    strcpy(value->name, name);
}

void freeValue(struct data* value)
{
    free(value->name);
}

struct TestValues* createValues()
{
    struct TestValues* values = malloc(sizeof(struct TestValues));
    values->n = 4;
    values->values = malloc(values->n * sizeof(struct data));
    
    initValue(&(values->values[0]), 50, "rooty");
    initValue(&(values->values[1]), 13, "lefty");
    initValue(&(values->values[2]), 110, "righty");
    initValue(&(values->values[3]), 10, "lefty of lefty");
    
    return values;
}

void destroyValues(struct TestValues* values)
{
    int i;
	for (i = 0; i < values->n; ++i)
    {
        freeValue(&(values->values[i]));
    }
    free(values->values);
    free(values);
}

// -----

void printTestResult(int predicate, char *nameTestFunction, char 
*message){
    if (predicate)
        printf("%s(): PASS %s\n",nameTestFunction, message);
    else
        printf("%s(): FAIL %s\n",nameTestFunction, message);        
}

/**
 * Tests adding 4 nodes to the BST.
 */
void testAddNode()
{
    struct TestValues* tv = createValues();
    struct BSTree *tree	= newBSTree();
    
    // Add all values to the tree
    int i;
	for (i = 0; i < tv->n; ++i)
    {
        addBSTree(tree, &(tv->values[i]));
        if (tree->count != i + 1)
        {
            printf("addNode() test: FAIL to increase count when inserting\n");
            return;
        }
    }
    
    // Check that root node is rooty
    if (tree->root->value != &(tv->values[0]))
    {
        printf("addNode() test: FAIL to insert 50 as root\n");
        return;
    }
    else
    {
        printf("addNode() test: PASS when adding 50 as root\n");
    }
    
    if (tree->root->left->value != &(tv->values[1]))
    {
        printf("addNode() test: FAIL to insert 13 as left child of root\n");
        return;
    }
    else
    {
        printf("addNode() test: PASS when adding 13 as left of root\n");
    }
    
    if (tree->root->right->value != &(tv->values[2]))
    {
        printf("addNode() test: FAIL to insert 110 as right child of root\n");
        return;
    }
    else
    {
        printf("addNode() test: PASS when adding 110 as right of root\n");
    }
    
    if (tree->root->left->left->value != &(tv->values[3]))
    {
        printf("addNode() test: FAIL to insert 10 as left child of left of root\n");
        return;
    }
    else
    {
        printf("addNode() test: PASS when adding 10 as left of left of root\n");
    }
    
    deleteBSTree(tree);
    destroyValues(tv);
}

/**
 * Tests that the BST contains the added elements,
 * and that it does not contain an element that was not added.
 */
void testContainsBSTree()
{
    struct TestValues* tv = createValues();
    struct BSTree *tree	= newBSTree();
    
    // Create value not added to the tree
    struct data notInTree;
    notInTree.number = 111;
    notInTree.name = "not in tree";
    
    // Add all other values to the tree
    int i;
	for (i = 0; i < tv->n; ++i)
    {
        addBSTree(tree, &(tv->values[i]));
    }
    
    printTestResult(containsBSTree(tree, &(tv->values[0])), "containsBSTree", "when test containing 50 as root");
    printTestResult(containsBSTree(tree, &(tv->values[1])), "containsBSTree", "when test containing 13 as left of root");
    printTestResult(containsBSTree(tree, &(tv->values[2])), "containsBSTree", "when test containing 110 as right of root");
    printTestResult(containsBSTree(tree, &(tv->values[3])), "containsBSTree", "when test containing 10 as left of left of root");
    
    printTestResult(!containsBSTree(tree, &notInTree), "containsBSTree", "when test containing 111, which is not in the tree");
    
    deleteBSTree(tree);
    destroyValues(tv);
}

/**
 * Tests leftMost.
 */
void testMinMax()
{
	struct TestValues* tv = createValues();
    BSTree* tree	= newBSTree();

    int i;
	for (i = 0; i < tv->n; ++i)
    {
        addBSTree(tree, &(tv->values[i]));
    }
	
	if(compare(minBSTree(tree), &(tv->values[3])) == 0)
		printf("Test minBSTree(): PASS\n");
    else
        printf("Test minBSTree(): FAIL\n");
	
	if(compare(maxBSTree(tree), &(tv->values[2])) == 0)
		printf("Test maxBSTree(): PASS\n");
    else
        printf("Test maxBSTree(): FAIL\n");
	
	deleteBSTree(tree);
    destroyValues(tv);
}



/**
 * Tests removal of all nodes.
 */
void testRemoveBSTree()
{
    struct TestValues* tv = createValues();
    BSTree *tree	= newBSTree();

    int i;
	for (i = 0; i < tv->n; ++i)
    {
        addBSTree(tree, &(tv->values[i]));
    }
    
	printf("Original tree:\n");
	printBSTree(tree);
	
    removeBSTree(tree, &tv->values[3]);
	printf("The tree below should not contain the value 10\n");
	printBSTree(tree);
	        
    removeBSTree(tree, &tv->values[2]);
	printf("The tree below should not contain the value 110\n");
	printBSTree(tree);
	   
    removeBSTree(tree, &tv->values[1]);
	printf("The tree below should not contain the value 13\n");
	printBSTree(tree);
        
    removeBSTree(tree, &tv->values[0]);
	printf("The tree below should be empty\n");
	printBSTree(tree);
    
    deleteBSTree(tree);
    destroyValues(tv);
}


// Main function for testing

int main(int argc, char *argv[])
{	

   /* After implementing your code, you must uncomment the following calls to the test functions and test your code. Otherwise, you will not receive any 
points */

  	testAddNode();
	
	printf("\n");
  	testContainsBSTree();
	
	printf("\n");
    testMinMax();
	
	printf("\n");
    testRemoveBSTree();
    
	return 0;
}
