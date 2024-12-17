#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string line;
    std::vector<std::string> longestPaths;
    int longestLength = 0;

    // Read input from stdin
    while (std::getline(std::cin, line)) {
        // Separate the key (length) and value (path) by tab
        size_t tabPos = line.find('\t');
        int length = std::stoi(line.substr(0, tabPos));
        std::string path = line.substr(tabPos + 1);

        // Compare the path length
        if (length > longestLength) {
            longestPaths.clear();    // Clear previous paths
            longestPaths.push_back(path);  // Store the new longest path
            longestLength = length;  // Update the longest length
        } else if (length == longestLength) {
            longestPaths.push_back(path);  // Add another path of the same length
        }
    }

    // Output the longest path(s)
    for (const std::string& path : longestPaths) {
        std::cout << path << std::endl;
    }

    return 0;
}
