from flask import Flask, jsonify, request
import json_parser
import topics_matcher


app = Flask(__name__)

@app.route('/match_topics', methods=['POST'])
def topic_matching():

    input_parsed_model = json_parser.JsonParser(request.json)
    assigned_topics_model = topics_matcher.TopicsMatcher(
        input_parsed_model.student_ids,
        input_parsed_model.topic_ids,
        input_parsed_model.student_priorities_dict,
        input_parsed_model.topic_priorities_dict,
        input_parsed_model.max_accepted_proposals
    )
    return jsonify(assigned_topics_model.get_student_topic_matches())

if __name__ == "__main__":
    app.run(debug=True)
