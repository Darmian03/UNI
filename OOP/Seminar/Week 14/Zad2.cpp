#include <iostream>
#include <fstream>
#include <cstring>

int main(){
    std::ofstream file;

    file.open("txt2.txt");

    char text[1024];
    std::cin.getline(text, 1024);

    while(strlen(text) > 0){
        file << text << std::endl;
        std::cin.getline(text, 1024);
    }

    file.close();
}