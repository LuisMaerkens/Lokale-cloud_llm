from typing import List

def rank_relevant_lines(lines: List[str], keywords: List[str]) -> List[str]:
    def score_line(line: str) -> int:
        score = 0
        for keyword in keywords:
            if keyword.lower() in line.lower():
                score += 1
        return score

    ranked = sorted(lines, key=score_line, reverse=True)
    return ranked
