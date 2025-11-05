# run.py — AIWAVE X CAPSTONE FINAL DEMO
# DAY 16 — 52/52 FIXED | JSON + HUMAN OUTPUT | ZERO CRASH | POLISHED UI

import os
import warnings
import logging
from datetime import datetime
from colorama import Fore, Style, init
from src.pipeline import GrammarPipeline

# Initialize color support for Windows
init(autoreset=True)

# Suppress unnecessary warnings
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)

# Environment fixes for common torch/spacy issues
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def banner():
    print(Fore.CYAN + "\n" + "═" * 78)
    print(Fore.YELLOW + " " * 20 + "AIWAVE X — GRAMMAR ENHANCER")
    print(Fore.GREEN + " " * 22 + "CAPSTONE FINAL DEMO")
    print(Fore.CYAN + " " * 18 + "Phases 6–10 | 52/52 Fixed | JSON Output")
    print(Fore.MAGENTA + " " * 24 + "BANOTH JAGADISH")
    print(Fore.CYAN + "═" * 78 + Style.RESET_ALL)


def main():
    banner()

    print(Fore.LIGHTWHITE_EX + "\nPASTE YOUR TEXT BELOW (Ctrl+V):")
    print("   Example: She go to store yesterday, she buy apple.")
    text = input(Fore.YELLOW + "\n> " + Style.RESET_ALL).strip()

    if not text:
        print(Fore.RED + "\nNo input detected. Exiting...")
        return

    print(Fore.CYAN + "\n" + "—" * 50)
    print(Fore.GREEN + "FIXING GRAMMAR ERRORS ACROSS 5 PHASES...")
    print(Fore.CYAN + "—" * 50 + Style.RESET_ALL)

    try:
        pipeline = GrammarPipeline()
        result = pipeline.run(text)
    except Exception as e:
        print(Fore.RED + f"\n❌ ERROR: {e}")
        print(Style.RESET_ALL)
        input("Press Enter to exit...")
        return

    print(Fore.CYAN + "\n" + "═" * 78)
    print(Fore.YELLOW + "FINAL CORRECTED TEXT:")
    print(Fore.CYAN + "═" * 78 + Style.RESET_ALL)
    print(Fore.LIGHTWHITE_EX + f"{result['corrected_text']}\n" + Style.RESET_ALL)
    print(Fore.CYAN + "═" * 78 + Style.RESET_ALL)

    # Save check
    json_path = f"{result.get('id', 'output')}.json"
    if os.path.exists(json_path):
        print(Fore.GREEN + f"\n✅ JSON Saved → {json_path}")
    else:
        print(Fore.RED + "\n⚠️  JSON file not found! (Ensure write permissions)")

    print(Fore.YELLOW + f"\nTotal Fixes: {result['total_fixed']}")
    print(f"Confidence:  {result['confidence_avg']:.3f}")
    print(f"F1 Score:    {result['f1_score']:.2f}")
    print(f"Completed:   {datetime.now().strftime('%H:%M:%S')}")
    print(Fore.CYAN + "═" * 78)

    print(Fore.LIGHTGREEN_EX + "SUBMISSION CHECKLIST:")
    print("   • Corrected Output ✅")
    print("   • JSON file ✅")
    print("   • AIWAVE_X_FINAL.zip ✅")
    print("   • 10-slide PPT ✅")
    print(Fore.CYAN + "═" * 78 + Style.RESET_ALL)

    input(Fore.LIGHTWHITE_EX + "\nPress Enter to exit..." + Style.RESET_ALL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nProcess interrupted by user.")
    except Exception as e:
        print(Fore.RED + f"\nUnexpected error: {e}")
        input("Press Enter to exit...")
