# CONTRIBUTING.MD
## Contributing to Auto-Integrate

Thank you for considering contributing to Auto-Integrate. It's people like you that make Auto-Integrate such a great tool.


## How Can I Contribute?

## Reporting Bugs
This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

### Before Submitting A Bug Report

Perform a cursory search to see if the problem has already been reported. If it has and the issue is still open, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as GitHub issues. Create an issue and provide the following information:

1. Use a clear and descriptive title for the issue to identify the problem.
2. Describe the exact steps which reproduce the problem in as many details as possible.
3. Provide specific examples to demonstrate the steps. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples.
4. Describe the behavior you observed after following the steps and point out what exactly is the problem with that behavior.
5. Explain which behavior you expected to see instead and why.
6. Include screenshots and animated GIFs which show you following the described steps and clearly demonstrate the problem.
7. Suggesting Enhancements
8. This section guides you through submitting an enhancement suggestion for Auto-Integrate, including completely new features and minor improvements to existing functionality.

### Before Submitting An Enhancement Suggestion

1. Check the wiki to make sure your feature does not already exist.
2. Check the issue tracker to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide the following information:

1. Use a clear and descriptive title for the issue to identify the suggestion.
2. Provide a step-by-step description of the suggested enhancement in as many details as possible.
3. Provide specific examples to demonstrate the steps. Include copy/pasteable snippets which you use in those examples, as Markdown code blocks.
4. Describe the current behavior and explain which behavior you expected to see instead and why.
5. Explain why this enhancement would be useful to most Auto-Integrate users.
6. List some other projects where this enhancement exists.

## Your First Code Contribution
Unsure where to begin contributing to Auto-Integrate? You can start by looking through beginner and help-wanted issues. You can identify the categories by issue and pull request labels which are a good indicator for the level of activity. Some of the widely used labels are:

### Issue and Pull Request Labels
This section lists the labels we use to help us track and manage issues and pull requests. While not perfect, these labels help to categorize and prioritize our work and to guide our contributors.

`beginner` - Good for someone just starting with open-source
`help wanted` - Extra attention is needed
`question` - Further information is requested
`bug` - Something isn't working
`enhancement` - New feature or request
`good first issue` - Good for newcomers

## Pull Requests
The process described here has several goals:

 - Maintain Auto-Integrate's quality
 - Fix problems that are important to users
 - Engage the community in working toward the best possible Auto-Integrate
 - Enable a sustainable system for Auto-Integrate's maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

 - Follow all instructions in the template
 - Follow the styleguides
 - After you submit your pull request, verify that all status checks are passing

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Setting up the environment
Run the following commands to set up the environment:
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

## Styleguides

### Pre-commit hooks
We use pre-commit hooks to ensure that all code is formatted correctly. Before committing to the repository, please make sure to install the pre-commit hooks. Run the following command:
```bash
pre-commit install
```

This will format your code with black and flake8. It should also format the files by checking for any linting errors. This will also ensure the requirements.txt is up-to-date before your commits are pushable to the remote.

Just in case, you need to do it yourself. Make sure you are using a virtual environment to manage your dependencies. Finally, run the following command:
```bash
pip freeze > requirements.txt
```

### Git Commit Messages
We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for our commit messages. This leads to more readable messages that are easy to follow when looking through the project history. But also, it uses the git commit message to automatically determine the next version number if a release is necessary.

Some examples of our commit message specifications are:
 - Use the present tense ("Add feature" not "Added feature")
 - Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
 - Limit the first line to 79 characters or less
 - Reference issues and pull requests liberally after the first line
 - Consider starting the commit message with an applicable emoji:
🎨 :art: when improving the format/structure of the code
🐎 :racehorse: when improving performance
🚱 :non-potable_water: when plugging memory leaks
📝 :memo: when writing docs
🔥 :fire: when removing code or files
💚 :green_heart: when fixing the CI build
✅ :white_check_mark: when adding tests
🔒 :lock: when dealing with security
⬆️ :arrow_up: when upgrading dependencies
⬇️ :arrow_down: when downgrading dependencies

### Python Styleguide
All Python code must adhere to PEP8 standards. You can use any linter you want, but we recommend using flake8. It's already included in the requirements.txt file.
