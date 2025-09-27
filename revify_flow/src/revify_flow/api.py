from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import sys
import threading
import time
from datetime import datetime
import traceback
import re
import json
import traceback
from datetime import datetime

# Add your project to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import your existing functions
from main import run_workflow, extract_json_from_markdown, summarize_reviews_chunked
from src.revify_flow.crews.team_revify.team_revify import TeamRevify

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your Next.js frontend

# Global variable to track analysis status
analysis_status = {
    'is_running': False,
    'progress': 0,
    'current_phase': '',
    'error': None,
    'result': None,
    'start_time': None
}

def reset_status():
    """Reset the analysis status"""
    global analysis_status
    analysis_status = {
        'is_running': False,
        'progress': 0,
        'current_phase': '',
        'error': None,
        'result': None,
        'start_time': None
    }

def update_status(progress, phase, error=None):
    """Update the analysis status"""
    global analysis_status
    analysis_status['progress'] = progress
    analysis_status['current_phase'] = phase
    if error:
        analysis_status['error'] = error
        analysis_status['is_running'] = False

def run_analysis_workflow(product_url, product_name):
    """Run the analysis workflow in a separate thread"""
    try:
        global analysis_status
        analysis_status['is_running'] = True
        analysis_status['start_time'] = datetime.now()
        
        update_status(10, "Initializing TeamRevify...")
        team = TeamRevify()
        
        # Phase 1: Extract Features
        update_status(20, "Extracting product features...")
        
        from crewai import Crew, Process
        feature_agent = team.feature_extractor()
        feature_task = team.extract_features_task()
        
        feature_crew = Crew(
            agents=[feature_agent],
            tasks=[feature_task],
            process=Process.sequential,
            verbose=False  # Reduce console output
        )
        
        feature_result = feature_crew.kickoff(inputs={"product_input": product_url})
        feature_raw = feature_result.raw
        
        update_status(40, "Processing extracted features...")
        
        # Process features
        extracted_json = extract_json_from_markdown(feature_raw)
        features_data = json.loads(extracted_json)
        
        if isinstance(features_data, dict) and "features" in features_data:
            features = features_data["features"]
        else:
            features = features_data
        
        # Limit features to avoid rate limits
        if len(features) > 5:
            features = features[:5]
        
        update_status(50, f"Scraping reviews for {len(features)} features...")
        
        # Phase 2: Scrape Reviews
        review_scraper = team.review_scraper()
        scrape_reviews_task = team.scrape_reviews_task()
        
        scrape_crew = Crew(
            agents=[review_scraper],
            tasks=[scrape_reviews_task],
            process=Process.sequential,
            verbose=False
        )
        
        scrape_result = scrape_crew.kickoff(inputs={
            "product_url": product_url,
            "target_reviews": 50,  # Reasonable number for demo
            "product_name": product_name or "Product"
        })
        
        update_status(70, "Processing scraped reviews...")
        
        # Phase 3: Load and process reviews
        import pandas as pd
        
        if not os.path.exists("scraped_reviews.csv"):
            raise Exception("No reviews were scraped. Please check the product URL.")
            
        df = pd.read_csv("scraped_reviews.csv")
        if df.empty:
            raise Exception("No reviews found in the scraped data.")
        
        df_filtered = df[['name', 'brand', 'reviews.rating', 'reviews.title', 'reviews.text']]
        review_dicts = df_filtered.to_dict(orient='records')
        
        update_status(80, "Analyzing reviews by features...")
        
        # Phase 4: Analyze reviews
        chunk_summaries = summarize_reviews_chunked(review_dicts, team, chunk_size=30)
        reviews_input = "\n\n".join(chunk_summaries)
        
        review_agent = team.review_analysis_agent()
        analysis_task = team.comprehensive_review_analysis_task()
        
        analysis_crew = Crew(
            agents=[review_agent],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=False
        )
        
        result = analysis_crew.kickoff(inputs={
            "features": ", ".join(features),
            "reviews": reviews_input
        })
        
        update_status(95, "Finalizing results...")
        
        # Process results with better error handling
        raw_output = result.raw
        print(f"DEBUG: Raw output preview: {raw_output[:500]}...")
        
        # Extract and clean JSON
        json_str = extract_json_from_markdown(raw_output)
        print(f"DEBUG: Extracted JSON preview: {json_str[:500]}...")
        
        # Try to parse JSON with multiple fallback strategies
        analysis_results = None


        # Strategy 1: Direct parsing
        try:
            analysis_results = json.loads(json_str)
            print("✅ JSON parsed successfully on first attempt")
        except json.JSONDecodeError as e:
            print(f"⚠️ First JSON parse attempt failed: {e}")
            
            # Strategy 2: Try with additional cleaning
            try:
                # More aggressive cleaning
                cleaned_json = json_str.replace('\\"', '"')  # Fix over-escaped quotes
                cleaned_json = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned_json)  # Remove control chars
                analysis_results = json.loads(cleaned_json)
                print("✅ JSON parsed successfully after cleaning")
            except json.JSONDecodeError as e2:
                print(f"⚠️ Second JSON parse attempt failed: {e2}")
                
                # Strategy 3: Try to extract just the array part if it's wrapped
                try:
                    # Look for array pattern
                    array_match = re.search(r'\[(.*)\]', json_str, re.DOTALL)
                    if array_match:
                        array_content = '[' + array_match.group(1) + ']'
                        analysis_results = json.loads(array_content)
                        print("✅ JSON parsed successfully by extracting array")
                    else:
                        raise Exception("No valid JSON array found")
                except Exception as e3:
                    print(f"⚠️ Third JSON parse attempt failed: {e3}")
                    
                    # Strategy 4: Create a fallback result
                    print("Creating fallback result from raw text...")
                    analysis_results = create_fallback_result(raw_output, features)
        
        if not analysis_results:
            raise Exception("Could not parse analysis results into valid JSON")
        
        # Ensure analysis_results is a list
        if not isinstance(analysis_results, list):
            if isinstance(analysis_results, dict):
                analysis_results = [analysis_results]
            else:
                raise Exception("Analysis results is not in expected format")

        # Save results
        os.makedirs("output", exist_ok=True)
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/feature_analysis_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        update_status(100, "Analysis completed successfully!")
        
        # Set the result
        analysis_status['result'] = {
            'features': features,
            'analysis': analysis_results,
            'total_reviews': len(review_dicts),
            'filename': filename
        }
        analysis_status['is_running'] = False
        
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}"
        print(f"Analysis error: {error_msg}")
        print(traceback.format_exc())
        update_status(0, "Analysis failed", error_msg)

def create_fallback_result(raw_output, features):
    """Create a fallback result when JSON parsing fails"""
    fallback_results = []
    
    # Try to extract information from raw text
    lines = raw_output.split('\n')
    current_feature = None
    current_analysis = {}
    
    for line in lines:
        line = line.strip()
        
        # Look for feature names
        for feature in features:
            if feature.lower() in line.lower():
                if current_feature and current_analysis:
                    fallback_results.append(current_analysis)
                
                current_feature = feature
                current_analysis = {
                    "feature": feature,
                    "sentiment": "Mixed",
                    "verdict": "Analysis could not be fully parsed due to formatting issues.",
                    "key_points": ["Raw analysis data available in logs"]
                }
                break
    
    # Add the last analysis if exists
    if current_feature and current_analysis:
        fallback_results.append(current_analysis)
    
    # If no features found, create generic fallback
    if not fallback_results:
        for feature in features:
            fallback_results.append({
                "feature": feature,
                "sentiment": "Unknown",
                "verdict": "Analysis could not be completed due to data formatting issues.",
                "key_points": ["Please try again or check the raw output logs"]
            })
    
    return fallback_results


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Revify API is running"})

@app.route('/api/analyze', methods=['POST'])
def analyze_product():
    """Start product analysis"""
    try:
        data = request.get_json()
        
        if not data or 'product_url' not in data:
            return jsonify({"error": "product_url is required"}), 400
        
        product_url = data['product_url']
        product_name = data.get('product_name', '')
        
        # Check if analysis is already running
        if analysis_status['is_running']:
            return jsonify({"error": "Analysis is already running"}), 409
        
        # Reset status and start analysis in background thread
        reset_status()
        
        # Start analysis in a separate thread
        analysis_thread = threading.Thread(
            target=run_analysis_workflow, 
            args=(product_url, product_name)
        )
        analysis_thread.daemon = True
        analysis_thread.start()
        
        return jsonify({
            "message": "Analysis started successfully",
            "status": "running"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to start analysis: {str(e)}"}), 500

@app.route('/api/status', methods=['GET'])
def get_analysis_status():
    """Get current analysis status"""
    return jsonify(analysis_status)

@app.route('/api/results', methods=['GET'])
def get_results():
    """Get analysis results"""
    if analysis_status['result']:
        return jsonify(analysis_status['result'])
    else:
        return jsonify({"error": "No results available"}), 404

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download analysis file"""
    try:
        file_path = os.path.join("output", filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)