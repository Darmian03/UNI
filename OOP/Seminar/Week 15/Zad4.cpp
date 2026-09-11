#include <iostream>
#include <fstream>

int main(){
    std::ifstream file;

    file.open("txt1.txt");

    char text[1024];
    int index = 0;
    while(file.getline(text, 1024)){
        if(text[0] == '#'){
            index++;
        }
    }

    std::cout << index;

    file.close();
}