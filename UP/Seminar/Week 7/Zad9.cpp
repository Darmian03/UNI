#include <iostream>

int main()
{
    int arr[3][3];

    std::cout << "Board:" <<std::endl;
    for(int i=0; i<3; i++){
        std::cout << "{ ";
        for(int j=0; j<3; j++){
            std::cout << arr[i][j] << " ";
        }
        std::cout << "}" << std::endl;
    }
}