#include <iostream>

int main()
{
    int n = 0;
    std::cout << "Enter size N:";
    std::cin >> n;

    int arr[100][100];

    int sum = 0;
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            int x = 0;
            std::cout << "Enter [" << i << "][" << j << "] element: ";
            std::cin >> x;
            arr[i][j] = x;
            sum += x;
        }
    }

    std::cout << sum;
}