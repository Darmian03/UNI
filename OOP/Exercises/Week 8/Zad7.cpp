#include <iostream>

const int x=3;
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

    std::string a = "";
    std::cout << "A = ";
    std::cin >> a;

    int arr2[y][x] = {0};

    if(a=="left"){
        for(int i=x; i>=0; i--){
            for(int j=0; j<x; j++){
                arr2[i][j] = arr1[j][i];
            }
        }

        for(int i=x-1; i>=0; i--){
            std::cout << "{ ";
            for(int j=0; j<y; j++){
                std::cout << arr2[i][j] << " ";
            }
            std::cout << "}" << std::endl;
        }
    }
    else if(a=="right"){
        for(int i=0; i<y; i++){
            for(int j=0; j<x; j++){
                arr2[i][j] = arr1[j][i];
            }
        }

        for(int i=0; i<x; i++){
            std::cout << "{ ";
            for(int j=y-1; j>=0; j--){
                std::cout << arr2[i][j] << " ";
            }
            std::cout << "}" << std::endl;
        }
    }
    else{
        std::cout << "Please input correct a.";
    }
}