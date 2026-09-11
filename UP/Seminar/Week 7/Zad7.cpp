#include <iostream>

const int size = 3;

void swapLines(int arr[size][size], int l1, int l2);

int main()
{
    int arr[size][size];

    int sum = 0;
    for(int i=0; i<size; i++){
        for(int j=0; j<size; j++){
            int x = 0;
            std::cout << "Enter [" << i << "][" << j << "] element: ";
            std::cin >> x;
            arr[i][j] = x;
            sum += x;
        }
    }

    int l1,l2;
    std::cout << "Enter lines to swap:";
    std::cin >> l1;
    std::cin >> l2;

    swapLines(arr, l1, l2);

    std::cout << "Your matrix is:" <<std::endl;
    for(int i=0; i<size; i++){
        for(int j=0; j<size; j++){
            std::cout << "Matrix [" << i << "][" << j << "] = " << arr[i][j] << std::endl;
        }
    }
}

void swapLines(int arr[size][size], int l1, int l2){
    l1--;
    l2--;

    for(int i=0; i<size; i++){
        int a = arr[l1][i];
        arr[l1][i] = arr[l2][i];
        arr[l2][i] = a;
    }
}