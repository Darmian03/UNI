#include "browser.h"
    
Browser::Browser()
{
    tabs.push_back(Tab());
    currentTab = 0;
}

void Browser::go(const Page& page)
{
    tabs[currentTab].visit(page);
    history.push_front(page);
}

void Browser::back()
{
    try{
        Page currentPage("", "");
        currentPage = tabs[currentTab].getPage();
        tabs[currentTab].back();

        if(currentPage.getUrl() != tabs[currentTab].getPage().getUrl()){
            history.push_front(tabs[currentTab].getPage());
        }
    }
    catch(std::invalid_argument& e){
        std::cout << "Error! The current tab doesn't have a opened page." << std::endl;
    }
}

void Browser::forward()
{
    try{
        Page currentPage("", "");
        currentPage = tabs[currentTab].getPage();
        tabs[currentTab].forward();
        
        if(currentPage.getUrl() != tabs[currentTab].getPage().getUrl()){
            history.push_front(tabs[currentTab].getPage());
        }
    }
    catch(std::invalid_argument& e){
        std::cout << "Error! The current tab doesn't have a opened page." << std::endl;
    }
}

void Browser::newTab(const Page& page)
{
    tabs.push_back(Tab(page));
    currentTab = tabs.size() - 1;
    history.push_front(page);
}

void Browser::closeTab()
{
    tabs.erase(tabs.begin() + currentTab);

    if(currentTab >= tabs.size()){
        if(!tabs.empty()){
            --currentTab;
            std::cout << tabs[currentTab].getPage().getContent() << std::endl;
            return;
        }

        tabs.push_back(Tab());
        currentTab = 0;
    }
    else{
        std::cout << tabs[currentTab].getPage().getContent() << std::endl;
    }
}

void Browser::switchTab(const int& index)
{
    int oldTab = currentTab;
    if(index < 0){
        currentTab = 0;
    }
    else if(index >= tabs.size()){
        currentTab = tabs.size() - 1;
    }
    else{
        currentTab = index;
    }

    if(oldTab == currentTab){
        std::cout << "Huh. You went on the same tab you were just in." << std::endl;
        return;
    }

    std::cout << tabs[currentTab].getPage().getContent() << std::endl;
}

void Browser::viewHistory()
{
    if(history.empty()){
        std::cout << "Huh. There is no history." << std::endl;
    }
    for(Page page : history){
        std::cout << page.getUrl() << std::endl;
    }
}

void Browser::historyRemove(const std::string& url)
{
    history.remove_if([&url](Page value) { return value.getUrl() == url; });

    std::cout << "Done!" << std::endl;
}

void Browser::clearHistory()
{
    history.clear();
    std::cout << "History cleared." << std::endl;
}

void Browser::bookmark(const std::string& name, const std::string& folder)
{
    Page current = tabs[currentTab].getPage();

    if(bookmarks.find(folder) == bookmarks.end()){
        bookmarks[folder] = std::list<std::pair<std::string, Page>>();
    }

    bookmarks[folder].push_back({name, current});
    std::cout << "Done!" << std::endl;
}

void Browser::viewBookmarks(const std::string& folder)
{
    if(bookmarks.find(folder) != bookmarks.end()){
        for(std::pair<std::string, Page> name : bookmarks[folder]){
            std::cout << name.first << std::endl;
        }
    }
    else{
        std::cout << "Error! Folder " << folder << " does not exist." << std::endl;
    }
}

void Browser::removeBookmark(const std::string& name, const std::string& folder)
{
    if(bookmarks.find(folder) != bookmarks.end()){
        bookmarks[folder].remove_if([&name](const std::pair<std::string, Page>& value) { return value.first == name; });

        std::cout << "Done!" << std::endl;
    }
    else{
        std::cout << "Error! Folder " << folder << " or Name " << name <<" does not exist!" << std::endl;
    }
}