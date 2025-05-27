#!/usr/bin/env python3
"""
Meta-Crew Spawner - Entry Point
Dynamic AI crew generator using CrewAI framework
"""

import os
import sys
from dotenv import load_dotenv
from crew_generator import MetaCrewSpawner

def main():
    """Main entry point for CLI usage"""
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GROQ_API_KEY', 'MISTRAL_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing API keys for: {', '.join(missing_vars)}")
        print("Some LLM providers may not be available.")
    
    spawner = MetaCrewSpawner()
    
    if len(sys.argv) > 1:
        # CLI mode with task as argument
        task = ' '.join(sys.argv[1:])
        print(f"Processing task: {task}")
        result = spawner.process_task(task)
        print(f"\nResult:\n{result}")
    else:
        # Interactive CLI mode
        print("Meta-Crew Spawner - Interactive Mode")
        print("Enter your task description (or 'quit' to exit):")
        
        while True:
            try:
                task = input("\n> ").strip()
                if task.lower() in ['quit', 'exit', 'q']:
                    break
                if not task:
                    continue
                    
                print(f"\nProcessing: {task}")
                result = spawner.process_task(task)
                print(f"\nResult:\n{result}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
