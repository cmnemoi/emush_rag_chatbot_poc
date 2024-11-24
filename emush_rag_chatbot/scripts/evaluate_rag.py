import asyncio
import csv
import datetime
import json
import logging
import uuid
from pathlib import Path
from typing import List, Dict

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from tqdm import tqdm

from emush_rag_chatbot.config import settings
from emush_rag_chatbot.src.rag_chain import RAGChain

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EVAL_PROMPT = """You are an expert evaluator for question-answering systems. 
Your task is to evaluate the quality of an AI assistant's response compared to the ground truth answer.

Question: {question}

Ground Truth Answer: {ground_truth}

AI Assistant's Response: {response}

Please evaluate the response based on the following criteria:
1. Correctness: Is the information provided accurate compared to the ground truth? (0-5)
2. Completeness: Does it cover all key points from the ground truth? (0-5)
3. Relevance: Does it directly address the question asked? (0-5)

Provide your evaluation in JSON format with the following fields:
- correctness_score: numeric score (0-5)
- completeness_score: numeric score (0-5)
- relevance_score: numeric score (0-5)
- explanation: brief explanation of the scores
- overall_score: average of all scores (0-5)

Be strict in your evaluation. The response should be marked down for any inaccuracies or missing key information."""


class RAGEvaluator:
    def __init__(self):
        self.rag_chain = RAGChain()
        self.evaluator_llm = ChatOpenAI(
            model="gpt-4o-mini", temperature=0, seed=42, openai_api_key=settings.OPENAI_API_KEY
        )
        self.eval_prompt = ChatPromptTemplate.from_messages([("system", EVAL_PROMPT)])
        self.output_parser = JsonOutputParser()

    async def evaluate_single_response(self, question: str, ground_truth: str, response: str) -> Dict:
        """Evaluate a single RAG response against ground truth"""
        chain = self.eval_prompt | self.evaluator_llm | self.output_parser

        result = await chain.ainvoke({"question": question, "ground_truth": ground_truth, "response": response})

        return result

    async def evaluate_test_set(self, test_file: Path) -> List[Dict]:
        """Evaluate entire test set"""
        results = []

        with open(test_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            test_cases = list(reader)

        for case in tqdm(test_cases, desc="Evaluating responses"):
            # Generate RAG response
            response, _ = await self.rag_chain.generate_response(case["question"])

            # Evaluate response
            evaluation = await self.evaluate_single_response(
                question=case["question"], ground_truth=case["ground_truth"], response=response
            )

            results.append(
                {
                    "question": case["question"],
                    "ground_truth": case["ground_truth"],
                    "rag_response": response,
                    "evaluation": evaluation,
                }
            )

        return results

    def save_results(self, results: List[Dict], output_file: Path):
        """Save evaluation results to CSV file"""
        # Add metadata to results
        evaluation_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        # Flatten results for CSV
        flattened_results = []
        for result in results:
            row = {
                "evaluation_id": evaluation_id,
                "timestamp": timestamp,
                "dataset_name": "test_set_v1",
                "rag_params": {
                    "top_k": 4,
                    "model": "gpt-4",
                    "temperature": 0
                },
                "question": result["question"],
                "ground_truth": result["ground_truth"],
                "rag_response": result["rag_response"],
                "correctness_score": result["evaluation"]["correctness_score"],
                "completeness_score": result["evaluation"]["completeness_score"],
                "relevance_score": result["evaluation"]["relevance_score"],
                "overall_score": result["evaluation"]["overall_score"],
                "explanation": result["evaluation"]["explanation"]
            }
            flattened_results.append(row)
            
        # Save as CSV, appending if file exists
        output_file = output_file.with_suffix('.csv')
        file_exists = output_file.exists()
        
        mode = "a" if file_exists else "w"
        with open(output_file, mode, newline="", encoding="utf-8") as f:
            fieldnames = flattened_results[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(flattened_results)


async def main():
    evaluator = RAGEvaluator()

    # Get script directory
    script_dir = Path(__file__).parent
    test_file = script_dir / "test_set.csv"
    output_file = script_dir / "evaluation_results"  # Extension will be added in save_results

    # Run evaluation
    results = await evaluator.evaluate_test_set(test_file)

    # Save results
    evaluator.save_results(results, output_file)

    # Calculate and display average scores
    avg_scores = {
        "correctness": sum(r["evaluation"]["correctness_score"] for r in results) / len(results),
        "completeness": sum(r["evaluation"]["completeness_score"] for r in results) / len(results),
        "relevance": sum(r["evaluation"]["relevance_score"] for r in results) / len(results),
        "overall": sum(r["evaluation"]["overall_score"] for r in results) / len(results),
    }

    print("\nEvaluation Results:")
    print(f"Average Correctness Score: {avg_scores['correctness']:.2f}/5")
    print(f"Average Completeness Score: {avg_scores['completeness']:.2f}/5")
    print(f"Average Relevance Score: {avg_scores['relevance']:.2f}/5")
    print(f"Average Overall Score: {avg_scores['overall']:.2f}/5")
    print(f"\nDetailed results saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
