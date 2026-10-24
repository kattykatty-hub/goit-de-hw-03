"""Homework 03: PySpark purchase analysis.

Run from the repository root: python main.py
Requires users.csv, products.csv and purchases.csv inside data/.
"""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_table(spark, name):
    path = DATA_DIR / f"{name}.csv"
    if not path.is_file():
        raise FileNotFoundError(f"Missing input file: {path}")
    return spark.read.option("header", True).option("inferSchema", True).csv(str(path))


def display(title, dataframe):
    print(f"\n--- {title} ---")
    dataframe.show(truncate=False)


def main():
    spark = SparkSession.builder.appName("PurchaseCategoryAnalysis").getOrCreate()
    try:
        # Task 1: Load the three independent datasets.
        tables = {name: load_table(spark, name) for name in ("users", "purchases", "products")}
        for name, df in tables.items():
            display(f"1. Original {name}", df)

        # Task 2: Remove rows containing null values before joining.
        clean = {name: df.dropna() for name, df in tables.items()}
        for name, df in clean.items():
            print(f"{name}: {tables[name].count()} rows before, {df.count()} after cleaning")
            display(f"2. Cleaned {name}", df)

        # Build purchase-level records with category, age, and transaction value.
        transactions = (
            clean["purchases"]
            .join(clean["products"], on="product_id", how="inner")
            .join(clean["users"], on="user_id", how="inner")
            .withColumn("purchase_amount", F.col("quantity") * F.col("price"))
        )
        display("Joined purchase records", transactions)

        # Task 3: Total value of purchases by product category.
        category_totals = (
            transactions.groupBy("category")
            .agg(F.sum("purchase_amount").alias("category_sales"))
            .orderBy("category")
        )
        display("3. Sales by category", category_totals)

        # Task 4: Repeat the aggregation for customers aged 18 to 25 inclusive.
        young_adult_totals = (
            transactions.where(F.col("age").between(18, 25))
            .groupBy("category")
            .agg(F.sum("purchase_amount").alias("young_adult_sales"))
        )
        display("4. Sales by category (ages 18-25)", young_adult_totals.orderBy("category"))

        # Task 5: Each category's share of total spending in this age group.
        overall = young_adult_totals.agg(F.sum("young_adult_sales").alias("overall_sales")).first()["overall_sales"]
        if overall is None or overall == 0:
            print("5. No nonzero spending found for customers aged 18-25.")
            return
        shares = (
            young_adult_totals.withColumn(
                "spending_percent", F.round(F.col("young_adult_sales") / F.lit(overall) * 100, 2)
            )
            .orderBy(F.desc("spending_percent"), F.asc("category"))
        )
        display("5. Percentage of spending by category (ages 18-25)", shares)

        # Task 6: Highest three category shares.
        display("6. Top 3 categories", shares.limit(3))
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
