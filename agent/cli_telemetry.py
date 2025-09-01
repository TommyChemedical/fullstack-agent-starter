import json
from agent.telemetry import summarize

def main():
    print(json.dumps(summarize(), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
