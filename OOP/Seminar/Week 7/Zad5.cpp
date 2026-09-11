#include <iostream>

const int size = 3;

bool isDiagonal(int arr[size][size]);

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

    std::cout << isDiagonal(arr);
}

bool isDiagonal(int arr[size][size]){
    int sInd = 0;

    for(int i=0; i < size; i++){
        if(arr[i][sInd] != 0){
            return false;
            break;
        }
        sInd++;
    }

    return true;
}