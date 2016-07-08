# Declare all languages with there extension and name.

# Structure : {"language" : [ details, extension ]}

default_c = """
#include <stdio.h>

int main()
{
    printf("Hello World!\\n");
    return 0;
} 
"""

default_cpp = """
#include <iostream>

using namespace std;

int main()
{
    cout << "Hello World!" << endl;
    return 0;
}
"""

default_py = """
print "Hello World!
"""

extra_data = []
code_lang = "C"

lang = {
    "C" :           ["C", default_c],
    "CPP" :         ["CPP", default_cpp],
    "PYTHON" :      ["Python (python 2.7.3)", default_py],
    # using this to pass context in form of json to teomplate
    "Info" :        {"auth": 1, "code_id":  "XXXXX","code_lang": code_lang, "extra": extra_data }
}

lang_to_ext = {
    "C":"c",
    "CPP":"cpp",
    "PYTHON":"py",
}