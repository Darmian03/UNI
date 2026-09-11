#include <iostream>
#include <fstream>
#include <cmath>

int main(){
    std::ifstream file;

    file.open("txt3.txt");

    int size;
    file >> size;

    double sum = 0;
    int a,b;

    file >> a >> b;

    for(int i = 1; i < size; i++){
        int c,d;

        file >> c >> d;

        sum += sqrt((a-c)*(a-c) + (b-d)*(b-d));

        a = c;
        b = d;
    }

    std::cout << sum;

    file.close();
}