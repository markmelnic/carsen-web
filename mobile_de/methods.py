import scalg

from mobile_de.scraper import *

# perform a detailed search of each listing
def search(search_params: list, db=False) -> list:
    if db:
        current_url, pagesnr, database = search_url(search_params, db)
    else:
        current_url, pagesnr = search_url(search_params, db)

    # get links
    car_links = []
    for i in range(pagesnr):
        for link in get_page_listings(current_url):
            car_links.append(link)
        current_url = next_page(current_url, i + 1)

    assert len(car_links) != 0

    data = [get_data(link) for link in car_links]
    data = scalg.score_columns(data, [2, 3, 4], [0, 1, 0])

    if db:
        return database, data
    else:
        return data


# perform a surface search for the generated url
def surface_search(search_params: list, db=False) -> list:
    if db:
        current_url, pagesnr, database = search_url(search_params, db)
    else:
        current_url, pagesnr = search_url(search_params, db)

    data = []
    for i in range(pagesnr):
        for item in surface_data(current_url):
            data.append(item)
        current_url = next_page(current_url, i + 1)

    assert data != []

    data = scalg.score_columns(data, [2, 3, 4], [0, 1, 0])
    data.sort(key=lambda d: d[-1])

    undup = []
    undup_indexes = []
    for i, d in enumerate(data):
        if d[-1] in undup:
            undup_indexes.append(i)
        else:
            undup.append(d[-1])
    for i in sorted(undup_indexes, reverse=True):
        del data[i]

    return (data, database) if db else data


# existing searches checker
def checker(data: list) -> list:
    changed = False
    changed_data = []
    for item in data:
        new_price = check_car_price(item[0])
        if not float(new_price) == float(item[2]):
            changed = True
            item.append(new_price - item[2])
            changed_data.append(item)

    assert changed
    return changed_data
