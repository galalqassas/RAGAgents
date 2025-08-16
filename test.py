import os
import json
from crew import AgenticRagCrew
import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API key from environment
load_dotenv()
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    genai.configure(api_key=gemini_key)
else:
    print('[Warning] GEMINI_API_KEY not set in environment')

COMPLEX_QUERIES = [
    "I'm a vegetarian with $50 budget looking for affordable restaurants near tourist attractions in Rome, and need visa information for my US passport. How can I get around the city?",
    "Planning a family trip to Cairo in winter with kids under 10. Need a budget hotel for 5 nights and short family-friendly activities nearby.",
    "What are some authentic quick seafood dishes in Barcelona that I can try in under 2 hours between meetings? How do I get from La Rambla to Sagrada Familia afterward?",
    "As a senior couple traveling to Japan for 2 weeks in cherry blossom season, what visa do we need, where should we stay for under $150/night, and what are some relaxing cultural activities?",
    "I'm planning a 7-day trip to Italy with my vegetarian wife and two children (ages 8 and 12). We need visa information, affordable family-friendly hotels in Rome and Florence, local pasta dishes under €20, efficient transportation between cities, seasonal events in June, and cultural activities that take less than 3 hours."
]

def run_all_tests():
    os.makedirs("json_results", exist_ok=True)
    crew = AgenticRagCrew()
    results = {}
    for i, query in enumerate(COMPLEX_QUERIES, start=1):
        res = crew.run_task_by_classified_intent(query)
        outfile = os.path.join("json_results", f"query_result_{i}.json")
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2)
        results[f"Query {i}"] = {"Query": query, "ResultFile": outfile}
    summary_file = os.path.join("json_results", "test_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

def evaluate_questions(summary_file="json_results/test_summary.json"):
    with open(summary_file, 'r', encoding='utf-8') as f:
        summary = json.load(f)

    # Create model instance with gemini-2.0-flash
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Prepare combined data for a single prompt
    all_pairs_data = []
    for i, (key, info) in enumerate(summary.items(), start=1):
        question = info["Query"]
        result_path = info["ResultFile"]
        try:
            with open(result_path, 'r', encoding='utf-8') as rf:
                result_data = json.load(rf)
            pair_text = f"--- Pair {i} ---\nQuestion: {question}\nFinal Result: {json.dumps(result_data, indent=2)}\n"
            all_pairs_data.append(pair_text)
        except FileNotFoundError:
            print(f"Warning: Result file not found {result_path}")
            all_pairs_data.append(f"--- Pair {i} ---\nQuestion: {question}\nFinal Result: Error - File not found.\n")
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {result_path}")
            all_pairs_data.append(f"--- Pair {i} ---\nQuestion: {question}\nFinal Result: Error - Invalid JSON.\n")

    combined_prompt_data = "\n".join(all_pairs_data)

    # Construct the single prompt
    prompt = f"""Evaluate each of the following question-result pairs individually and concisely.

Instructions for each pair:
- Evaluate clarity, accuracy, and completeness of the result based on the question.
- Provide a short, concise evaluation for each pair.
- Clearly label the evaluation for each pair (e.g., "Evaluation for Question 1:", "Evaluation for Question 2:", etc.).

{combined_prompt_data}

Evaluations:
"""

    print("Sending combined prompt to Gemini...")
    # Send the single prompt to the model
    response = model.generate_content(prompt)
    # Print the evaluation result in the terminal
    print("Evaluation Results:\n", response.text)

    # Save the single evaluation response
    evaluation_output_file = os.path.join("json_results", "combined_evaluation.txt")
    with open(evaluation_output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(response.text)

    print(f"Combined evaluation saved to {evaluation_output_file}")

if __name__ == "__main__":
    run_all_tests()
    evaluate_questions()