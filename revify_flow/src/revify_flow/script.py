import os
import json
import sys

# Get the directory of the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Use relative paths from the script location
INPUT_DIR = os.path.join(SCRIPT_DIR, "output")  # Changed from "/output" to "output"
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "product_summaries.json")

def generate_summary(feature_analysis):
    """
    Converts a list of feature-wise verdicts into a coherent single-paragraph summary.
    """
    paragraph_parts = []
    for i, item in enumerate(feature_analysis):
        verdict = item.get("verdict", "").strip()
        if verdict:
            if i == 0:
                paragraph_parts.append(verdict)
            else:
                paragraph_parts.append(verdict[0].upper() + verdict[1:])
    return ' '.join(paragraph_parts)

def main():
    summaries = {}

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(INPUT_DIR, filename)
            with open(file_path, "r") as f:
                try:
                    feature_data = json.load(f)
                    summary = generate_summary(feature_data)
                    summaries[filename] = summary
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    # Save all summaries to a single output file
    with open(OUTPUT_FILE, "w") as out_file:
        json.dump(summaries, out_file, indent=2)

    print(f"\n✅ Generated summaries for {len(summaries)} products.")
    print(f"📄 Output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
