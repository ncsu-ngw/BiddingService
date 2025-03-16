from flask import Flask, jsonify, request
from app import json_parser
from app import topics_matcher

app = Flask(__name__)

@app.route('/match_topics', methods=['POST'])
def topic_matching():
    try:
        input_parsed_model = json_parser.JsonParser(request.json)
    except Exception as e:
        return jsonify({"error": f"Bad Request: {str(e)}"}), 400

    try:
        assigned_topics_model = topics_matcher.TopicsMatcher(
            input_parsed_model.student_ids,
            input_parsed_model.topic_ids,
            input_parsed_model.student_priorities_dict,
            input_parsed_model.topic_priorities_dict,
            input_parsed_model.max_accepted_proposals
        )
        result = assigned_topics_model.get_student_topic_matches()
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
