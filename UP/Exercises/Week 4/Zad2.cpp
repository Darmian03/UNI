#include <iostream>

bool ifDiv(int x, int y, int div);

int main()
{
    int x,y,div;
    std::cin >> x;
    std::cin >> y;
    std::cin >> div;
    std::cout << ifDiv(x, y, div);

}

bool ifDiv(int x, int y, int div){
    if(x%div== y%div){
        return true;
    }
    else{
        return false;
    }
}