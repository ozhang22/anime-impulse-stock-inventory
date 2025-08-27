from pyscript import fetch
import asyncio
from datetime import datetime
from time import sleep

# AIOC
async def aioc():
    map = {
        "RZIL01":   "Ren Zotto            Sun 08/31  1:45PM",
        "RZIL02":   "Ren Zotto            Sun 08/31  3:15PM",
        "GGAV01":   "Gale Galleon         Sun 08/31  5:00PM",
        "ZNAV01":   "Zander Netherbrand   Sun 08/31  5:00PM",
        "RGAV01":   "Rosco Graves         Sun 08/31  5:00PM",
        "CFAV01":   "Cassian Floros       Sun 08/31  5:00PM",
        "LLAV01":   "Lucien Lunaris       Sun 08/31  5:00PM",
        "PGOB01":   "Petra Gurin          Sun 08/31  6:30PM",
        "SQ8701527":"Petra Gurin          Sun 08/31  7:35PM",
        "NXRV01":   "Nix Voltare          Sat 08/30  4:45PM",
        "MCRV01":   "Malim Cendari        Sat 08/30  4:45PM",
        "RBRV01":   "Ryzar Blazenfang     Sat 08/30  4:45PM",
        "AZRV01":   "Altus Zendoji        Sat 08/30  4:45PM",
        "NURV01":   "Nayuta Umbrage       Sat 08/30  4:45PM",
        "UNSAT01":  "Unnämed Meet&Grip    Sat 08/30  9:00PM",
    } 

    catalog = {
        # FSP
        "BZOgOET0D1jSM2Y2NTI3NjcxMzUzZTVjZmY1ZDhkMDZmY2ZiOTgw": [
            "686edf3a7bd5232891d938eb",
            "686ef9f7f08d7b61302dcb1d",
            "686efa772f6026214416a9d2",
            "686efb6c0969407cb651ec43",
            "686efeae27a54e75fd809e48",
            "6792c3c73840ee70ff30120d",
            "6792c2afd71db53c7a5709d4",
            "6792c599ee752800eeac8ac4",
            "6792c472a491d70de23f7a42",
            "678859129ba2a11328064c39",
        ],
        # Unnamed
        "BUyBl7D21w26NzljYjVlZjFmYjdlMTVhMjUyZWJjZDA2MTMxYTI4" : [
            "68758da34bbb5f4b29f31eb8"
        ],
        # Nijisanji
        "BdPHFNu3KUvaZDhjOGQ1NGNmNTM5NjEwNDYxZjNkOGU0NjRkMGEy" : [
            "66bbe90091c1d110415bee5b",
            "66e4c9b07e763c11bb526cd3",
        ],
    }

    async def make_http_request(crumb, itemId):
        retries = 0
        while (retries < 3):
            try:
                link = f"https://animeimpulse.com/api/commerce/inventory/stock/?crumb={crumb}&itemId={itemId}"
                response = await fetch(url=link, method="GET")

                if response.status_code == 200:
                    response_results = (await response.json())['results']
                    for item in response_results:
                        results[item['sku']] = item['qtyInStock']
                        links[item['sku']] = link
                    
                    return

                print(f"Request failed with status code: {response.status_code}. Response Text: {response.text}")
                retries += 1

                sleep(2)
            
            except requests.exceptions.RequestException as e:
                print(f"An error occurred for {itemId}: {e}")
                retries += 1

                sleep(2)

    results = {}
    links = {}
    for crumb, itemIds in catalog.items():
        for itemId in itemIds:
            await make_http_request(crumb, itemId)
            sleep(2)

    print("```")
    print("Anime Impulse Orange County Tickets Remaining")
    print(f"As of {datetime.now():%-m/%-d/%Y %-I:%M:%S%p} PDT:")
    for key, value in results.items():
        if (value > 0):
            print(f"{map[key]} {value} {links[key]}")
            
    print("```")

asyncio.run(aioc())
