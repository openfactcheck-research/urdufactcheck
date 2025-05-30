import os
import json
import pandas as pd


# Calculate Model Cost
def calculate_model_cost(
    num_input_tokens,
    num_output_tokens,
    input_cost_per_1M_tokens,
    output_cost_per_1M_tokens,
):
    input_cost = (num_input_tokens / 1_000_000) * input_cost_per_1M_tokens
    output_cost = (num_output_tokens / 1_000_000) * output_cost_per_1M_tokens
    total_cost = input_cost + output_cost
    return round(total_cost, 2)


# Calculate Serper Cost
def calculate_serper_cost(num_credits, cost_per_credit):
    return round(num_credits * cost_per_credit, 2)


costs_by_model = {
    "gpt-4o": {
        "input_cost_per_1M_tokens": 2.5,  # $2.5 for 1M tokens
        "output_cost_per_1M_tokens": 10,  # $10 for 1M tokens
    },
    "gpt-4o-mini": {
        "input_cost_per_1M_tokens": 0.15,  # $0.15 for 1M tokens
        "output_cost_per_1M_tokens": 0.60,  # $0.60 for 1M tokens
    },
    "gpt-4.1": {
        "input_cost_per_1M_tokens": 2,  # $2.5 for 1M tokens
        "output_cost_per_1M_tokens": 8,  # $10 for 1M tokens
    },
    "gpt-4.1-mini": {
        "input_cost_per_1M_tokens": 0.4,  # $0.4 for 1M tokens
        "output_cost_per_1M_tokens": 1.6,  # $1.6 for 1M tokens
    },
}

serper_cost_per_credit = 52.5 / 50000  # $52.5 for 50k credits

DATASET_PATH = "../../datasets/processed/qa"
OUTPUT_PATH = "evaluate_llm"
RESULTS_FILE = "results.jsonl"
MODEL_COST_FILE = "model_cost.jsonl"
SERPER_COST_FILE = "serper_cost.jsonl"

# Gather all dataset names and output subdirs
datasets = [
    d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))
]
output_dirs = [
    d for d in os.listdir(OUTPUT_PATH) if os.path.isdir(os.path.join(OUTPUT_PATH, d))
]

# Prepare containers
evaluate_llm_results = {}

for dataset in datasets:
    for output_dir in output_dirs:
        # e.g. "rarr_gpt4o" → factchecker_name="rarr", model_name="gpt4o"
        llm_name, model_name = output_dir.split("_", 1)

        # Ensure nested dicts exist
        evaluate_llm_results.setdefault(llm_name, {}).setdefault(model_name, {})

        # Build file paths
        base_dir = os.path.join(OUTPUT_PATH, output_dir)
        results_path = os.path.join(base_dir, RESULTS_FILE)
        model_cost_path = os.path.join(base_dir, MODEL_COST_FILE)
        serper_cost_path = os.path.join(base_dir, SERPER_COST_FILE)

        # List all files in the directory
        print(f"Processing {base_dir}...")
        files = os.listdir(base_dir)

        # ----- Load results -----
        true_claims = 0
        false_claims = 0
        for file in files:
            if file.endswith(".jsonl"):
                # Skip the model cost and serper cost files
                if (
                    file == MODEL_COST_FILE
                    or file == SERPER_COST_FILE
                    or file == RESULTS_FILE
                ):
                    continue

                # Load the JSONL file
                file_path = os.path.join(base_dir, file)

                with open(file_path, "r") as f:
                    data = [json.loads(line) for line in f]

                    if len(data) == 3:
                        for claim in data[2]["state"]["detail"]:
                            if claim["factuality"]:
                                true_claims += 1
                            else:
                                false_claims += 1

        # Store the counts in the results dictionary
        evaluate_llm_results[llm_name][model_name]["no_of_true_claims"] = true_claims
        evaluate_llm_results[llm_name][model_name]["no_of_false_claims"] = false_claims
        evaluate_llm_results[llm_name][model_name]["total_claims"] = (
            true_claims + false_claims
        )
        evaluate_llm_results[llm_name][model_name]["percentage_true_claims"] = (
            true_claims / (true_claims + false_claims) * 100
        )

        # ----- Compute model API cost -----
        if os.path.exists(model_cost_path):
            df_cost = pd.read_json(model_cost_path, lines=True)
            if "gpt-4o-mini" in costs_by_model:
                # Check if all df_cost["model"] are the same
                if not df_cost["model"].eq("gpt-4o-mini").all():
                    print(
                        f"[Warning] Model name mismatch in {model_cost_path}: expected gpt-4o-mini, found {df_cost['model'].unique()}"
                    )
                params = costs_by_model["gpt-4o-mini"]
                cost = calculate_model_cost(
                    num_input_tokens=df_cost["prompt_tokens"].sum(),
                    num_output_tokens=df_cost["completion_tokens"].sum(),
                    input_cost_per_1M_tokens=params["input_cost_per_1M_tokens"],
                    output_cost_per_1M_tokens=params["output_cost_per_1M_tokens"],
                )
                evaluate_llm_results[llm_name][model_name]["model_cost"] = cost
            else:
                print(f"[Warning] No cost parameters for model '{model_name}'")

        # ----- Compute Serper (search) cost -----
        if os.path.exists(serper_cost_path):
            df_serp = pd.read_json(serper_cost_path, lines=True)
            cost = calculate_serper_cost(
                num_credits=df_serp["google_serper_credits"].sum(),
                cost_per_credit=serper_cost_per_credit,
            )
            evaluate_llm_results[llm_name][model_name]["serper_cost"] = cost

with open("evaluate_llm_results.json", "w") as f:
    json.dump(evaluate_llm_results, f, indent=4)
