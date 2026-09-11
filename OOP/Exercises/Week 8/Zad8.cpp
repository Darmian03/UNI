#include <iostream>

const int x=4;
const int y=4;

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

    int a = 0;
    int b = 0;

    while(a<x){
        if(b==x-1){
            while(b>=0){
                std::cout << arr[a][b] << " ";
                b--;
            }
            b++;
        }
        else if(b==0){
            while(b<x){
                std::cout << arr[a][b] << " ";
                b++;
            }
            b--;
        }
        a++;
    }
}