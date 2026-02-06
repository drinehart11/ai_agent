# local ai agent - connects to LM Studio
# Note: .env file stored in parent folder
#
# Last Edit: 6-FEB-2026
# Author: Duane Rinehart (drinehar@sdccd.edu)


from email import parser
import os, sys
from pptx import Presentation
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import argparse

# from lib.present import load_presentation, iter_text_shapes, process_presentation, save_with_suffix

##############################################
#CONSTANTS
DEBUG = False
SYSTEM_PROMPTS = {
    "shorten": "You are an editor. Shorten the text while preserving all key information and bullet structure.",
    "simplify": "You are an editor. Rewrite the text in simpler, clearer language for a general audience.",
    "formalize": "You are an editor. Rewrite the text in a more formal, professional tone.",
}


def load_parent_env(debug: bool = False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    env_path = os.path.join(parent_dir, ".env")

    if os.path.exists(env_path):
        load_dotenv(env_path)
        return True
    else:
        print(f"No .env found in parent directory: {env_path}")
        return False
    

def parse_args():
    parser = argparse.ArgumentParser(
            description="Ai Agent argument ingestion"
        )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output (overrides default DEBUG=False)"
    )
    parser.add_argument(
        "--action",
        choices=["process", "testapi"],
        default="process",
        help="Choose 'process' to edit a PPTX or 'testapi' to verify LLM connectivity",
    )
    parser.add_argument(
        "pptx_path",
        nargs="?",
        help="Path to the input .pptx file (required unless --action testapi)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not modify the file, just print what would be edited",
    )
    return parser.parse_args()


def call_local_llm(ENDPOINT, MODEL, system_prompt: str, original_text: str) -> str:
    prompt = (
        f"{system_prompt}\n\n"
        "Here is slide text from a PowerPoint presentation. "
        "Return ONLY the revised text, no commentary.\n\n"
        f"{original_text}"
    )

    payload = {
        "model": MODEL,
        "input": prompt
    }

    resp = requests.post(ENDPOINT, json=payload, timeout=None)
    resp.raise_for_status()
    data = resp.json()

    return data["output"][-1]["content"].strip()


def main():
    args = parse_args()

    # Load .env with debug flag
    if not load_parent_env(debug=DEBUG):
        if args.debug:
            print("Exiting: .env in parent is required.")
        sys.exit(1)

    if args.debug:
        print("*" * 40)
        print("RECEIVED ARGUMENTS:")
        print("\t--action:", args.action)
        print("\t--pptx_path:", args.pptx_path)
        print("\t--dry-run:", args.dry_run)
        # print("\t--option_type:", args.option_type)
        # print(f"\t--rr_ratio: ≤ {args.rr_ratio}")
        # if args.option_type and args.option_type.lower() == "put":
        #     print("\t--pct_below:", args.pct_below)
        # if args.option_type and args.option_type.lower() == "call":
        #     print("\t--pct_above:", args.pct_above)
        # print("\t--spread_width:", args.spread_width)
        # print("\t--debug:", args.debug)
        print("*" * 40)

    # Read env
    ENDPOINT = os.getenv("LOCAL_LLM_ENDPOINT")
    API_KEY = os.getenv("API_KEY")
    MODEL = os.getenv("MODEL_NAME")
    DEFAULT_MODE = os.getenv("DEFAULT_MODE", "shorten")

    if not ENDPOINT:
        print("LOCAL_LLM_ENDPOINT not found in environment.")
        sys.exit(1)
    print("CONNECTING TO LOCAL LLM...")

    try:
        reply = call_local_llm(ENDPOINT, MODEL, "You are a test agent.", "Say 'API OK'.")
        print("API response:", reply)
    except Exception as e:
        print("API test failed:", e)
    return

    if not args.pptx_path:
        print("Error: pptx_path is required when using --action process")
        sys.exit(1)

    prs = Presentation(args.pptx_path)
    process_presentation(prs, mode=DEFAULT_MODE, dry_run=args.dry_run)

    if not args.dry_run:
        new_path = save_with_suffix(prs, args.pptx_path, DEFAULT_MODE)
        print(f"\nSaved updated presentation to: {new_path}")
    else:
        print("\nDry run complete. No file was saved.")



if __name__ == "__main__":
    main()