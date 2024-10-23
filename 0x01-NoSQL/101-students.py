#!/usr/bin/env python3
"""
A Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    Responsible for returning all students sorted bu average score
    """
    students_avg_score = mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
    return students_avg_score
