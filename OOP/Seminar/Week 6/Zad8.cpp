#include <iostream>

bool compare(int array1[], int size1, int array2[], int size2);

int main()
{
    int size1 = 0;
    std::cout << "Enter the lenght of the first array:";
    std::cin >> size1;

    int array1[100] = {};
    int array2[100] = {};

    for(int i = 0; i < size1; i++){
        int x;
        std::cin >> x;
        array1[i] = x;
    }

    int size2 = 0;
        std::cout << "Enter the lenght of the second array:";
    std::cin >> size2;

    for(int i = 0; i < size2; i++){
        int y;
        std::cin >> y;
        array2[i] = y;
    }

    std::cout << compare(array1, size1, array2, size2);
}

bool compare(int array1[], int size1, int array2[], int size2){
    for(int i = 0; i < size1; i++){
        for(int j = 0; j < size2; j++){
            if(array1[i] > array2[j]){
                return false;
                break;
            }
        }
    }
    return true;
}