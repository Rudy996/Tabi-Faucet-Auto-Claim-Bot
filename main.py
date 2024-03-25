import requests
import time
import threading

def load_proxies(file_path):
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            proxies.append(line.strip())
    return proxies

def send_request(address, proxy):
    url = "https://faucet-api.testnet.tabichain.com/api/faucet"
    payload = {
        "address": address
    }
    try:
        response = requests.post(url, json=payload, proxies=proxy)
        if response.status_code == 200:
            print("Request sent successfully.")
            print("Response:")
            print(response.json())  # выводим ответ от сервера
        elif response.status_code == 429:
            print("Too Many Requests. Sleeping for 2 hours.")
            time.sleep(7200)  # засыпаем на 2 часа
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_requests(address, proxies):
    while True:
        for proxy_info in proxies:
            proxy_split = proxy_info.split(":")
            if len(proxy_split) != 4:
                print("Invalid proxy format.")
                continue

            proxy_dict = {
                "http": f"http://{proxy_split[2]}:{proxy_split[3]}@{proxy_split[0]}:{proxy_split[1]}",
                "https": f"http://{proxy_split[2]}:{proxy_split[3]}@{proxy_split[0]}:{proxy_split[1]}"
            }

            send_request(address, proxy_dict)
            time.sleep(65)  # добавляем задержку в 30 секунд перед следующим запросом

if __name__ == "__main__":
    address = "" # сюда свой кош
    proxies = load_proxies("proxy.txt")

    num_threads = len(proxies)
    threads = []

    for i in range(num_threads):
        thread = threading.Thread(target=process_requests, args=(address, [proxies[i]]))
        thread.start()
        threads.append(thread)
        time.sleep(0.1)

    for thread in threads:
        thread.join()

