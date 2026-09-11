#include <iostream>

int absolute(int x);
bool isEven(int x);
char toLower(char sym);
void printAll(int from, int until);

int main()
{
    int x;
    std::cin >> x;
    std::cout << absolute(x) << " " << isEven(x);

}

int absolute(int x){
    if(x>=0){
        return x;
    }
    else{
        return -x;
    }
}

bool isEven(int x){
    if(x%2 == 0){
        return true;
    }
    else{
        return false;
    }
}

char toLower(char sym){
    if(sym > 64 && sym <91){
        return sym + 22;
    }
    else{
        return 0;
    }
}

void printAll(int from, int until){
    while(from<=until){
        std::cout << from << std::endl;
        from++;
    }
}