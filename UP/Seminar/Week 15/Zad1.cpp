#include <iostream>

bool simetricMatrix(int **matrix, int n){
    for(int i = 0; i < n; i++){
        for(int j = 0; j < n; j++){
            if(matrix[i][j] != matrix[j][i]){
                return false;
                break;
            }
        }
    }

    return true;
}

int main(){
    int n = 0;
    std::cout << "n = ";
    std::cin >> n;

    int **matrix = new int*[n];
    for(int i = 0; i < n; i++){
        matrix[i] = new int[n];
    }

    for(int i = 0; i < n; i++){
        for(int j = 0; j < n; j++){
            std::cin >> matrix[i][j];
        }
    }

    std::cout << simetricMatrix(matrix, n);

    delete[] matrix;
}