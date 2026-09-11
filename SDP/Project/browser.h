#include <unordered_map>
#include <vector>
#include "tab.cpp"

class Browser
{
    private:
    std::vector<Tab> tabs;
    int currentTab;
    std::unordered_map<std::string, std::list<std::pair<std::string, Page>>> bookmarks;
    std::list<Page> history;

    public:
    Browser();

    void go(const Page&);

    void back();

    void forward();

    void newTab(const Page&);

    void closeTab();

    void switchTab(const int&);

    void viewHistory();

    void historyRemove(const std::string&);

    void clearHistory();

    void bookmark(const std::string&, const std::string&);

    void viewBookmarks(const std::string&);

    void removeBookmark(const std::string&, const std::string&);
};