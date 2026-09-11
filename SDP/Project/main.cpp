#include "slow-web.cpp"

int main() {
    SlowWeb browser;
    std::string input;

    while (std::getline(std::cin, input)) {
        if (input.substr(0, 4) == "quit" && input.size() == 4) {
            return 0;
        }
        else{
            browser.command(input);
        }
    }
}