from rouge_score import rouge_scorer
from bert_score import score as bert_score_fn
import numpy as np
import pandas as pd
import json

# Sample data (replace with your actual dataset)
# Load data from product_summaries.json
# with open('product_summaries.json', 'r') as file:
#     data = json.load(file)

# # Initialize metrics storage
# results = []

# # Initialize ROUGE scorer
# rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# # Loop through each product entry
# for item in data:
#     # Dynamically load the correct feature_analysis field based on the numbering
#     feature_analysis_key = f"feature_analysis_{item['id']}.json" if item['id'] > 0 else "feature_analysis.json"
    
#     # Extract the generated summary from the corresponding feature_analysis field
#     generated = item[feature_analysis_key]
#     reference = item["amazon_summary"]
    
#     # ROUGE scores
#     rouge_scores = rouge.score(reference, generated)
    
#     # BERTScore
#     _, _, bert_f1 = bert_score_fn([generated], [reference], lang='en', model_type='microsoft/deberta-xlarge-mnli', verbose=False)
    
#     # Save scores
#     results.append({
#         "product": item["product"],
#         "rouge1": rouge_scores["rouge1"].fmeasure,
#         "rouge2": rouge_scores["rouge2"].fmeasure,
#         "rougeL": rouge_scores["rougeL"].fmeasure,
#         "bertscore_f1": bert_f1[0].item()
#     })

# # Convert to DataFrame for analysis
# df = pd.DataFrame(results)

# # Compute Aggregates
# summary = {
#     "avg_rouge1": df["rouge1"].mean(),
#     "avg_rouge2": df["rouge2"].mean(),
#     "avg_rougeL": df["rougeL"].mean(),
#     "avg_bertscore_f1": df["bertscore_f1"].mean(),
#     "std_bertscore_f1": df["bertscore_f1"].std()
# }

# # Best/Worst based on BERTScore
# best_idx = df["bertscore_f1"].idxmax()
# worst_idx = df["bertscore_f1"].idxmin()
# best_example = data[best_idx]
# worst_example = data[worst_idx]

# # Output
# print("=== Aggregated Metrics ===")
# print(pd.Series(summary), "\n")

# print("=== Best Example ===")
# print(f"Product: {best_example['product']}")
# print(f"Feature Analysis: {best_example['feature_analysis']}")
# print(f"Amazon Summary: {best_example['amazon_summary']}\n")

# print("=== Worst Example ===")
# print(f"Product: {worst_example['product']}")
# print(f"Feature Analysis: {worst_example['feature_analysis']}")
# print(f"Amazon Summary: {worst_example['amazon_summary']}")
# def main():
#     # Load data from product_summaries.json
#     with open('product_summaries.json', 'r') as file:
#         data = json.load(file)

#     # Initialize metrics storage
#     results = []

#     # Initialize ROUGE scorer
#     rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

#     # Loop through each product entry
#     for idx, item in enumerate(data):
#         # Skip processing if the index is 9
#         if idx == 9:
#             continue

#         # Dynamically load the correct feature_analysis field based on the numbering
#         feature_analysis_key = f"feature_analysis_{idx}.json" if idx > 0 else "feature_analysis.json"
        
#         # Extract the generated summary from the corresponding feature_analysis field
#         generated = item[feature_analysis_key]
#         reference = item["amazon_summary"]
        
#         # ROUGE scores
#         rouge_scores = rouge.score(reference, generated)
        
#         # BERTScore
#         _, _, bert_f1 = bert_score_fn([generated], [reference], lang='en', model_type='microsoft/deberta-xlarge-mnli', verbose=False)
        
#         # Save scores
#         results.append({
#             "rouge1": rouge_scores["rouge1"].fmeasure,
#             "rouge2": rouge_scores["rouge2"].fmeasure,
#             "rougeL": rouge_scores["rougeL"].fmeasure,
#             "bertscore_f1": bert_f1[0].item()
#         })

#     # Convert to DataFrame for analysis
#     df = pd.DataFrame(results)

#     # Compute Aggregates
#     summary = {
#         "avg_rouge1": df["rouge1"].mean(),
#         "avg_rouge2": df["rouge2"].mean(),
#         "avg_rougeL": df["rougeL"].mean(),
#         "avg_bertscore_f1": df["bertscore_f1"].mean(),
#         "std_bertscore_f1": df["bertscore_f1"].std()
#     }

#     # Best/Worst based on BERTScore
#     best_idx = df["bertscore_f1"].idxmax()
#     worst_idx = df["bertscore_f1"].idxmin()
#     best_example = data[best_idx]
#     worst_example = data[worst_idx]

#     # Output
#     print("=== Aggregated Metrics ===")
#     print(pd.Series(summary), "\n")

#     print("=== Best Example ===")
#     print(f"Product: {best_example['product']}")
#     print(f"Feature Analysis: {best_example['feature_analysis']}")
#     print(f"Amazon Summary: {best_example['amazon_summary']}\n")

#     print("=== Worst Example ===")
#     print(f"Product: {worst_example['product']}")
#     print(f"Feature Analysis: {worst_example['feature_analysis']}")
#     print(f"Amazon Summary: {worst_example['amazon_summary']}")

# if __name__ == "__main__":
#     main()


# from rouge_score import rouge_scorer
# import numpy as np
# import pandas as pd
# import json
# import os

# Import BERTScore with error handling
try:
    from bert_score import score as bert_score_fn
    BERT_SCORE_AVAILABLE = True
except ImportError:
    print("Warning: BERTScore not available. Install it with 'pip install bert-score'")
    BERT_SCORE_AVAILABLE = False

def main():
    # Load data from product_summaries.json
    try:
        with open('product_summaries.json', 'r') as file:
            data = json.load(file)
        print(f"Loaded data for {len(data)} items")
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    # Initialize metrics storage
    results = []

    # Initialize ROUGE scorer
    print("Initializing ROUGE scorer...")
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    # Loop through each product entry
    for idx, item in enumerate(data):
        print(f"Processing item {idx+1}/{len(data)}...")
        
        # Look for feature analysis and amazon summary keys
        feature_analysis = None
        amazon_summary = None
        key_found = False
        
        # Extract the key-value pairs from the item
        for key, value in item.items():
            if "feature_analysis" in key:
                feature_analysis = value
                feature_key = key
                key_found = True
            elif "amazon_summary" == key:
                amazon_summary = value
        
        # Skip if missing required data
        if not feature_analysis or not amazon_summary:
            print(f"Skipping item {idx+1} - missing required fields")
            continue
        
        print(f"  Using feature analysis from key: {feature_key}")
        
        # ROUGE scores
        print("  Calculating ROUGE scores...")
        rouge_scores = rouge.score(amazon_summary, feature_analysis)
        
        # BERTScore
        bert_f1 = None
        if BERT_SCORE_AVAILABLE:
            try:
                print("  Calculating BERTScore (this may take a while)...")
                # Use a smaller model for faster computation
                _, _, bert_f1 = bert_score_fn(
                    [feature_analysis], 
                    [amazon_summary], 
                    lang='en', 
                    model_type='microsoft/deberta-base-mnli',  # Using smaller model
                    verbose=False
                )
                bert_f1 = bert_f1[0].item()
                print(f"  BERTScore: {bert_f1:.4f}")
            except Exception as e:
                print(f"  Error calculating BERTScore: {e}")
                bert_f1 = None
        
        # Save scores
        result = {
            "index": idx,
            "feature_key": feature_key,
            "rouge1": rouge_scores["rouge1"].fmeasure,
            "rouge2": rouge_scores["rouge2"].fmeasure,
            "rougeL": rouge_scores["rougeL"].fmeasure,
        }
        
        if bert_f1 is not None:
            result["bertscore_f1"] = bert_f1
            
        results.append(result)
        print(f"  ROUGE-1: {rouge_scores['rouge1'].fmeasure:.4f}, ROUGE-2: {rouge_scores['rouge2'].fmeasure:.4f}")

    # Convert to DataFrame for analysis
    df = pd.DataFrame(results)
    
    # Save results to CSV for reference
    try:
        df.to_csv("benchmark_results.csv", index=False)
        print("\nBenchmark results saved to benchmark_results.csv")
    except:
        print("Could not save results to CSV")

    # Compute Aggregates
    print("\n=== Aggregated Metrics ===")
    summary = {
        "avg_rouge1": df["rouge1"].mean(),
        "avg_rouge2": df["rouge2"].mean(),
        "avg_rougeL": df["rougeL"].mean(),
    }
    
    if "bertscore_f1" in df.columns:
        summary["avg_bertscore_f1"] = df["bertscore_f1"].mean()
        summary["std_bertscore_f1"] = df["bertscore_f1"].std()
    
    print(pd.Series(summary), "\n")

    # Best/Worst based on ROUGE-L (or BERTScore if available)
    best_metric = "bertscore_f1" if "bertscore_f1" in df.columns else "rougeL"
    print(f"Finding best/worst examples based on {best_metric}...")
    
    try:
        best_idx = df[best_metric].idxmax()
        worst_idx = df[best_metric].idxmin()
        
        best_data_idx = df.loc[best_idx, "index"]
        worst_data_idx = df.loc[worst_idx, "index"]
        
        best_example = data[int(best_data_idx)]
        worst_example = data[int(worst_data_idx)]
        
        best_feature_key = df.loc[best_idx, "feature_key"]
        worst_feature_key = df.loc[worst_idx, "feature_key"]
        
        # Output best example
        print("\n=== Best Example ===")
        print(f"Feature Key: {best_feature_key}")
        print(f"Feature Analysis: {best_example[best_feature_key][:200]}...")
        print(f"Amazon Summary: {best_example['amazon_summary'][:200]}...\n")
        
        # Output worst example
        print("=== Worst Example ===")
        print(f"Feature Key: {worst_feature_key}")
        print(f"Feature Analysis: {worst_example[worst_feature_key][:200]}...")
        print(f"Amazon Summary: {worst_example['amazon_summary'][:200]}...")
        
    except Exception as e:
        print(f"Error finding best/worst examples: {e}")

if __name__ == "__main__":
    main()