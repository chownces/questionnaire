# Questionnaire API
This repository contains a RESTful API designed for a questionnaire application, written in [Django Rest Framework (DRF)](https://www.django-rest-framework.org/). For a simplified implementation, authentication is not implemented, and all endpoints are public.

A summary of the API can be found in the [Endpoints](#Endpoints) and [API Summary](#API-Summary) sections below.

As this is my first project using DRF and was done within a week, the codebase might not be as polished as it can be 😅.

A demo of this project is deployed on Heroku [here](https://qns-api.herokuapp.com/forms/). Do note that it may take up to a minute for the app to load initially, as it is deployed on Heroku's free tier.

## Endpoints
* `/forms`:
    * [`GET`](#GET-forms-and-GET-formsid): Get all forms
    * [`POST`](#POST-forms-and-PUT-formsid): Create a new form
* `/forms/:id`:
    * [`GET`](#GET-forms-and-GET-formsid): Get form by id
    * [`PUT`](#POST-forms-and-PUT-formsid): Update form by id 
        * Note that all existing submissions and answers related to the form will be deleted in the current simplified implementation
* `/submissions`:
    * [`GET`](#GET-submissions-and-GET-submissionsid): Get all submissions
    * [`POST`](#POST-submissions-and-PUT-submissionsid): Create a new submission
* `/submissions/:id`:
    * [`GET`](#GET-submissions-and-GET-submissionsid): Get submission by id
    * [`POST`](#POST-submissions-and-PUT-submissionsid): Update submission by id
    
## Assumptions
1. The frontend will preprocess the form data or CSV file into JSON before sending information to this API
1. The answers sent to the `/submissions` endpoint will be given in the `display_order` of questions in the specified form.

## Getting Started
### Local Development
1. Install a stable release of Python (e.g. version 3.8).
1. Clone this repository and navigate to it using "cd" in your command line or shell tool.
1. Run `pip3 install -r requirements_dev.txt` to install all dependencies.
1. Setup the database via `python manage.py migrate`.
1. Run `python manage.py runserver` to start the server at `http://localhost:8000`

### Deployment to production
1. The deployment configuration for Heroku is already set up on the `heroku` branch. To deploy:
    * Set up a new app on Heroku, and provision a Postgres database add-on
    * Deploy the `heroku` branch of this repository to the above app on Heroku
    * Run `python manage.py migrate` on this Heroku app to setup the Postgres database

## Development
### Running Tests
Before pushing to GitHub, ensure that your code is formatted and your tests are passing.
* `black .`: Run this at the top of your project directory. Formats your code. Ensure dev dependencies are installed before running this.
* `python manage.py test`: Runs the test suite.

## Future Extensions
1. Enable filtering of submissions by form id in URL parameters
1. Store answers to radio and checkbox questions properly as integers in the database
    * Currently, the answers to these questions are stored as text for a simplified implementation
    * One possible approach to handling checkbox answers is documented [here](https://www.sqlservercentral.com/articles/storing-checkbox-responses-as-integers)
1. Authentication
    * Only authenticated users can submit and/or edit their own forms
    * Forms should not be editable by other users
    * Only form admins can view all submissions to the form
    * Implementation details will depend on usecase
1. Forms can be shared with others via a unique link

## API Summary

### GET `/forms` and GET `/forms/:id`:
Returns the form title, and form questions with their corresponding fields.

Example return:
* Note that GET `/forms` returns an array of these JSON objects
```
{
  "id": 1,
  "questions": [
      {
          "id": 1,
          "display_order": 1,
          "question": "What is your full name?",
          "question_type": "textbox",
          "choices": []
      },
      {
          "id": 2,
          "display_order": 2,
          "question": "What is your favourite colour?",
          "question_type": "checkbox",
          "choices": [
              {
                  "id": 1,
                  "choice": "blue",
                  "choice_id": 1
              },
              {
                  "id": 2,
                  "choice": "red",
                  "choice_id": 2
              },
              {
                  "id": 3,
                  "choice": "green",
                  "choice_id": 3
              },
              {
                  "id": 4,
                  "choice": "yellow",
                  "choice_id": 4
              }
          ]
      },
      {
          "id": 3,
          "display_order": 3,
          "question": "What is your most familiar coding language?",
          "question_type": "radio",
          "choices": [
              {
                  "id": 7,
                  "choice": "python",
                  "choice_id": 1
              },
              {
                  "id": 8,
                  "choice": "java",
                  "choice_id": 2
              },
              {
                  "id": 9,
                  "choice": "ruby",
                  "choice_id": 3
              },
              {
                  "id": 10,
                  "choice": "javascript",
                  "choice_id": 4
              },
              {
                  "id": 11,
                  "choice": "golang",
                  "choice_id": 5
              }
          ]
      }
  ],
  "title": "form title"
}
```

### POST `/forms` and PUT `/forms/:id`:
Example JSON:
```
{
    "title": "dummy form",
    "questions": [
    {
        "display_order": 1,
        "question": "What is your full name?",
        "question_type": "textbox"
    },
    {
        "display_order": 2,
        "question": "What is your favourite colour?",
        "question_type": "checkbox",
        "choices": [
            {
                "choice_id": 1,
                "choice": "blue"
            },
            {
                "choice_id": 2,
                "choice": "red"
            },
            {
                "choice_id": 3,
                "choice": "green"
            },
            {
                "choice_id": 4,
                "choice": "yellow"
            }
        ]
    },
    {
        "display_order": 3,
        "question": "What is your most familiar coding language?",
        "question_type": "radio",
        "choices": [
            {
                "choice_id": 1,
                "choice": "python"
            },
            {
                "choice_id": 2,
                "choice": "java"
            },
            {
                "choice_id": 3,
                "choice": "ruby"
            },
            {
                "choice_id": 4,
                "choice": "javascript"
            },
            {
                "choice_id": 5,
                "choice": "golang"
            }
        ]
    }
    ]
}
```

### GET `/submissions` and GET `/submissions/:id`:
Returns submission answers and the corresponding form.

Example return:
* Note that GET `/submissions` returns an array of these JSON objects
```
{
  "id": 1,
  "answers": [
      {
          "id": 1,
          "answer": "John Doe",
          "question_id": 1
      },
      {
          "id": 2,
          "answer": "2",
          "question_id": 2
      },
      {
          "id": 3,
          "answer": "4",
          "question_id": 3
      }
  ],
  "form_id": {
      "id": 1,
      "questions": [
          {
              "id": 1,
              "display_order": 1,
              "question": "What is your full name?",
              "question_type": "textbox",
              "choices": []
          },
          {
              "id": 2,
              "display_order": 2,
              "question": "What is your favourite colour?",
              "question_type": "checkbox",
              "choices": [
                  {
                      "id": 1,
                      "choice": "blue",
                      "choice_id": 1
                  },
                  {
                      "id": 2,
                      "choice": "red",
                      "choice_id": 2
                  },
                  {
                      "id": 3,
                      "choice": "green",
                      "choice_id": 3
                  },
                  {
                      "id": 4,
                      "choice": "yellow",
                      "choice_id": 4
                  },
                  {
                      "id": 5,
                      "choice": "purple",
                      "choice_id": 5
                  },
                  {
                      "id": 6,
                      "choice": "pink",
                      "choice_id": 6
                  }
              ]
          },
          {
              "id": 3,
              "display_order": 3,
              "question": "What is your most familiar coding language?",
              "question_type": "radio",
              "choices": [
                  {
                      "id": 7,
                      "choice": "python",
                      "choice_id": 1
                  },
                  {
                      "id": 8,
                      "choice": "java",
                      "choice_id": 2
                  },
                  {
                      "id": 9,
                      "choice": "ruby",
                      "choice_id": 3
                  },
                  {
                      "id": 10,
                      "choice": "javascript",
                      "choice_id": 4
                  },
                  {
                      "id": 11,
                      "choice": "golang",
                      "choice_id": 5
                  }
              ]
          }
      ],
      "title": "form title"
  }
}
```

### POST `/submissions` and PUT `/submissions/:id`:
Example JSON:
* Note that the order of answers should correspond to the display order of the questions in the form
```
{
  "form_id": 1,
  "answers": [
      {
          "answer": "John Doe",
          "question_type": "textbox"
      },
      {
          "answer": "2",
          "question_type": "checkbox"
      },
      {
          "answer": "4",
          "question_type": "radio"
      }
  ]
}
```
