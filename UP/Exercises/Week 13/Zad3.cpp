#include <iostream>

struct Graph{
    int n;
    int **matrix = new int*[n];
};

void matrix(Graph gph){
    for(int i = 0; i < gph.n; i++){
        gph.matrix[i] = new int[gph.n];
    }

    for(int i = 0; i < gph.n; i++){
        for(int j = 0; j < gph.n; j++){
            gph.matrix[i][j] = 0;
        }
    }

    int m;
    std::cin >> m;

    for(int i = 0; i < m; i++){
        int a,b;
        std::cin >> a >> b;

        gph.matrix[a][b] = 1;
    }

    for(int i = 0; i < gph.n; i++){
        for(int j = 0; j < gph.n; j++){
            std::cout << gph.matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
};

int main(){
    Graph gph;

    std::cin >> gph.n;
    matrix(gph);
}