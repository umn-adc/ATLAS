#include "start_data_fetch.h"

int main() {
    char api_key[] = "PKR3IHCW22Q3IIWPTQRUNJINWC";
    char secret_key[] = "DuWbkQSo1ZvsjJfCi3eYpSeNbqoLNg4t3TcDEZjFL2az";
    char aapl[] = "AAPL";
    char tsla[] = "TSLA";
    char msft[] = "MSFT";
    char* tickers[] = { aapl, tsla, msft };

    start_data_fetch(api_key, secret_key, 3, tickers);
    return 0;
}