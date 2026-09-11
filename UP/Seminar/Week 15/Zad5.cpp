#include <iostream>

bool famous(int *arr, int n){
    int sum = 0;
    for(int i = 0; i < n; i++){
        sum += arr[i];
    }

    if(sum == n){
        return true;
    }
    else{
        return false;
    }
}

void friendships(int **matrix, int n){
    for(int i = 0; i < n; i++){
        if(famous(matrix[i], n)){
            std::cout << i+1;
        }
    }
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

    friendships(matrix, n);

    delete[] matrix;
}