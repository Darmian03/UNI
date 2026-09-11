#include <iostream>
#include <Windows.h>

int main(){
    int a = 0;
    while(a == 0){
    int x;
    std::cout << "Please enter a number between 0 and 7: ";
    std::cin >> x;

    switch(x){
        case 0:
        a++;
        break;
        case 1:
        Beep(130.81, 1000);
        break;
        case 2:
        Beep(146.83, 1000);
        break;
        case 3:
        Beep(164.81, 1000);
        break;
        case 4:
        Beep(174.61, 1000);
        break;
        case 5:
        Beep(196.00, 1000);
        break;
        case 6:
        Beep(220.00, 1000);
        break;
        case 7:
        Beep(246.94, 1000);
        break;
        default:
        std::cout << "Please enter a number between 0 and 7!";
    }
    }
    return 0;
}