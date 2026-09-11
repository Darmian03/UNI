#include <iostream>
#include <fstream>

int main(){
    std::ifstream file;

    file.open("txt1.txt");

    char text[1024];
    while(file.getline(text, 1024)){
        std::cout << text <<std::endl;
    }

    file.close();
}