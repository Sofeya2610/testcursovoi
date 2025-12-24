#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

const int WORD_LENGTH = 5;

// глобальні змінні
string TARGET_WORD = "";
bool HINT_USED = false;   // чи вже була підказка в цій грі

// завантаження словника (англійські 5-літерні слова)
vector<string> load_dictionary(const string &filename) {
    vector<string> words;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Cannot open dictionary file: " << filename << endl;
        return words;
    }

    string line;
    while (getline(file, line)) {
        // прибрати пробіли
        line.erase(remove_if(line.begin(), line.end(), ::isspace), line.end());
        if (line.empty()) continue;

        // зробити верхній регістр
        transform(line.begin(), line.end(), line.begin(), ::toupper);

        if ((int)line.size() == WORD_LENGTH) {
            words.push_back(line);
        }
    }

    return words;
}

// генерація фідбеку (G/Y/B) для англійського слова
string generate_feedback(const string &guess, const string &target) {
    int n = WORD_LENGTH;
    string res(n, 'B');
    vector<bool> used_target(n, false);

    // спочатку G
    for (int i = 0; i < n; ++i) {
        if (guess[i] == target[i]) {
            res[i] = 'G';
            used_target[i] = true;
        }
    }

    // потім Y
    for (int i = 0; i < n; ++i) {
        if (res[i] == 'G') continue;
        for (int j = 0; j < n; ++j) {
            if (!used_target[j] && guess[i] == target[j]) {
                res[i] = 'Y';
                used_target[j] = true;
                break;
            }
        }
    }

    return res;
}

// повертає підказку: позицію і букву, або "-1 -" якщо підказку вже використали
string get_hint() {
    if (TARGET_WORD.empty()) return "-1 -";
    if (HINT_USED) return "-1 -";

    vector<int> positions;
    for (int i = 0; i < WORD_LENGTH; ++i) {
        positions.push_back(i);
    }
    int idx = rand() % positions.size();
    int pos = positions[idx];

    HINT_USED = true;

    // формат: "index letter"
    string result = to_string(pos) + " " + string(1, TARGET_WORD[pos]);
    return result;
}

int main() {
    srand((unsigned)time(nullptr));

    vector<string> dictionary = load_dictionary("english_words.txt");
    if (dictionary.empty()) {
        cerr << "Empty dictionary." << endl;
        return 1;
    }

    string input;
    while (getline(cin, input)) {
        // прибрати \r і пробіли
        input.erase(remove(input.begin(), input.end(), '\r'), input.end());
        input.erase(remove_if(input.begin(), input.end(), ::isspace), input.end());

        // в верхній регістр
        transform(input.begin(), input.end(), input.begin(), ::toupper);

        if (input == "START") {
            int index = rand() % dictionary.size();
            TARGET_WORD = dictionary[index];
            HINT_USED = false;

            cerr << "TARGET: " << TARGET_WORD << endl;  // debug, можна прибрати

            cout << "READY " << WORD_LENGTH << endl;
            cout.flush();
        }
        else if (input == "HINT") {
            string hint = get_hint();
            cout << "HINT " << hint << endl;
            cout.flush();
        }
        else if ((int)input.size() == WORD_LENGTH) {
            if (TARGET_WORD.empty()) {
                cout << "ERROR: WORD NOT SET" << endl;
                cout.flush();
                continue;
            }

            string feedback = generate_feedback(input, TARGET_WORD);

            if (feedback == string(WORD_LENGTH, 'G')) {
                cout << "WIN " << feedback << endl;
            } else {
                cout << "FEEDBACK " << feedback << endl;
            }
            cout.flush();
        }
        else {
            cout << "INVALID" << endl;
            cout.flush();
        }
    }

    return 0;
}
