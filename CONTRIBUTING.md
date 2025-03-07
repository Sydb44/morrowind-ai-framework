# Contributing to Morrowind AI Framework

First off, thank you for considering contributing to the Morrowind AI Framework! It's people like you that make this project such an amazing tool for the Morrowind community.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible
* Include your environment details:
  - OS version
  - OpenMW version
  - Python version
  - Framework version
  - Any relevant configuration settings

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed feature
* Explain why this enhancement would be useful
* List any potential drawbacks or challenges
* Include mockups or examples if applicable

### Pull Requests

* Fill in the required template
* Follow the coding style guidelines
* Include appropriate tests
* Update documentation as needed
* End all files with a newline

## Development Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the test suite
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Coding Standards

### Python Code (AI Server)

* Follow PEP 8 style guide
* Use type hints for function parameters and return values
* Write docstrings for all public functions and classes
* Keep functions focused and single-purpose
* Use meaningful variable and function names
* Maximum line length of 100 characters
* Use f-strings for string formatting

### C++ Code (OpenMW Client)

* Follow the OpenMW coding standards
* Use modern C++ features (C++17)
* Keep header includes organized and minimal
* Use const correctness
* Prefer references over pointers where appropriate
* Document public APIs
* Use RAII principles
* Handle errors appropriately

### Lua Scripts

* Use 4 spaces for indentation
* Keep functions small and focused
* Document function parameters and return values
* Use local variables when possible
* Follow OpenMW's Lua API conventions

## Project Structure

```
morrowind_ai_framework/
├── ai-server/              # Python AI server component
│   ├── src/               # Server source code
│   ├── static-data/       # Game data and templates
│   ├── npc-profiles/      # NPC configuration files
│   └── memories/          # NPC memory storage
├── openmw-client/         # OpenMW integration component
│   ├── components/        # C++ components
│   └── resources/         # Lua scripts and resources
├── docs/                  # Documentation
├── tests/                 # Test suites
└── integration-scripts/   # Integration tools
```

## Testing

### AI Server Tests

* Write unit tests for all new functionality
* Use pytest for testing
* Maintain test coverage above 80%
* Mock external services appropriately
* Include integration tests for API endpoints

### OpenMW Client Tests

* Write unit tests for C++ components
* Include integration tests for Lua scripts
* Test across different platforms
* Verify memory management
* Test error handling

## Documentation

* Keep README.md up to date
* Document all configuration options
* Provide examples for new features
* Update API documentation
* Include troubleshooting guides

## Questions or Problems?

* Check the [Project Status](PROJECT_STATUS.md) for known issues
* Review the [Integration Guide](INTEGRATION_README.md)
* Open an issue for support questions
* Join our community discussions

## License

By contributing to this project, you agree that your contributions will be licensed under its MIT License.
