#include <fstream>
#include "slow-web.h"

SlowWeb::SlowWeb(): rng(std::random_device()()), dist(500, 1000)
{
    data = readSVGFile();
    Cache((int)round(sqrt(data.size())));
}

std::vector<std::string> SlowWeb::split(const std::string& elements, char separator)
{
    std::vector<std::string> result;
    std::string current;

    for (const char &c : elements)
    {
        if (c != separator)
        {
            current.push_back(c);
        }
        else
        {
            result.push_back(current);
            current = "";
        }
    }

    result.push_back(current);
    return result;
}

std::vector<Page> SlowWeb::readSVGFile()
{
    std::vector<Page> pages;
    std::ifstream file("database.svg");
    std::string line;

    while(std::getline(file, line)){
        std::vector<std::string> elements = split(line, ',');
        Page page(elements[0], elements[1]);
        pages.push_back(page);
    }

    file.close();
    return pages;
}

void SlowWeb::getPageContent(const std::string& url, const bool& command)
{
    Page result("","");

    if(cache.contains(url)){
        Page tempPage(url, cache.getContent(url));
        result = tempPage;
    }
    else{
        for (Page page : data){
            if (page.getUrl() == url){
                Page tempPage(url, page.getContent());
                result = tempPage;
                cache.putContent(result.getUrl(), result.getContent());
            }
        }
    }

    if(result.getUrl() == ""){
        std::cout << "404: Not Found" << std::endl;
    }
    else if(command){ // go
        browser.go(result);
    }
    else if(!command){ // newtab
        browser.newTab(result);
    }
}

void SlowWeb::command(const std::string& line)
{
    std::this_thread::sleep_for(std::chrono::milliseconds(dist(rng)));

    if(line.substr(0, 3) == "go "){
        std::string url = line.substr(3);
        getPageContent(url, 1);
    }
    else if(line.substr(0, 4) == "back"){
        browser.back();
    }
    else if(line.substr(0, 7) == "forward"){
        browser.forward();
    }
    else if(line.substr(0, 7) == "newtab "){
        std::string url = line.substr(7);
        getPageContent(url, 0);
    }
    else if(line.substr(0, 8) == "closetab"){
        browser.closeTab();
    }
    else if(line.substr(0, 10) == "switchtab "){
        std::string index = line.substr(10);
        int i = 0;
        for (char c : index) {
            if (c >= '0' && c <= '9') {
                i = i * 10 + (c - '0');
            }
            else {
                std::cout << "Error! Please put a valid number.";
                return;
            }
        }

        browser.switchTab(i);
    }
    else if(line.substr(0, 11) == "viewhistory"){
        browser.viewHistory();
    }
    else if(line.substr(0, 12) == "clearhistory"){
        browser.clearHistory();
    }
    else if(line.substr(0, 14) == "historyremove "){
        std::string url = line.substr(14);
        browser.historyRemove(url);
    }
    else if(line.substr(0, 9) == "bookmark "){
        std::vector<std::string> elements = split(line.substr(9), ' ');
        if(elements.size() == 2){
            browser.bookmark(elements[0], elements[1]);
        }
        else{
            browser.bookmark(elements[0], "");
        }
    }
    else if(line.substr(0, 13) == "viewbookmarks"){
        if(line.size() > 13){
            if(line[13] == ' '){
                std::string folder = line.substr(14);
                browser.viewBookmarks(folder);
            }
            else{
                std::cout << "Error! Invalid command." << std::endl;
            }
        }
        else{
            browser.viewBookmarks("");
        }
    }
    else if(line.substr(0, 15) == "removebookmark "){
        std::vector<std::string> elements = split(line.substr(15), ' ');
        if(elements.size() == 2){
            browser.removeBookmark(elements[0], elements[1]);
        }
        else{
            browser.removeBookmark(elements[0], "");
        }
    }
    else{
        std::cout << "Error! Invalid command." << std::endl;
    }
}