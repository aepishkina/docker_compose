from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, round

spark = SparkSession.builder\
        .appName("HousePrice")\
        .master('spark://spark-master:7077')\
        .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-jdbc.jar")\
        .getOrCreate()

db_url = "jdbc:postgresql://db:5432/houses_db"
con_props = {
    "user": "root",
    "password": "root",
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(url=db_url, table="house_prices", properties=con_props)

query_result = df.filter(df["property_type"].isin('House', 'Flat')). \
    groupBy('location','city', 'bedrooms').agg(round(mean("price"), 2).alias("AVG Price")). \
    orderBy(["location", "city", "bedrooms","AVG Price"], ascending=[False, False, False, True])

query_result.show()

spark.stop()