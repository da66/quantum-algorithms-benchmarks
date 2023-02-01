
"""Utility functions to display optimization results."""

import os
import os.path
import json
from typing import List


def parse_solutions(problem_name: str, fields: List[str]) -> dict:
    """Parse the files under problems/problem_name/ and extract the summary.

    Args:
        problem_name: The name of the problem to parse.
        fields: The fields to extract from the summary.json file.
    """

    summary = {"problem": []}
    summary.update({field: [] for field in fields})

    for dirpath, dirnames, filenames in os.walk(f"problems/{problem_name}/"):
        for filename in [f for f in filenames if f == "summary.json"]:

            summary["problem"].append((os.path.normpath(dirpath).split(os.sep)[2]))

            data = json.load(open(os.path.join(dirpath, filename)))

            for field in fields:
                summary[field].append(data.get(field, {"value": "n.a."})["value"])

    return summary
