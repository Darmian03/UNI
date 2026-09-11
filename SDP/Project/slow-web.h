#include <random>
#include <chrono>
#include <thread>
#include "browser.cpp"
#include "cache.cpp"

class SlowWeb
{
    private:
    std::vector<Page> data;
    std::mt19937 rng;
    std::uniform_int_distribution<std::mt19937::result_type> dist;
    Browser browser;
    Cache cache;

    std::vector<std::string> split(const std::string&, char);

    std::vector<Page> readSVGFile();

    void getPageContent(const std::string&, const bool&);

    public:
    SlowWeb();

    void command(const std::string&);
};