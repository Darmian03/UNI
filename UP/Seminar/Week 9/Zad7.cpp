#include <iostream>

void print(char arr[], int size);

int main()
{
    char arr[] = {"abcdedcba"};
    int size = sizeof(arr)/ sizeof(arr[0]);

    print(arr, size-1);
}

void print(char arr[], int size){
}