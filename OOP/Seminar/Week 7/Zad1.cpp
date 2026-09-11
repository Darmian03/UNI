#include <iostream>

int main()
{
    int n = 0;
    std::cout << "Enter size N:";
    std::cin >> n;

    int arr[100][100];

    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            int x = 0;
            std::cout << "Enter [" << i << "][" << j << "] element: ";
            std::cin >> x;
            arr[i][j] = x;
        }
    }

    std::cout << "Your matrix is:" <<std::endl;
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            std::cout << "Matrix [" << i << "][" << j << "] = " << arr[i][j] << std::endl;
        }
    }
}