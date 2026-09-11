#include <iostream>

const int x=2;
const int y=3;

int main()
{
    int arr1[x][y] = {0};

    for(int i=0; i<x; i++){
        for(int j=0; j<y; j++){
            int index = 0;
            std::cin >> index;
            arr1[i][j] = index;
        }
    }

    int arr2[y][x] = {0};

    for(int i=0; i<y; i++){
        for(int j=0; j<x; j++){
            arr2[i][j] = arr1[j][i];
        }
    }

    for(int i=0; i<y; i++){
        std::cout << "{ ";
        for(int j=0; j<x; j++){
            std::cout << arr2[i][j] << " ";
        }
        std::cout << "}" << std::endl;
    }
}