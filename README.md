# BuzzHub - API Repository

Welcome to the BuzzHub API repository! This repository contains Python Lambda functions used as GraphQL resolver functions for the BuzzHub project. The API handles data retrieval and manipulation for the BuzzHub UI.

## Getting Started

To get started with the BuzzHub API, please follow the instructions below:

1. Clone the repository to your local machine using the following command:

`git clone github.com/Kryps1s/BuzzHub-API`

2. Navigate to the project directory:

`cd BuzzHub-API`

3. Install the project dependencies by running the following command:

`pip install -r requirements.txt`

4. Configure the necessary environment variables. You will need to create a `.env` file with the required variables

## Running pylint

To run pylint and perform code analysis, execute the following command:

`pylint *`

This will analyze the Python source code files located in the entire project and provide feedback based on the defined linting rules.

## Running pytest

To run pytest and execute the test suite, use the following command:

`pytest tests`

This will run all the tests located in the `tests` directory and display the test results along with any failures or errors encountered.

## Project Structure

The project structure of the BuzzHub API repository is as follows:

- `/lambdas`: This directory contains the Python Lambda functions serving as GraphQL resolver functions.
- `/tests`: This directory contains the test suite for the API functions.
- `requirements.txt`: The file specifying the project's dependencies.
- `.env`: The file for configuring environment variables.

## Technologies Used

The BuzzHub API is built using the following technologies:

- [Python](https://www.python.org/): A powerful programming language with a focus on simplicity and readability.
- [AWS Lambda](https://aws.amazon.com/lambda/): A serverless computing service for running code without managing infrastructure.
- [GraphQL](https://graphql.org/): A query language and runtime for APIs, enabling efficient data retrieval and manipulation.


## Contributing

We welcome contributions to the BuzzHub project! If you would like to contribute, please follow these guidelines:

1. Fork the repository on GitHub.
2. Create a new branch with a name based off a user story on the [Kanban Board](https://tree.taiga.io/project/kryps1s-bee/kanban).
3. Commit your changes and push them to your forked repository.
4. run the commands `pylint *` and `pytest tests` to ensure that there are no linting errors or failed test cases.
5. Submit a pull request to the main repository, describing your changes in detail.

## License

The BuzzHub project is licensed under the [MIT License](LICENSE). Feel free to modify and use the code for your own purposes.

## Contact

If you have any questions or feedback regarding the BuzzHub project, please contact me at [eoreilly1994@gmail.com]. I appreciate your interest and support!
