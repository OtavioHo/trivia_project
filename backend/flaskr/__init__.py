import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = [c.format() for c in Category.query.all()]
        return jsonify({'categories': categories})

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        questions = [q.format() for q in Question.query.all()]
        start = (page - 1) * 10
        end = start + 10

        if len(questions) == 0:
            abort(404)

        categories = [c.format() for c in Category.query.all()]

        return jsonify({
          'questions': questions[start:end],
          'total_questions': len(questions),
          'categories': categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        question.delete()
        return jsonify({'success': True})

    @app.route('/questions', methods=['POST'])
    def add_question():
        try:
            data = request.get_json()
            question = Question(data['question'],
                                data['answer'],
                                data['category'],
                                data['difficulty'])

            question.insert()

            return jsonify(question.format())
        except:
            abort(422)

    @app.route('/search', methods=['POST'])
    def search():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        data = request.get_json()
        questions = Question.query.filter(
                    Question.question.ilike('%{}%'.format(data['searchTerm'])))
        formattedQuestions = [q.format() for q in questions]
        categories = [c.format() for c in Category.query.all()]

        return jsonify({
          'questions': formattedQuestions[start:end],
          'total_questions': len(formattedQuestions),
          'categories': categories
        })

    @app.route('/categories/<int:id>/questions')
    def get_categories_questions(id):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.filter_by(category=id+1)
        formattedQuestions = [q.format() for q in questions]
        categories = [c.format() for c in Category.query.all()]
        return jsonify({
          'questions': formattedQuestions[start:end],
          'total_questions': len(formattedQuestions),
          'categories': categories
        })

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        data = request.get_json()
        category = data['quiz_category']['id']

        if category == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category).all()

        questions = list(filter(
                    lambda x: x not in data['previous_questions'], questions))

        if len(questions) == 0:
            abort(404)

        question = random.choice(questions)

        return jsonify({
          'question': question.format(),
          'previousQuestions': data['previous_questions'].append(question.id)
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    return app
