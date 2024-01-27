import argparse
import csv
import json
import os
import requests
import sys
import zipfile
from urllib.request import urlretrieve

# avoid _csv.Error: field larger than field limit (131072)
csv.field_size_limit(sys.maxsize)


def main(
    base: str,
    outpath: str = None,
    compression: str = None,
    file_size_limit: int = None,
    limit: int = 10,
    provenance: str = None,
    asset_types: list[str] = ["dataset", "filter"],
):
    print("[socrata-dump] starting")

    if not os.path.isabs(outpath):
        raise Exception("[socrata-dump] outpath is not absolute {outpath}")

    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    if isinstance(base, str) is False:
        raise Exception("[socrata-dump] missing base")

    if base.startswith("http") is False:
        base = "https://" + base
        print('[socrata-dump] added "https://" to the start of the base')

    url = f"{base}/api/views/metadata/v1/"

    if limit:
        url += f"?limit={limit}"

    print(f"[socrata-dump] fetching {url}")
    for index, asset in enumerate(requests.get(url).json()):
        id = asset["id"]
        name = asset["name"]
        print(f'\n[socrata-dump] [{id}] {index} processing "{name}"')

        if (
            "provenance" in asset
            and isinstance(asset["provenance"], str)
            and asset["provenance"] != provenance
        ):
            print(f"[socrata-dump] [{id}] skipping asset because of its provenance")
            continue

        metadata_url = f"{base}/api/views/{id}.json"
        print(f"[socrata-dump] [{id}] fetching " + metadata_url)
        metadata = requests.get(metadata_url).json()

        if "error" in metadata:
            if "message" in metadata:
                print(metadata["message"])
                continue

        if "columns" in metadata:
            for column in metadata["columns"]:
                if "cachedContents" in column:
                    del column["cachedContents"]

        assetType = metadata["assetType"]
        print(f"[socrata-dump] [{id}] assetType:", assetType)
        if assetType not in asset_types:
            print(
                f"[socrata-dump] [{id}] skipping because it's not one of the following asset types: {(',').join(asset_types)}"
            )
            continue

        dataset_dirpath = os.path.join(outpath, id)
        if not os.path.isdir(dataset_dirpath):
            os.mkdir(dataset_dirpath)
            print(
                f'[socrata-dump] [{id}] created dataset directory "{dataset_dirpath}"'
            )

        # save metadata
        metadata_path = os.path.join(dataset_dirpath, f"{id}.metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
            print(f'[socrata-dump] [{id}] saved metadata to "{metadata_path}"')

        csv_filename = id + ".csv"

        download_csv_path = os.path.join(dataset_dirpath, csv_filename)
        download_url = f"{base}/api/views/{id}/rows.csv?accessType=DOWNLOAD"
        print(f'[socrata-dump] [{id}] downloading "{name}"')
        try:
            urlretrieve(download_url, download_csv_path)
        except Exception as e:
            # skip this asset if problem downloading
            continue
        print(f'[socrata-dump] [{id}] downloaded "{name}"')

        if compression == "zip":
            zip_path = download_csv_path + ".zip"
            with zipfile.ZipFile(
                zip_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
            ) as zip:
                zip.write(download_csv_path, "./data/{id}/{id}.csv.zip")
            os.remove(download_csv_path)

        # remove any file above file limit in the data folder
        if isinstance(file_size_limit, int):
            file_size_limit_bytes = file_size_limit * 1e6
            for filename in os.listdir(dataset_dirpath):
                filepath = os.path.join(dataset_dirpath, filename)
                if os.path.isfile(filepath):
                    filesize = os.path.getsize(filepath)
                    if filesize > file_size_limit_bytes:
                        print(
                            f"[{id}] ${zip_path} is {round(filesize / 1e6, 2)} MB, so removing"
                        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="socrata-dump",
        description="Dump Socrata Instance into a Folder, including both Metadata and Data",
    )
    parser.add_argument("base", help="base url of Socrata instance")
    parser.add_argument("outpath", help="output directory to save downloaded data")
    parser.add_argument(
        "--compression",
        type=str,
        help='type of compression to apply to csv files.  currently only valid value is "zip"',
    )
    parser.add_argument(
        "--file-size-limit",
        type=int,
        help="total max file size in megabytes.  any file larger than this will be deleted",
    )
    parser.add_argument(
        "--limit", "-l", type=int, help="total number of assets to process"
    )

    args = parser.parse_args()

    main(**vars(args))
