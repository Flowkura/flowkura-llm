#!/usr/bin/env python3
"""
Test script for Diplomeo Dev chat using Giskard evaluation framework
"""

import pandas as pd
import requests
from datetime import datetime
from typing import List

# Configuration
RAGFLOW_HOST = "https://rag-staging.flowkura.com"
RAGFLOW_API_KEY = "ragflow-d4iWypSjduSHlkWb-wFOwda57ytZFsE7sxc6npOt9b8"
CHAT_ID = "d110c95bfbfc11f0861202420a000115"  # Diplomeo Dev

print("=" * 80)
print("GISKARD EVALUATION - Diplomeo Dev Chat")
print("=" * 80)
print()

# ============================================================================
# STEP 1: Test RAG connection
# ============================================================================
print("Step 1: Testing connection to Diplomeo Dev chat...")

def test_ragflow_connection():
    """Quick connection test"""
    url = f"{RAGFLOW_HOST}/api/v1/chats_openai/{CHAT_ID}/chat/completions"
    headers = {
        "Authorization": f"Bearer {RAGFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen",
        "messages": [{"role": "user", "content": "Bonjour"}],
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("choices"):
            answer = data["choices"][0]["message"]["content"]
            return True, answer
        return False, "No response"
    except Exception as e:
        return False, str(e)

connected, test_answer = test_ragflow_connection()

if connected:
    print(f"   Connection successful")
    print(f"   Test response: {test_answer[:100]}...")
else:
    print(f"   Connection failed: {test_answer}")
    exit(1)

# ============================================================================
# STEP 2: Define manual testset
# ============================================================================
print("\nStep 2: Creating manual testset (5 questions)...")

testset = [
    {
        "question": "Quelles formations en comptabilité sont disponibles ?",
        "expected_topics": ["BTS", "comptabilité", "DCG"],
        "category": "General training"
    },
    {
        "question": "Je cherche une formation d'infirmier à Lille",
        "expected_topics": ["infirmier", "Lille", "Hauts-de-France", "Diplôme d'État"],
        "category": "Training + Location"
    },
    {
        "question": "Quel est le métier de technicien radioprotection ?",
        "expected_topics": ["radioprotection", "technicien", "métier"],
        "category": "Career info"
    },
    {
        "question": "Quels sont les BTS disponibles dans le commerce ?",
        "expected_topics": ["BTS", "commerce", "MCO", "vente"],
        "category": "Specific training"
    },
    {
        "question": "Je veux faire un Bac Pro, que me conseillez-vous ?",
        "expected_topics": ["Bac Pro", "conseil", "orientation"],
        "category": "Career guidance"
    }
]

print(f"   {len(testset)} questions prepared")

# ============================================================================
# STEP 3: Create Giskard wrapper
# ============================================================================
print("\nStep 3: Creating Giskard wrapper...")

try:
    import giskard
    
    class SimpleRagflowModel:
        """Simple wrapper for Giskard"""
        
        def __init__(self, host, api_key, chat_id):
            self.host = host
            self.api_key = api_key
            self.chat_id = chat_id
            self.headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        
        def predict(self, df: pd.DataFrame) -> List[str]:
            """Method called by Giskard"""
            results = []
            
            for question in df["question"]:
                url = f"{self.host}/api/v1/chats_openai/{self.chat_id}/chat/completions"
                payload = {
                    "model": "qwen",
                    "messages": [{"role": "user", "content": question}],
                    "stream": False
                }
                
                try:
                    response = requests.post(url, headers=self.headers, json=payload, timeout=30)
                    data = response.json()
                    
                    if data.get("choices"):
                        answer = data["choices"][0]["message"]["content"]
                        results.append(answer)
                    else:
                        results.append("[No response]")
                except Exception as e:
                    results.append(f"[Error: {str(e)}]")
            
            return results
    
    # Create model
    rag_model = SimpleRagflowModel(RAGFLOW_HOST, RAGFLOW_API_KEY, CHAT_ID)
    
    # Giskard wrapper
    giskard_model = giskard.Model(
        model=rag_model.predict,
        model_type="text_generation",
        name="Diplomeo dev - Chat Ragflow",
        description="RAG agent for academic and career guidance in France",
        feature_names=["question"]
    )
    
    print("   Giskard wrapper created successfully")
    
except ImportError:
    print("   Warning: Giskard not installed - running tests without Giskard wrapper")
    giskard_model = None

# ============================================================================
# STEP 4: Evaluate RAG with testset
# ============================================================================
print("\nStep 4: Evaluating chat with testset...")

results = []

for idx, test_case in enumerate(testset, 1):
    print(f"\n   [{idx}/{len(testset)}] {test_case['question'][:60]}...")
    
    # Prepare data for Giskard
    test_df = pd.DataFrame([{"question": test_case["question"]}])
    
    if giskard_model:
        # Use Giskard with Dataset
        test_dataset = giskard.Dataset(test_df, target=None)
        predictions = giskard_model.predict(test_dataset)
        answer = predictions.raw_prediction[0]
    else:
        # Direct call without Giskard
        url = f"{RAGFLOW_HOST}/api/v1/chats_openai/{CHAT_ID}/chat/completions"
        headers = {
            "Authorization": f"Bearer {RAGFLOW_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "qwen",
            "messages": [{"role": "user", "content": test_case["question"]}],
            "stream": False
        }
        response = requests.post(url, headers=headers, json=payload)
        answer = response.json()["choices"][0]["message"]["content"]
    
    # Analyze response
    answer_lower = answer.lower()
    found_topics = [topic for topic in test_case["expected_topics"] 
                    if topic.lower() in answer_lower]
    
    score = len(found_topics) / len(test_case["expected_topics"])
    
    results.append({
        "question": test_case["question"],
        "category": test_case["category"],
        "answer": answer,
        "expected_topics": test_case["expected_topics"],
        "found_topics": found_topics,
        "score": score,
        "status": "PASS" if score >= 0.5 else "PARTIAL" if score > 0 else "FAIL"
    })
    
    print(f"      {results[-1]['status']}: Score {score:.0%} ({len(found_topics)}/{len(test_case['expected_topics'])} topics found)")

# ============================================================================
# STEP 5: Generate report
# ============================================================================
print("\nStep 5: Generating report...")

results_df = pd.DataFrame(results)

# Statistics
total_questions = len(results_df)
avg_score = results_df["score"].mean()
success_rate = (results_df["score"] >= 0.5).sum() / total_questions

# Save CSV
csv_file = f"test_diplomeo_dev_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
results_df.to_csv(csv_file, index=False, encoding='utf-8')

# Create Markdown report
report = f"""# Giskard Evaluation Report - Diplomeo Dev

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Chat ID**: {CHAT_ID}  
**Method**: Manual testset with Giskard wrapper

## Summary

- **Total questions**: {total_questions}
- **Average score**: {avg_score:.0%}
- **Success rate**: {success_rate:.0%} ({(results_df["score"] >= 0.5).sum()}/{total_questions} questions passed)

## Results by category

"""

for category in results_df["category"].unique():
    cat_results = results_df[results_df["category"] == category]
    cat_score = cat_results["score"].mean()
    report += f"- **{category}**: {cat_score:.0%}\n"

report += f"""

## Test details

"""

for idx, row in results_df.iterrows():
    report += f"""
### {row['status']} - Test {idx + 1}: {row['category']}

**Question**: {row['question']}

**RAG Response**:
```
{row['answer']}
```

**Analysis**:
- Score: {row['score']:.0%}
- Expected topics: {', '.join(row['expected_topics'])}
- Found topics: {', '.join(row['found_topics']) if row['found_topics'] else 'None'}

---
"""

report += f"""

## Conclusion

{'All tests passed successfully' if success_rate == 1.0 else 
 f'{success_rate:.0%} of tests passed - improvements possible' if success_rate >= 0.5 else
 'System needs significant improvements'}

Diplomeo Dev chat meets **{avg_score:.0%}** of expected topics on average.

## Technical details

- Giskard integration: {'Working' if giskard_model else 'Not installed'}
- Generated files:
  - {csv_file} (CSV results)
  - This report (Markdown)

"""

report_file = f"test_diplomeo_dev_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n   Report generated: {report_file}")
print(f"   CSV data: {csv_file}")

# ============================================================================
# STEP 6: Display summary
# ============================================================================
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Ragflow connection: OK")
print(f"Giskard wrapper: {'OK' if giskard_model else 'Not installed (direct test)'}")
print(f"Tests executed: {total_questions}/{len(testset)}")
print(f"Average score: {avg_score:.0%}")
print(f"Success rate: {success_rate:.0%}")
print()
print(f"Generated files:")
print(f"   - {report_file}")
print(f"   - {csv_file}")
print()
print("=" * 80)
print("Evaluation completed")
print("=" * 80)
