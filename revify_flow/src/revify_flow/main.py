import json
import os
import re
import sys
from typing import Dict
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import pandas as pd

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Now use absolute import
from src.revify_flow.crews.team_revify.team_revify import TeamRevify

from src.revify_flow.tools.amazon_scraper_tool import AmazonScraperTool

# Load environment variables
load_dotenv()

class FeatureList(BaseModel):
    """Model for feature extraction results"""
    features: list[str] = Field(description="List of extracted product features")

# def run_feature_extraction():
#     """Run only the feature extraction task from TeamRevify"""
#     print("\n===== Revify Feature Extractor =====\n")
    
#     # Get the product URL or name from the user
#     product_url = input("Enter the product URL or name: ")

#     # Create the full TeamRevify instance (this loads your YAML configs)
#     team_revify = TeamRevify()
    
#     # Get the feature extraction task
#     feature_task = team_revify.extract_features_task()
#     feature_agent = team_revify.feature_extractor()
    
#     print(f"\n🔍 Extracting features for: {product_url}")
#     print("⏳ This may take a moment...\n")
    
#     # Create a single-task crew to run just the feature extraction
#     single_task_crew = Crew(
#         agents=[feature_agent],
#         tasks=[feature_task],
#         verbose=True,
#         process=Process.sequential
#     )
    
#     # Execute the crew with the product URL as input
#     result = single_task_crew.kickoff(inputs={"product_input": product_url})
    
#     # Process and display the result
#     try:
#         # Create output directory if it doesn't exist
#         os.makedirs("output", exist_ok=True)
        
#         # Save the raw result
#         with open("output/extracted_features_raw.txt", "w") as f:
#             f.write(str(result.raw))
        
#         # Try to extract and format the features
#         print("\n✅ Feature extraction complete!")
#         print("\nExtracted Features:")
        
#         # Display the raw result since it's all we have
#         print(result.raw)
        
#         # For structured output, save to JSON format
#         with open("output/extracted_features.json", "w") as f:
#             f.write(json.dumps({"raw_output": result.raw}, indent=2))
        
#         print("\nResults saved to output directory")
#         print("\n===== Extraction Complete =====")
        
#         return result.raw
            
#     except Exception as e:
#         print(f"Error processing result: {e}")
#         print(f"Raw result: {getattr(result, 'raw', str(result))}")
#         return {"error": str(e), "raw_result": getattr(result, 'raw', str(result))}

# def analyse_reviews():
#     """Run the review analysis task from TeamRevify"""
#     print("\n===== Revify Review Analyzer =====\n")
    
#     df = pd.read_csv("reviews_cleaned.csv")
#     if df.empty:
#         print("No reviews found in the CSV file.")
#         return

#     # Select only the required columns
#     df_filtered = df[['name', 'brand', 'reviews.rating', 'reviews.title', 'reviews.text']]

#     # Convert each row into a dictionary
#     review_data = df_filtered.to_dict(orient='records')

def extract_json_from_markdown(text: str) -> str:
    """Extract JSON content from markdown code blocks"""
    # Look for content between triple backticks
    pattern = r"```(?:json)?\s*\n([\s\S]*?)\n\s*```"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    
    # If no backticks, try to find JSON between curly braces
    pattern = r"\{[\s\S]*?\}"
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    
    return text  # Return original if no patterns match

def review_analysis():
    print("\n🚀 Starting Dynamic Feature-Based Review Analysis\n")
    product_input = input("Enter the product name or URL: ")

    # Load and prepare reviews
    df = pd.read_csv("reviews_cleaned.csv")
    if df.empty:
        print("❌ No reviews found.")
        return
    review_dicts = df[['name', 'brand', 'reviews.rating', 'reviews.title', 'reviews.text']].to_dict(orient='records')

    # Load team, agents, and the feature extraction task
    team = TeamRevify()
    feature_task = team.extract_features_task()
    feature_agent = team.feature_extractor()
    review_agent = team.review_analysis_agent()

    # -- Phase 1: Extract Features
    print("\n🔍 Extracting product features...")
    feature_crew = Crew(
        agents=[feature_agent],
        tasks=[feature_task],
        process=Process.sequential,
        verbose=True
    )
    feature_result = feature_crew.kickoff(inputs={"product_input": product_input})
    feature_raw = feature_result.raw
    extracted_json = extract_json_from_markdown(feature_raw)

    # try:
    #     # Parse the extracted JSON string
    #     features_data = json.loads(extracted_json)
        
    #     # Extract the features list
    #     if isinstance(features_data, dict) and "features" in features_data:
    #         features = features_data["features"]
    #     else:
    #         features = features_data  # Assume it's already the list
        
    #     if not isinstance(features, list):
    #         raise ValueError("Expected a list of features")
    # except Exception as e:
    #     print(f"❌ Failed to parse features: {e}")
    #     print(f"Raw output: {feature_result.raw}")
    #     return
    try:
        # Parse the extracted JSON string
        features_data = json.loads(extracted_json)
        
        # Extract the features list
        if isinstance(features_data, dict) and "features" in features_data:
            features = features_data["features"]
        else:
            features = features_data  # Assume it's already the list
        
        if not isinstance(features, list):
            raise ValueError("Expected a list of features")
            
        print(f"\n✅ Extracted {len(features)} features:")
        for i, feature in enumerate(features):
            print(f"  {i+1}. {feature}")
    except Exception as e:
        print(f"❌ Failed to parse features: {e}")
        print(f"Raw output: {feature_raw}")
        return
    
    print(f"\n🔍 Extracted Features: {features}")
    print("\n⏳ Analyzing reviews...\n")

    # -- Phase 2: Option 1: Dynamically create tasks per feature
    # review_agent = team.review_analysis_agent()
    # analysis_tasks = []

    # for feature_name in features:
    #     task = Task(
    #         description=f'''
    #             For the feature: "{feature_name}", analyze the user reviews of the product from the perspective
    #             of that feature only.

    #             Reviews:
    #             {review_dicts}

    #             Output must be a valid JSON object containing:
    #             - Feature name
    #             - Sentiment
    #             - Key points (with frequency count)
    #             - Overall verdict
    #         ''',
    #         expected_output=f"A JSON summary of sentiment and insights for feature '{feature_name}'. **DO NOT INCLUDE BACKTICKS (```) OR THE WORD 'json' IN THE OUTPUT. THE OUTPUT SHOULD START AT OPENING CURLY BRACES "'{'" AND END AT CLOSING CURLY BRACES "'}'" **",
    #         agent=review_agent
    #     )
    #     analysis_tasks.append(task)
    
    # # -- Phase 3: Run the analysis tasks
    # review_crew = Crew(
    #     agents=[review_agent],
    #     tasks=analysis_tasks,
    #     process=Process.sequential,  
    #     # or .parallel if you'd like to try that
    #     verbose=True
    # )
    # final_result = review_crew.kickoff()

    # # -- Save results
    # os.makedirs("output", exist_ok=True)
    # with open("output/dynamic_feature_analysis.json", "w") as f:
    #     f.write(json.dumps(final_result, indent=2))

    # print("\n✅ Feature-by-feature analysis complete. Results saved.")
    # return final_result


    # -- Phase 2: Option 2: Create a single comprehensive analysis task
    print("\n⏳ Starting comprehensive review analysis for all features...")

    # Instead of creating a new task inline, use the one from TeamRevify
    analysis_task = team.comprehensive_review_analysis_task()

    # Create a crew with just the review analysis task
    analysis_crew = Crew(
        agents=[review_agent],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )

    # Pass the dynamic content as inputs when kicking off the crew
    result = analysis_crew.kickoff(inputs={
        "features": ", ".join(features),
        "reviews": json.dumps(review_dicts, indent=2)
    })

    # Extract and process the result
    try:
        # Get raw result
        raw_output = result.raw
        
        # Extract JSON from markdown if needed
        json_str = extract_json_from_markdown(raw_output)
        
        # Parse the JSON
        analysis_results = json.loads(json_str)
        
        # Save the results
        os.makedirs("output", exist_ok=True)
        with open("output/feature_analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n✅ Analysis complete!")
        print(f"\nAnalyzed {len(analysis_results)} features from {len(review_dicts)} reviews")
        
        # Show a brief summary for each feature
        for i, analysis in enumerate(analysis_results):
            feature = analysis.get("feature", "Unknown")
            sentiment = analysis.get("sentiment", "Unknown")
            verdict = analysis.get("verdict", "No verdict provided")
            
            print(f"\n{i+1}. {feature}: {sentiment}")
            print(f"   {verdict[:100]}..." if len(verdict) > 100 else f"   {verdict}")
        
        print("\nDetailed results saved to 'output/feature_analysis.json'")
        return analysis_results
    
    except Exception as e:
        print(f"❌ Error processing analysis results: {e}")
        print(f"Raw output: {raw_output}")
        
        # Still try to save the raw output for debugging
        with open("output/feature_analysis_raw.txt", "w", encoding="utf-8") as f:
            f.write(raw_output)
        
        print("Raw output saved to 'output/feature_analysis_raw.txt'")
        return None

def estimate_tokens(text):
    return len(text.split()) * 1.3  # crude estimate (avg word = 1.3 tokens)

from crewai import Crew, Process, Task
import math

def summarize_reviews_chunked(review_data, team, chunk_size=500):
    print(f"\n🔧 Chunking and summarizing {len(review_data)} reviews...")
    
    review_chunks = [
        review_data[i:i + chunk_size]
        for i in range(0, len(review_data), chunk_size)
    ]
    summaries = []
    team = TeamRevify()
    summarize_agent = team.chunk_summary_agent()  # you’ll define this in YAML
    print(f"🧠 Loaded summary agent to handle {len(review_chunks)} chunks")

    for i, chunk in enumerate(review_chunks):
        print(f"\n📝 Summarizing chunk {i+1}/{len(review_chunks)}...")
        task = Task(
            description=(
                "Summarize the following list of product reviews. Focus on overall tone, frequently mentioned features, "
                "and any strong sentiments. This is just one chunk of many.\n\n"
                f"Reviews:\n{chunk}"
            ),
            expected_output="A concise paragraph summarizing this chunk of reviews.",
            agent=summarize_agent
        )

        crew = Crew(
            agents=[summarize_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        summaries.append(result.raw)

    print(f"\n✅ Done summarizing all chunks. Total summaries: {len(summaries)}")
    return summaries


import litellm

from litellm.exceptions import RateLimitError
import time
def review_analysis2():
    
    print("\n🚀 Starting Dynamic Feature-Based Review Analysis\n")
    product_input = input("Enter the product name or URL: ")

    # Load and prepare reviews
    try:
        df = pd.read_csv("reviews_cleaned.csv")
        if df.empty:
            print("❌ No reviews found.")
            return
        
        # Limit to only 10 reviews to reduce token usage
        df_filtered = df[['name', 'brand', 'reviews.rating', 'reviews.title', 'reviews.text']]
        review_dicts = df_filtered.to_dict(orient='records')
        
        print(f"📋 Loaded {len(review_dicts)} reviews for analysis")
    except Exception as e:
        print(f"❌ Error loading reviews: {e}")
        return

    # Load team, agents, and the feature extraction task
    team = TeamRevify()
    
    # -- Phase 1: Extract Features with retry logic
    print("\n🔍 Extracting product features...")
    
    # Define retry logic for feature extraction
    max_retries = 3
    feature_raw = None
    
    for attempt in range(max_retries):
        try:
            feature_agent = team.feature_extractor()
            feature_task = team.extract_features_task()
            
            feature_crew = Crew(
                agents=[feature_agent],
                tasks=[feature_task],
                process=Process.sequential,
                verbose=True
            )
            
            feature_result = feature_crew.kickoff(inputs={"product_input": product_input})
            feature_raw = feature_result.raw
            break  # If successful, exit the retry loop
            
        except RateLimitError as e:
            print(f"\n⚠️ Rate limit hit during feature extraction (attempt {attempt+1}/{max_retries})")
            if attempt < max_retries - 1:
                wait_time = min(30, (2 ** attempt) * 5)  # Exponential backoff with max 30 seconds
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("\n❌ Max retries reached for feature extraction.")
                print(f"Error: {str(e)}")
                litellm._turn_on_debug()
                return
        except Exception as e:
            print(f"\n❌ Unexpected error during feature extraction: {str(e)}")
            return
    
    # Process feature extraction results
    if not feature_raw:
        print("\n❌ Failed to extract features.")
        return
        
    extracted_json = extract_json_from_markdown(feature_raw)

    try:
        # Parse the extracted JSON string
        features_data = json.loads(extracted_json)
        
        # Extract the features list
        if isinstance(features_data, dict) and "features" in features_data:
            features = features_data["features"]
        else:
            features = features_data  # Assume it's already the list
        
        if not isinstance(features, list):
            raise ValueError("Expected a list of features")
            
        # Limit to max 5 features to reduce API calls
        if len(features) > 5:
            print(f"\n⚠️ Limiting analysis to the first 5 features to avoid rate limits")
            features = features[:5]
            
        print(f"\n✅ Extracted {len(features)} features:")
        for i, feature in enumerate(features):
            print(f"  {i+1}. {feature}")
    except Exception as e:
        print(f"❌ Failed to parse features: {e}")
        print(f"Raw output: {feature_raw}")
        return
    
    print(f"\n🔍 Features for analysis: {features}")
    print("\n⏳ Preparing review analysis...\n")

    # -- Phase 2: Comprehensive analysis with retry logic
    print("\n⏳ Starting comprehensive review analysis...")

    # Use the comprehensive task from TeamRevify
    review_agent = team.review_analysis_agent()
    analysis_task = team.comprehensive_review_analysis_task()

    # Create a crew with just the review analysis task
    analysis_crew = Crew(
        agents=[review_agent],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )

    # Retry logic for analysis phase
    max_retries = 3
    analysis_result = None
    
    for attempt in range(max_retries):
        try:
            # Wait before making this call to avoid rate limits
            if attempt > 0:
                wait_time = min(60, (2 ** attempt) * 10)  # Longer waits for review analysis
                print(f"\n⏳ Waiting {wait_time} seconds before attempt {attempt+1}...")
                time.sleep(wait_time)
            
            print(f"\n⚙️ Running comprehensive feature analysis (attempt {attempt+1}/{max_retries})...")
            
            chunk_summaries = summarize_reviews_chunked(review_dicts, team, chunk_size=200)
            reviews_input = "\n\n".join(chunk_summaries)

            # Pass the dynamic content as inputs when kicking off the crew
            result = analysis_crew.kickoff(inputs={
                "features": ", ".join(features),
                "reviews": reviews_input  # Further limit reviews if needed
            })
            
            analysis_result = result
            break  # Success, exit retry loop
            
        except RateLimitError as e:
            print(f"\n⚠️ Rate limit hit during review analysis (attempt {attempt+1}/{max_retries})")
            if attempt < max_retries - 1:
                # Don't need to sleep here as we already sleep at the beginning of the loop
                print(f"Will retry soon...")
            else:
                print("\n❌ Max retries reached for review analysis.")
                print(f"Error: {str(e)}")
                return
        except Exception as e:
            print(f"\n❌ Unexpected error during review analysis: {str(e)}")
            if attempt < max_retries - 1:
                print("Will retry...")
            else:
                return

    # Process analysis results
    if not analysis_result:
        print("\n❌ Failed to complete review analysis.")
        return
        
    try:
        # Get raw result
        raw_output = analysis_result.raw
        
        # Extract JSON from markdown if needed
        json_str = extract_json_from_markdown(raw_output)
        
        # Parse the JSON
        analysis_results = json.loads(json_str)
        
        # Save the results
        os.makedirs("output", exist_ok=True)
        with open("output/feature_analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n✅ Analysis complete!")
        print(f"\nAnalyzed {len(analysis_results)} features")
        
        # Show a brief summary for each feature
        for i, analysis in enumerate(analysis_results):
            feature = analysis.get("feature", "Unknown")
            sentiment = analysis.get("sentiment", "Unknown")
            verdict = analysis.get("verdict", "No verdict provided")
            
            print(f"\n{i+1}. {feature}: {sentiment}")
            print(f"   {verdict[:100]}..." if len(verdict) > 100 else f"   {verdict}")
        
        print("\nDetailed results saved to 'output/feature_analysis.json'")
        return analysis_results
    
    except Exception as e:
        print(f"❌ Error processing analysis results: {e}")
        print(f"Raw output: {raw_output}")
        
        # Still try to save the raw output for debugging
        with open("output/feature_analysis_raw.txt", "w", encoding="utf-8") as f:
            f.write(str(raw_output))
        
        print("Raw output saved to 'output/feature_analysis_raw.txt'")
        return None

import logging
import traceback
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("revify_debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("revify_debug")
# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

def debug_scraper_tool():
    """Debug function to test just the scraper tool directly"""
    logger.info("Starting scraper tool debug")
    
    product_url = input("Enter the product URL to test scraping: ")
    
    try:
        # Create the scraper tool directly
        # amazon_tool = AmazonScraperTool
        # # Run the tool directly with the URL
        # result = amazon_tool._run(
        #     url=product_url,
        #     target_reviews=10,  # Reduced for testing
        #     product_name="Debug Test Product"
        # )

        result = AmazonScraperTool._run(url=product_url, target_reviews=50, product_name="Debug Test Product")
        
        logger.info(f"Scraper tool result: {result}")
        print(f"\n✅ Scraper tool result: {result}")
        
        # Check if CSV was created
        if os.path.exists("scraped_reviews.csv"):
            df = pd.read_csv("scraped_reviews.csv")
            logger.info(f"CSV file created with {len(df)} reviews")
            print(f"CSV file created with {len(df)} reviews")
            print("\nFirst 3 reviews:")
            for i, row in df.head(3).iterrows():
                print(f"Title: {row['reviews.title']}")
                print(f"Rating: {row['reviews.rating']}")
                print(f"Text: {row['reviews.text'][:100]}...\n")
        else:
            logger.error("No CSV file was created!")
            print("❌ No CSV file was created!")
    
    except Exception as e:
        logger.error(f"Error in scraper tool: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"❌ Error in scraper tool: {str(e)}")


def debug_run_workflow():
    """Debug version of run_workflow with additional logging and checks"""
    logger.info("Starting debug version of run_workflow")
    print("\n🚀 Starting Revify Debug - Product Review Analysis")
    
    # Get the product URL from the user
    product_url = input("Enter the product URL: ")

    # After getting the product_url from the user:
    original_url = product_url

    product_name = input("Enter the product name (optional): ")
    
    logger.info(f"Input URL: {product_url}")
    logger.info(f"Input product name: {product_name}")
    
    # Create TeamRevify instance
    team = TeamRevify()
    logger.info("TeamRevify instance created")
    
    # 1. Extract product features
    print("\n📋 Phase 1: Extracting product features...")
    logger.info("Starting feature extraction phase")
    
    try:
        feature_agent = team.feature_extractor()
        feature_task = team.extract_features_task()
        
        feature_crew = Crew(
            agents=[feature_agent],
            tasks=[feature_task],
            process=Process.sequential,
            verbose=True
        )
        
        logger.info(f"Sending URL to feature extraction: {product_url}")
        feature_result = feature_crew.kickoff(inputs={"product_input": product_url})
        feature_raw = feature_result.raw
        
        logger.info("Feature extraction completed")
        logger.info(f"Raw feature result: {feature_raw}")
        
        # Process feature extraction results
        extracted_json = extract_json_from_markdown(feature_raw)
        logger.info(f"Extracted JSON: {extracted_json}")
        
        features_data = json.loads(extracted_json)
        
        # Extract the features list
        if isinstance(features_data, dict) and "features" in features_data:
            features = features_data["features"]
        else:
            features = features_data  # Assume it's already the list
        
        logger.info(f"Extracted features: {features}")
        print(f"\n✅ Extracted features: {features}")
    
    except Exception as e:
        logger.error(f"Error in feature extraction: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"\n❌ Error in feature extraction: {str(e)}")
        return
    
    # 2. Debug the scraper directly
    print("\n📋 Phase 2: Testing scraper tool directly...")
    logger.info("Testing scraper tool directly")
    
    try:
        # Create the scraper tool directly
        amazon_tool= team.amazon_scraper_tool()
        
        # Create an input dictionary
        # input_dict = {
        #     "url": product_url,
        #     "target_reviews": 10,
        #     "product_name": product_name if product_name else "Test Product"
        # }
        # Run the tool directly with the URL
        direct_result = amazon_tool._run(
            url=product_url,
            target_reviews=10,  # Reduced for testing
            product_name=product_name if product_name else "Test Product"
        )
        # direct_result = amazon_tool._run(input_dict)
        
        logger.info(f"Direct scraper result: {direct_result}")
        print(f"\n✅ Direct scraper result: {direct_result}")
        
    except Exception as e:
        logger.error(f"Error in direct scraper test: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"\n❌ Error in direct scraper test: {str(e)}")
    
    # 3. Now try through the agent system
    print("\n📋 Phase 3: Testing scraper through agent system...")
    logger.info("Testing scraper through agent system")
    
    try:
        review_scraper = team.review_scraper()
        scrape_reviews_task = team.scrape_reviews_task()

        scrape_crew = Crew(
            agents=[review_scraper],
            tasks=[scrape_reviews_task],
            process=Process.sequential,
            verbose=True
        )
        
        logger.info(f"Sending URL to scrape crew: {product_url}")
        print(f"Original URL being sent: {product_url}")
        
        # Just before scrape_crew.kickoff():
        print(f"\n🔍 VERIFICATION: The exact URL that should be used is: {original_url}")
        # Pass product name if available
        scrape_result = scrape_crew.kickoff(inputs={
            "product_url": product_url, 
            "target_reviews": 10,  # Reduced for testing
            "product_name": product_name if product_name else "Test Product"
        })

        logger.info("Scraper crew completed")
        logger.info(f"Scraper result: {scrape_result.raw}")
        print("\n✅ Scraper crew completed")
        # After scraping is done:
        print(f"\n🔍 Checking if original URL {original_url} was preserved during scraping...")
    
    except Exception as e:
        logger.error(f"Error in scraper crew: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"\n❌ Error in scraper crew: {str(e)}")
    
    # Check if reviews were successfully scraped
    if os.path.exists("scraped_reviews.csv"):
        try:
            df = pd.read_csv("scraped_reviews.csv")
            logger.info(f"Found scraped_reviews.csv with {len(df)} reviews")
            print(f"\n✅ Found scraped_reviews.csv with {len(df)} reviews")
            
            # Only proceed if we have reviews
            if len(df) > 0:
                # Continue with the rest of the workflow...
                print("\n✅ Debug workflow completed successfully!")
                logger.info("Debug workflow completed successfully")
            else:
                print("\n⚠️ No reviews were scraped. Stopping workflow.")
                logger.warning("No reviews were scraped. Stopping workflow.")
        except Exception as e:
            logger.error(f"Error reading scraped_reviews.csv: {str(e)}")
            print(f"\n❌ Error reading scraped_reviews.csv: {str(e)}")
    else:
        logger.error("scraped_reviews.csv file not found")
        print("\n❌ scraped_reviews.csv file not found. Scraping failed.")

def run_workflow():
    """Run the full Revify workflow"""
    print("\n🚀 Starting Revify - Product Review Analysis")
    
    # Get the product URL from the user
    product_url = input("Enter the product URL: ")
    product_name = input("Enter the product name (optional): ")
    
    # Create TeamRevify instance
    team = TeamRevify()
    
    # 1. Extract product features
    print("\n📋 Phase 1: Extracting product features...")
    feature_agent = team.feature_extractor()
    feature_task = team.extract_features_task()
    
    feature_crew = Crew(
        agents=[feature_agent],
        tasks=[feature_task],
        process=Process.sequential,
        verbose=True
    )
    
    max_retries = 3
    feature_raw = None
    
    for attempt in range(max_retries):
        try:
            print(f"\n⚙️ Running feature extraction (attempt {attempt+1}/{max_retries})...")
            feature_result = feature_crew.kickoff(inputs={"product_input": product_url})
            feature_raw = feature_result.raw
            break
        except RateLimitError as e:
            print(f"\n⚠️ Rate limit hit during feature extraction (attempt {attempt+1}/{max_retries})")
            if attempt < max_retries - 1:
                wait_time = min(30, (2 ** attempt) * 5)
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("\n❌ Max retries reached for feature extraction.")
                print(f"Error: {str(e)}")
                return
        except Exception as e:
            print(f"\n❌ Unexpected error during feature extraction: {str(e)}")
            return
    
    # Process feature extraction results
    if not feature_raw:
        print("\n❌ Failed to extract features.")
        return
        
    extracted_json = extract_json_from_markdown(feature_raw)
    
    try:
        # Parse the extracted JSON string
        features_data = json.loads(extracted_json)
        
        # Extract the features list
        if isinstance(features_data, dict) and "features" in features_data:
            features = features_data["features"]
        else:
            features = features_data  # Assume it's already the list
        
        if not isinstance(features, list):
            raise ValueError("Expected a list of features")
            
        # Limit to max 5 features to reduce API calls
        if len(features) > 5:
            print(f"\n⚠️ Limiting analysis to the first 5 features to avoid rate limits")
            features = features[:5]
            
        print(f"\n✅ Extracted {len(features)} features:")
        for i, feature in enumerate(features):
            print(f"  {i+1}. {feature}")
    except Exception as e:
        print(f"❌ Failed to parse features: {str(e)}")
        print(f"Raw output: {feature_raw}")
        return
    
    # 2. Scrape product reviews
    print("\n📋 Phase 2: Scraping product reviews...")
    review_scraper = team.review_scraper()
    scrape_reviews_task = team.scrape_reviews_task()

    scrape_crew = Crew(
        agents=[review_scraper],
        tasks=[scrape_reviews_task],
        process=Process.sequential,
        verbose=True
    )
    
    max_retries = 3
    scrape_result = None
    
    for attempt in range(max_retries):
        try:
            print(f"\n⚙️ Running review scraping (attempt {attempt+1}/{max_retries})...")
            # url = format_amazon_url(product_url)
            
            # Pass product name if available
            scrape_result = scrape_crew.kickoff(inputs={
                    "product_url": product_url,
                    "target_reviews": 50,  # Reduced for testing
                    "product_name": product_name if product_name else "Test Product"
                })
            
            print("URL of the product is: ", product_url)
            break
        except Exception as e:
            print(f"\n❌ Error during review scraping: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = min(30, (2 ** attempt) * 5)
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("\n❌ Max retries reached for review scraping.")
                return
    
    # 3. Load and process reviews
    try:
        df = pd.read_csv("scraped_reviews.csv")
        if df.empty:
            print("❌ No reviews found.")
            return
        
        df_filtered = df[['name', 'brand', 'reviews.rating', 'reviews.title', 'reviews.text']]
        review_dicts = df_filtered.to_dict(orient='records')
        
        print(f"📋 Loaded {len(review_dicts)} reviews for analysis")
    except Exception as e:
        print(f"❌ Error loading reviews: {str(e)}")
        return
    
    # 4. Summarize reviews in chunks
    chunk_summaries = summarize_reviews_chunked(review_dicts, team, chunk_size=10)
    reviews_input = "\n\n".join(chunk_summaries)
    
    # 5. Analyze reviews by feature
    print("\n📋 Phase 3: Analyzing reviews by feature...")
    review_agent = team.review_analysis_agent()
    analysis_task = team.comprehensive_review_analysis_task()
    
    analysis_crew = Crew(
        agents=[review_agent],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True
    )
    
    max_retries = 3
    analysis_result = None
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                wait_time = min(60, (2 ** attempt) * 10)
                print(f"\n⏳ Waiting {wait_time} seconds before attempt {attempt+1}...")
                time.sleep(wait_time)
            
            print(f"\n⚙️ Running comprehensive feature analysis (attempt {attempt+1}/{max_retries})...")
            result = analysis_crew.kickoff(inputs={
                "features": ", ".join(features),
                "reviews": reviews_input
            })
            
            analysis_result = result
            break
        except RateLimitError as e:
            print(f"\n⚠️ Rate limit hit during review analysis (attempt {attempt+1}/{max_retries})")
            if attempt < max_retries - 1:
                print(f"Will retry soon...")
            else:
                print("\n❌ Max retries reached for review analysis.")
                print(f"Error: {str(e)}")
                return
        except Exception as e:
            print(f"\n❌ Unexpected error during review analysis: {str(e)}")
            if attempt < max_retries - 1:
                print("Will retry...")
            else:
                return
    
    if not analysis_result:
        print("\n❌ Failed to complete review analysis.")
        return
        
    try:
        # Get raw result
        raw_output = analysis_result.raw
        
        # Extract JSON from markdown if needed
        json_str = extract_json_from_markdown(raw_output)
        
        # Parse the JSON
        analysis_results = json.loads(json_str)
        
        # Save the results
        os.makedirs("output", exist_ok=True)
        with open("output/feature_analysis.json", "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n✅ Analysis complete!")
        print(f"\nAnalyzed {len(analysis_results)} features")
        
        # Show a brief summary for each feature
        for i, analysis in enumerate(analysis_results):
            feature = analysis.get("feature", "Unknown")
            sentiment = analysis.get("sentiment", "Unknown")
            verdict = analysis.get("verdict", "No verdict provided")
            
            print(f"\n{i+1}. {feature}: {sentiment}")
            print(f"   {verdict[:100]}..." if len(verdict) > 100 else f"   {verdict}")
        
        print("\nDetailed results saved to 'output/feature_analysis.json'")
        return analysis_results
    
    except Exception as e:
        print(f"❌ Error processing analysis results: {e}")
        print(f"Raw output: {raw_output}")
        
        # Still try to save the raw output for debugging
        with open("output/feature_analysis_raw.txt", "w", encoding="utf-8") as f:
            f.write(str(raw_output))
        
        print("Raw output saved to 'output/feature_analysis_raw.txt'")
        return None

if __name__ == "__main__":
    # review_analysis2()
    run_workflow()
# if __name__ == "__main__":
#     print("\n🔍 Revify Debug Tool")
#     print("1. Test Scraper Tool directly")
#     print("2. Run Debug Workflow")
    
#     choice = input("\nSelect option (1-2): ")
#     if choice == "1":
#         debug_scraper_tool()
#     elif choice == "2":
#         debug_run_workflow()
#     else:
#         print("❌ Invalid option selected.")