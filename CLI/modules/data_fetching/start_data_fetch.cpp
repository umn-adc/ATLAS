#include "start_data_fetch.h"
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <string>
#include <sstream>

using json = nlohmann::json;

void start_data_fetch(char* api_key, char* secret_key, int num_tickers, char** tickers) {
    if (!api_key || !secret_key || num_tickers <= 0 || !tickers) {
        std::cerr << "ERROR: invalid arguments to start_data_fetch.\n";
        return;
    }

    // Build the comma-separated "symbols" query parameter from the ticker array.
    std::ostringstream symbols;
    for (int i = 0; i < num_tickers; ++i) {
        if (i > 0) symbols << ",";
        symbols << tickers[i];
    }

    std::cout << "Sending Alpaca API request for symbols: " << symbols.str() << "\n";

    cpr::Response r = cpr::Get(
        cpr::Url{"https://data.alpaca.markets/v2/stocks/bars/latest"},
        cpr::Header{
            {"Accept", "application/json"},
            {"APCA-API-KEY-ID", api_key},
            {"APCA-API-SECRET-KEY", secret_key}
        },
        cpr::Parameters{{"symbols", symbols.str()}}
    );

    if (r.status_code == 200) {
        // SAFETY CHECK: Does the response text look like an HTML error page?
        if (!r.text.empty() && r.text[0] == '<') {
            std::cerr << "CRITICAL ERROR: Server returned HTML code instead of JSON!\n";
            std::cerr << "--- Server Output Snippet ---\n" << r.text.substr(0, 300) << "\n-----------------------\n";
            return;
        }

        try {
            json data = json::parse(r.text);

            // Alpaca returns { "bars": { "AAPL": { ... }, "TSLA": { ... } }, ... }
            auto bars = data["bars"];

            for (int i = 0; i < num_tickers; ++i) {
                std::string sym = tickers[i];

                if (!bars.contains(sym)) {
                    std::cout << "--- " << sym << ": no bar data returned ---\n";
                    continue;
                }

                auto bar = bars[sym];
                double open  = bar["o"];
                double high  = bar["h"];
                double low   = bar["l"];
                double close = bar["c"];
                long volume  = bar["v"];
                std::string timestamp = bar["t"];

                std::cout << "--- " << sym << " ---\n";
                std::cout << "Timestamp: " << timestamp << "\n";
                std::cout << "Open:   $" << open << "\n";
                std::cout << "High:   $" << high << "\n";
                std::cout << "Low:    $" << low << "\n";
                std::cout << "Close:  $" << close << "\n";
                std::cout << "Volume: " << volume << "\n";
            }
        }
        catch (const json::parse_error& e) {
            std::cerr << "JSON Parsing failed: " << e.what() << "\n";
        }
        catch (const json::out_of_range& e) {
            std::cerr << "Missing expected field in JSON: " << e.what() << "\n";
        }
    } else {
        std::cerr << "Request failed with HTTP status code: " << r.status_code << "\n";
        std::cerr << "Response body: " << r.text << "\n";
    }
}