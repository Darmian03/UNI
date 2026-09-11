#include <iostream>
#include <climits>

const int size = 3;

void biggestElem(int arr[size][size]);

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

    biggestElem(arr);
}

void biggestElem(int arr[size][size]){
    int counter = 1;

    for(int i=0; i<size; i++){
        int maxElem = INT_MIN;
        for(int j=0; j<size; j++){
            if(arr[i][j] > maxElem){
                maxElem = arr[i][j];
            }
        }

        std::cout << "Line " << counter << ": " << maxElem << std::endl;
        counter++;
    }
}