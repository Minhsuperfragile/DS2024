#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::string line;
    
    // Read from standard input (the list of paths)
    while (std::getline(std::cin, line)) {
        // Trim any surrounding whitespace (if necessary)
        line = line.substr(0, line.find_last_not_of(" \n\r\t") + 1);

        // Calculate the length of the path
        int length = line.length();

        // Output the length as the key, and the path as the value
        std::cout << length << "\t" << line << std::endl;
    }

    return 0;
}
