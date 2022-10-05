from secret import api_key

import pandas as pd
import pickle
import requests


REFRESH_DEPS = False


def get_deps(platform, name):
    per_page = 100
    page = 1

    def get_deps_page(pagenum):
        print(f"Getting page {pagenum}...")
        url = (f'https://libraries.io/api/{platform}/{name}/'
               f'dependents?api_key={api_key}'
               f'&per_page={per_page}&page={pagenum}')
        r = requests.get(url)

        if r.status_code != 200:
            raise RuntimeError(f"Status code {r.status_code}")

        js = r.json()
        print(f" - got {len(js)} entries")

        return js

    all_deps = []
    while deps := get_deps_page(page):
        all_deps += deps
        page += 1

    fname = f'{platform}-{name}.pickle'
    print(f"Writing to {fname}...")

    with open(fname, 'wb') as f:
        pickle.dump(all_deps, f)

    print("Done")


def load_deps(platform, name):
    fname = f'{platform}-{name}.pickle'
    with open(fname, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    if REFRESH_DEPS:
        get_deps('pypi', 'numba')

    deps = load_deps('pypi', 'numba')

    df = pd.DataFrame(deps)
    ranked = df.sort_values('stars', ascending=False)
    cols = ranked[['stars', 'name', 'homepage']]
    print(cols.to_string())
