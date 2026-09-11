#include <iostream>

void print(char* start, int size);
void printRev(char* start, int size);

int main()
{
    char arr[] = {"Hello World!"};
    int size = sizeof(arr)/ sizeof(arr[0]);
    char* start = arr;
    char* end = arr + size - 1;

    print(end, size-1);
    printRev(start, size);
}

void print(char* end, int size){
    if(size>=0){
        std::cout << *(end - size);
        printRev(end, size-1);
    }
}

void printRev(char* start, int size){
    if(size>=0){
        std::cout << *(start + size);
        printRev(start, size-1);
    }
}