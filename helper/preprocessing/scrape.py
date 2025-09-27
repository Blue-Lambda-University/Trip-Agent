"""Download .zip files """
import requests
from datetime import datetime
import io
import os
from io import BytesIO
import zipfile
import pandas as pd

# from ..aws_helper.s3 import S3Handler
from helper.aws_helper.s3 import S3Handler


# TODO: cleanup and modularize script
# TODO: create class to hold all the methods
# TODO: parametarize the arguments/ no hardcoding
# TODO: fix requests function and download all files
# TODO: Extract content of .zip file - use `import zipfile`
# TODO: Merge all .zip files into one big file
# TODO: Load data to S3 and move to

# Link to Website: https://s3.amazonaws.com/capitalbikeshare-data/index.html


def generate_year(start: int = 2010,
                  monthly_data_begins: int = 2018,
                  end: int = datetime.now().year) -> list[str]:
    """Dynamically generate the years holding the files to download."""
    now = datetime.now()
    years = []
    months = [f"{i:02d}" for i in range(1, 13)]

    for year in range(start, end + 1):
        if year >= start and year < monthly_data_begins:
            years.append(str(year))
        else:
            if year != now.year:
                for month in months:
                    years.append(str(year) + month)
            else:
                months = [f"{i:02d}" for i in range(1, now.month)]
                for month in months:
                    years.append(str(year) + month)
    return years


class BikeData():
    @classmethod
    def generate_urls(cls):
        """Generate URLS for all files"""
        def construct_url_template(year: str):
            return f"https://s3.amazonaws.com/capitalbikeshare-data/{year}-capitalbikeshare-tripdata.zip"
        urls = []
        years = generate_year()
        for year in years:
            urls.append(construct_url_template(year))

        return cls(urls=urls)

    def __init__(self, urls: list):
        self.urls = urls

    def download_file(url, filename):

    """Download zip file and extract csv component"""
        response = requests.get(url)
        data = BytesIO(response.content)

        with ZipFile(data, 'r') as zf:
            if filename:
                with zf.open(filename) as csv_file:

                    df = pd.read_csv(csv_file)
                    print(df.info())
            else:
                print("No CSV file found in the ZIP archive.")
        return data

    def download_files(self, out_dir: str):
        """Download and extract all files."""

        # TODO create the out_dir
        for url in self.urls[:10]:
            try:
                response = requests.get(url)
                response.raise_for_status()

                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    for member in z.namelist():
                        if member.startswith("__MACOSX/"):
                            continue
                        z.extract(member, out_dir)

                print(f" Extracted {url} to {out_dir}")

            except requests.exceptions.HTTPError as e:
                print(f"Failed to download {url}: {e}")
            except zipfile.BadZipFile:
                print(f" Skipping {url} (not a valid ZIP).")

    def create_dataframe(self, out_dir: str):
        """Create dataframe"""
        final_df = pd.DataFrame()

        for filename in os.listdir(out_dir):
            df = pd.read_csv(f"{out_dir}/{filename}")
            final_df = pd.concat([final_df, df])

        final_df.to_csv("data.csv", index=False)
        print(final_df)

    def save_to_s3(self, out_dir: str):
        """Save dataframe to s3 bucket"""
        s3_handler = S3Handler()
        s3_handler.upload_csv("bluelambdalambda",
                              f"{out_dir}/data.csv")

bike = BikeData.generate_urls()

bike.download_files("/Users/bluelambdauniversity/PycharmProjects/UNIVERSITY/Trip-Agent/data")

bike.create_dataframe("/Users/bluelambdauniversity/PycharmProjects/UNIVERSITY/Trip-Agent/data")

bike.save_to_s3("/Users/bluelambdauniversity/PycharmProjects/UNIVERSITY/Trip-Agent/data")

# # Step 1: Construct URL
# def construct_url_template(year: str):
#     return f"https://s3.amazonaws.com/capitalbikeshare-data/{year}-capitalbikeshare-tripdata.zip"
#
#
# # Step 2:
#
# def generate_year(start: int = 2010,
#                   monthly_data_begins: int = 2018,
#                   end: int = datetime.now().year) -> list[str]:
#     """Dynamically generate the years holding the files to download."""
#     now = datetime.now()
#     years = []
#     months = [f"{i:02d}" for i in range(1, 13)]
#
#     for year in range(start, end + 1):
#         if year >= start and year < monthly_data_begins:
#             years.append(str(year))
#         else:
#             if year != now.year:
#                 for month in months:
#                     years.append(str(year) + month)
#             else:
#                 months = [f"{i:02d}" for i in range(1, now.month)]
#                 for month in months:
#                     years.append(str(year) + month)
#     return years
#
#
# def generate_urls():
#     """Generate URLS for all files"""
#     urls = []
#     years = generate_year()
#     for year in years:
#         urls.append(construct_url_template(year))
#     return urls
#
#
# def generate_filenames():
#     file_names = []
#     urls = generate_urls()
#     for url in urls:
#         file_names.append(url.split("/")[-1].replace("zip", "csv"))
#     return file_names
#
#
# def download_file(url, filename):
#     """Download zip file and extract csv component"""
#     response = requests.get(url)
#     data = BytesIO(response.content)
#
#     with ZipFile(data, 'r') as zf:
#         if filename:
#             with zf.open(filename) as csv_file:
#
#                 df = pd.read_csv(csv_file)
#                 print(df.info())
#         else:
#             print("No CSV file found in the ZIP archive.")
#     return data
#
#
# df = download_file(
#     "https://s3.amazonaws.com/capitalbikeshare-data/202507-capitalbikeshare-tripdata.zip",
#     "202507-capitalbikeshare-tripdata.csv")