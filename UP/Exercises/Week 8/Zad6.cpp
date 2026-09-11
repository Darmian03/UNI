#include <iostream>

const int x=4;
const int y=3;

int main()
{
    int arr[x][y] = {0};

    for(int i=0; i<x; i++){
        for(int j=0; j<y; j++){
            int index = 0;
            std::cin >> index;
            arr[i][j] = index;
        }
    }

    for(int i=x-1; i>=0; i--){
        std::cout << "{ ";
        for(int j=0; j<y; j++){
            std::cout << arr[i][j] << " ";
        }
        std::cout << "}" << std::endl;
    }
}