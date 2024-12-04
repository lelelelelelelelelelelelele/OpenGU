# OpenGU Documentation

Welcome to the OpenGU project documentation. This project implements various methods of forgetting learning, including *segmentation forgetting*, *approximate forgetting*, and others.

## Table of Contents

- [Introduction](#introduction)
- [Segmentation Forgetting](#segmentation-forgetting)
- [Approximate Forgetting](#approximate-forgetting)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

OpenGU is a project that focuses on implementing forgetting learning methods, which are widely used in machine learning for enhancing models' efficiency. The project covers methods like segmentation forgetting and approximate forgetting.

## Segmentation Forgetting

Segmentation forgetting aims to dynamically discard irrelevant data segments, improving the model's long-term performance.

## Approximate Forgetting

Approximate forgetting involves strategies to approximate the forgetting process in a computationally efficient manner while maintaining high accuracy.

## Installation

You can install OpenGU using pip:

```bash
pip install opengu
```

## Usage

To use OpenGU, you need to import the module and choose the forgetting method based on your needs.

```python
import opengu

# Example usage of segmentation forgetting
opengu.segment_forget(data)
```

## API Documentation

Detailed API documentation can be found [here](https://opengu.readthedocs.io).

## Contributing

If you'd like to contribute to the development of OpenGU, please fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```

