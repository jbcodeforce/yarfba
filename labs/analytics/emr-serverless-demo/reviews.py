import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
if __name__ == "__main__":
    print(len(sys.argv))
    if (len(sys.argv) != 4):
        print("Usage: spark-etl [input-folder] [output-folder1] [output-folder2]")
        sys.exit(0)
    spark = SparkSession.builder.appName("SparkETL").getOrCreate()
    reviews = spark.read.json(sys.argv[1])
    reviews.createOrReplaceTempView('reviews')
    reviews_by_productcategory=spark.sql("select  product_category, stars , count(*) as number_of_reviews from reviews group by product_category , stars order by product_category, stars ")
    reviews_by_productcategory.write.mode("OVERWRITE").parquet(sys.argv[2])
    productcategory_topreview=spark.sql("select  product_category, count(*) as number_of_reviews from reviews  group by product_category order by count(*) desc ")
    productcategory_topreview.write.mode("OVERWRITE").parquet(sys.argv[3])