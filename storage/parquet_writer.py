from pathlib import Path

import pandas as pd


class ParquetWriter:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)

    def write(self, records: list[dict]) -> None:
        if not records:
            return

        new_df = pd.DataFrame(records)

        if self.file_path.exists():
            existing_df = pd.read_parquet(self.file_path)
            combined_df = pd.concat(
                [existing_df, new_df],
                ignore_index=True,
            )
        else:
            combined_df = new_df

        combined_df.to_parquet(
            self.file_path,
            index=False,
        )
