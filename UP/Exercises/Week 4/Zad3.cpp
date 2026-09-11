#include <iostream>

int arithSequenceSum(int start, int difference, int n);

int main()
{
    int start,difference,n;
    std::cin >> start;
    std::cin >> difference;
    std::cin >> n;

    std::cout << arithSequenceSum(start, difference, n);
}

int arithSequenceSum(int start, int difference, int n){
    int sum = 0;
    int count = 0;
    while(count <n){
        sum += start;
        start += difference;
        count ++;
    }

    return sum;
}