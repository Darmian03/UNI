#include <iostream>

int deFlatten(int arr[], int columns, int i, int j);

int main()
{
    int size = 0;
    std::cout << "Enter size size:";
    std::cin >> size;

    int arr[100] = {};

    for(int i = 0; i < size; i++){
        int x;
        std::cin >> x;
        arr[i] = x;
    }

    int columns,i,j;

    std::cout << "Enter number of columns: ";
    std::cin >> columns;

    std::cout << "Enter index i: ";
    std::cin >> i;

    std::cout << "Enter index j: ";
    std::cin >> j;

    std::cout << "Your element is: " << deFlatten(arr,columns,i,j);
}

int deFlatten(int arr[], int columns, int i, int j){
    int index = columns*i + j;
    return arr[index];
}