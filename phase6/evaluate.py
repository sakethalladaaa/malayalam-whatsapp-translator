from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

from phase6.inference import create_engine, transliterate


INPUT_PATH = Path("phase6/data/indicxlit_validation_75.csv")
OUTPUT_PATH = Path("phase6/results/indicxlit_validation_75_results.csv")


def similarity(a: str, b: str) -> float:
    a = " ".join(str(a).strip().split())
    b = " ".join(str(b).strip().split())
    return SequenceMatcher(None, a, b).ratio()


def main() -> None:
    df = pd.read_csv(INPUT_PATH)

    engine = create_engine()

    df["predicted_malayalam"] = df["roman_input"].apply(
        lambda text: transliterate(text, engine=engine)
    )

    df["exact_match"] = (
        df["predicted_malayalam"].str.strip()
        == df["ground_truth_malayalam"].str.strip()
    )

    df["normalized_similarity"] = df.apply(
        lambda row: similarity(
            row["ground_truth_malayalam"],
            row["predicted_malayalam"],
        ),
        axis=1,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("SAVED:", OUTPUT_PATH)
    print("TOTAL:", len(df))
    print("EXACT MATCHES:", int(df["exact_match"].sum()))
    print("EXACT-MATCH RATE:", f"{df['exact_match'].mean() * 100:.2f}%")
    print(
        "MEAN NORMALIZED SIMILARITY:",
        f"{df['normalized_similarity'].mean() * 100:.2f}%",
    )
    print(
        "MEDIAN NORMALIZED SIMILARITY:",
        f"{df['normalized_similarity'].median() * 100:.2f}%",
    )
    print(
        ">= 0.90 SIMILARITY:",
        f"{(df['normalized_similarity'] >= 0.90).sum()}/{len(df)}",
    )
    print(
        "< 0.90 SIMILARITY:",
        f"{(df['normalized_similarity'] < 0.90).sum()}/{len(df)}",
    )


if __name__ == "__main__":
    main()
