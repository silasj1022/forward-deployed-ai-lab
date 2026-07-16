"""Optional PySpark ingestion example for enterprise knowledge records."""

from __future__ import annotations

from typing import Any


def build_knowledge_silver_layer(spark: Any, input_path: str, output_path: str) -> dict[str, int]:
    """Validate, deduplicate, and write a Delta/Parquet-ready silver dataset.

    The function accepts a SparkSession-like object so it can be unit-tested with
    a fixture and run in local Spark or Databricks.
    """
    from pyspark.sql import functions as F  # type: ignore[import-not-found]
    from pyspark.sql.window import Window  # type: ignore[import-not-found]

    raw = spark.read.json(input_path)
    required = {"document_id", "title", "content", "source"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    ranked = (
        raw.withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_content_hash", F.sha2(F.col("content"), 256))
        .withColumn(
            "_rank",
            F.row_number().over(
                Window.partitionBy("document_id").orderBy(F.col("_ingested_at").desc())
            ),
        )
    )
    silver = ranked.filter(F.col("_rank") == 1).drop("_rank")
    silver.write.mode("overwrite").format("parquet").save(output_path)
    return {"input_rows": raw.count(), "output_rows": silver.count()}
