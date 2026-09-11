#include "cache.h"

Cache::Node::Node(const std::string& _url,const std::string& _content): url(_url), content(_content), prev(nullptr), next(nullptr){}

Cache::Cache(): capacity(0), size(0), head(nullptr), tail(nullptr){}

Cache::Cache(const int& _capacity): capacity(_capacity), size(0), head(nullptr), tail(nullptr){}

Cache::Cache(const Cache& other)
{
    copy(other);
}

Cache::~Cache()
{
    cleanup();
}

Cache& Cache::operator=(const Cache& other)
{
    if(this != &other){
        cleanup();
        copy(other);
    }

    return *this;
}

void Cache::removeNode(Node* node)
{
	if (node->prev != nullptr) {
		node->prev->next = node->next;
	} else {
		head = node->next;
	}

	if (node->next != nullptr) {
		node->next->prev = node->prev;
	} else {
		tail = node->prev;
	}
}

void Cache::addNodeToHead(Node* node)
{
    node->next = head;
    node->prev = nullptr;
    if(head != nullptr){
        head->prev = node;
    }
    head = node;
    if(tail == nullptr){
        tail = head;
    }
}

void Cache::moveToHead(Node* node)
{
    removeNode(node);
    addNodeToHead(node);
}

Cache::Node* Cache::popTail()
{
    Node *node = tail;
    removeNode(node);
    return node;
}

void Cache::cleanup()
{
    if (head == nullptr){
        return;
    }

    Node *current = head;

    while (current != tail){
        Node *toRemove = current;
        cache.erase(toRemove->url);
        current = current->next;
        delete toRemove;
        size--;
    }

    delete current;
}

void Cache::copy(const Cache& other)
{
    size = 0;
    this->capacity = other.capacity;

    Node *currentOther = other.tail;

    while (currentOther != nullptr)
    {   
        putContent(currentOther->url, currentOther->content);
        currentOther = currentOther->prev;
    }
}

bool Cache::contains(const std::string& url)
{
    if(cache.find(url) != cache.end()){
        return true;
    }

    return false;
}

std::string Cache::getContent(const std::string& url)
{
    Node *node = cache[url];
    moveToHead(node);
    return node->content;
}

void Cache::putContent(const std::string& url, const std::string& content)
{
    if (contains(url)) {
        Node *node = cache[url];
        node->content = content;
        moveToHead(node);
    } else {
        Node *newNode = new Node(url, content);
        cache[url] = newNode;
        addNodeToHead(newNode);
        size++;

        if (size > capacity) {
            Node *tailNode = popTail();
            cache.erase(tailNode->url);
            delete tailNode;
            size--;
        }
    }
}