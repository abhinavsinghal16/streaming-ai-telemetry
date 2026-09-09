from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count

spark = (
    SparkSession.builder
    .appName("telemetry-analytics")
    .getOrCreate()
)

telemetry_df = spark.read.parquet(
    "storage/telemetry.parquet"
)

print("\n=== Schema ===")
telemetry_df.printSchema()

print("\n=== Sample Records ===")
telemetry_df.select(
    "request.provider",
    "request.model",
    "performance.total_latency_ms",
).show(10, truncate=False)

print("\n=== Average Latency By Model ===")
telemetry_df.groupBy("request.model") \
    .agg(
        avg("performance.total_latency_ms")
        .alias("avg_latency_ms")
    ) \
    .orderBy("avg_latency_ms") \
    .show(truncate=False)

print("\n=== Average Latency By Provider ===")
telemetry_df.groupBy("request.provider") \
    .agg(
        avg("performance.total_latency_ms")
        .alias("avg_latency_ms")
    ) \
    .show(truncate=False)

print("\n=== Request Volume By Provider ===")
telemetry_df.groupBy("request.provider") \
    .agg(
        count("*").alias("request_count")
    ) \
    .orderBy("request_count", ascending=False) \
    .show()

print("\n=== Average Token Usage By Model ===")
telemetry_df.groupBy("request.model") \
    .agg(
        avg("tokens.prompt_tokens").alias("avg_prompt_tokens"),
        avg("tokens.completion_tokens").alias("avg_completion_tokens")
    ) \
    .show(truncate=False)

print("\n=== Outcome Counts ===")
telemetry_df.groupBy("outcome.status") \
    .count() \
    .show()

print("\n=== Top 10 Tenants ===")
telemetry_df.groupBy("request.tenant_id") \
    .count() \
    .orderBy("count", ascending=False) \
    .show(10)

print("\n=== Cache Hit Distribution ===")
telemetry_df.groupBy("rag.cache_hit") \
    .count() \
    .show()

spark.stop()