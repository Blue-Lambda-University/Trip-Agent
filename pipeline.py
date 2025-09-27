

bike = BikeData.generate_urls()

bike.download_files("/Users/bluelambdauniversity/PycharmProjects/UNIVERSITY/Trip-Agent/data")

bike.create_dataframe("/Users/bluelambdauniversity/PycharmProjects/UNIVERSITY/Trip-Agent/data")

bike.save_to_s3("/Users/bluelambdauniversity/PycharmProjects/UNIVERSITY/Trip-Agent/data")