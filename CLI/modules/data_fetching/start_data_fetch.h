#pragma once

#ifdef __cplusplus
extern "C" {
#endif

void start_data_fetch(char* api_key, char* secret_key, int num_tickers, char** tickers);

#ifdef __cplusplus
}
#endif