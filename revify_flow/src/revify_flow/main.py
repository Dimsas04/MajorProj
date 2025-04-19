import json
import os
from typing import Dict
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from .crews.team_revify.team_revify import TeamRevify

# Load environment variables
load_dotenv()

class FeatureList(BaseModel):
    """Model for feature extraction results"""
    features: list[str] = Field(description="List of extracted product features")

def run_feature_extraction():
    """Run only the feature extraction task from TeamRevify"""
    print("\n===== Revify Feature Extractor =====\n")
    
    # Get the product URL or name from the user
    product_url = input("Enter the product URL or name: ")

    # Create the full TeamRevify instance (this loads your YAML configs)
    team_revify = TeamRevify()
    
    # Get the feature extraction task
    feature_task = team_revify.extract_features_task()
    feature_agent = team_revify.feature_extractor()
    
    print(f"\n🔍 Extracting features for: {product_url}")
    print("⏳ This may take a moment...\n")
    
    # Create a single-task crew to run just the feature extraction
    single_task_crew = Crew(
        agents=[feature_agent],
        tasks=[feature_task],
        verbose=True,
        process=Process.sequential
    )
    
    # Execute the crew with the product URL as input
    result = single_task_crew.kickoff(inputs={"product_input": product_url})
    
    # Process and display the result
    try:
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Save the raw result
        with open("output/extracted_features_raw.txt", "w") as f:
            f.write(str(result.raw))
        
        # Try to extract and format the features
        print("\n✅ Feature extraction complete!")
        print("\nExtracted Features:")
        
        # Display the raw result since it's all we have
        print(result.raw)
        
        # For structured output, save to JSON format
        with open("output/extracted_features.json", "w") as f:
            f.write(json.dumps({"raw_output": result.raw}, indent=2))
        
        print("\nResults saved to output directory")
        print("\n===== Extraction Complete =====")
        
        return result.raw
            
    except Exception as e:
        print(f"Error processing result: {e}")
        print(f"Raw result: {getattr(result, 'raw', str(result))}")
        return {"error": str(e), "raw_result": getattr(result, 'raw', str(result))}

if __name__ == "__main__":
    run_feature_extraction()