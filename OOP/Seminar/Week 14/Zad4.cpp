#include <iostream>
#include <fstream>
#include <cstring>

struct Vehicle{
    char name[100];
    int speed;
};

void write(){
    std::ofstream file;
    Vehicle vhcl;

    file.open("txt4.txt", std::ios::binary);

    std::cin.getline(vhcl.name, 100);
    std::cin >> vhcl.speed;

    while(strlen(vhcl.name) > 0){
        file << vhcl.name << std::endl;
        file << vhcl.speed << std::endl;

        std::cin.getline(vhcl.name, 100);
        std::cin >> vhcl.speed;
    }
}

void read(){
    std::ifstream file;
    Vehicle vhcl;

    file.open("txt4.txt", std::ios::binary);

    file.read(vhcl.name, 100);
    file >> vhcl.speed;

    while(strlen(vhcl.name) > 0){
        std::cout << vhcl.name << std::endl;
        std::cout << vhcl.speed << std::endl;

        file.read(vhcl.name, 100);
        file >> vhcl.speed;
    }
}

int main(){
    write();
}