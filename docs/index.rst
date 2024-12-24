OpenGU Documentation
====================

Welcome to the **OpenGU** documentation! OpenGU is an open-source benchmark platform designed for **Graph Unlearning (GU)**. It facilitates the evaluation and development of GU methodologies by providing standardized datasets, state-of-the-art GU algorithms, and versatile tools.

Introduction
------------

**OpenGU** offers a unified framework that integrates multiple GU algorithms and supports a variety of downstream tasks across several Graph Neural Network (GNN) backbones. This platform enables flexible unlearning requests and ensures comprehensive and fair evaluations of GU methods, addressing the unique challenges posed by complex relational data.

Key Features
~~~~~~~~~~~~

- **Standardized Benchmark**: Provides consistent datasets and evaluation metrics for fair comparison of GU methods.
- **State-of-the-Art Algorithms**: Includes numerous GU algorithms categorized into Partition-based, IF-based, Learning-based, and others.
- **Multi-Domain Support**: Supports diverse datasets across different application domains and multiple GNN backbones.
- **Flexible Evaluation**: Facilitates cross-task evaluations and assesses GU algorithms on effectiveness, robustness, and efficiency.

Installation
------------

**Prerequisites**

- **Python**: 3.8.0 or higher

Step 1: Create and Activate a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's recommended to use a virtual environment to manage dependencies.

Using `venv`
~~~~~~~~~~~~

.. code-block:: bash

    python -m venv venv
    # Activate the virtual environment
    # Windows
    venv\Scripts\activate
    # Unix/MacOS
    source venv/bin/activate

Using `conda`
~~~~~~~~~~~~~

.. code-block:: bash

    conda create -n opengu_env python=3.8
    conda activate opengu_env

Step 2: Install OpenGU
~~~~~~~~~~~~~~~~~~~~~~

You can install OpenGU using pip or from the GitHub repository for local development.

1. **Using Pip**

   Install OpenGU directly from PyPI:

   .. code-block:: bash

       pip install opengu

2. **Installing from GitHub for Local Development**

   Clone the repository and install OpenGU in editable mode:

   .. code-block:: bash

       git clone https://github.com/bwfan-bit/OpenGU.git
       cd OpenGU
       pip install -e .

Step 3: Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CUDA-Specific Dependencies (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For GPU support, install the appropriate versions of PyTorch and CuPy that match your CUDA version.

**Example for CUDA 12.1:**

.. code-block:: bash

    pip install torch==2.2.1 torchvision==0.17.1 torchaudio --index-url https://download.pytorch.org/whl/cu121
    pip install cupy-cuda121

*Ensure your system has the appropriate CUDA version installed. Refer to the `CuPy Installation Guide <https://docs.cupy.dev/en/stable/install.html#using-pip>`_ for more details.*

General Dependencies
^^^^^^^^^^^^^^^^^^^^

Install the remaining dependencies from the `requirements.txt` file:

.. code-block:: bash

    pip install -r requirements.txt

Verify Installation
~~~~~~~~~~~~~~~~~~~~

After installation, verify that OpenGU is installed correctly:

.. code-block:: bash

    python -c "import opengu; print(opengu.__version__)"



Cite
----

If you use OpenGU in your research, please cite the following paper:

.. code-block:: none

    @inproceedings{openGU2024,
        title={OpenGU: A Benchmark Platform for Graph Unlearning},
        author={Your Name and Co-authors},
        booktitle={Proceedings of the XYZ Conference},
        year={2024},
        organization={Conference Organization}
    }

.. toctree::
    :maxdepth: 1
    :caption: Tutorial

    tutorial/quick_start
    tutorial/example
    tutorial/parameters

.. toctree::
    :maxdepth: 2
    :caption: API Documentation

    api/dataset
    api/pipeline
    api/task
    api/unlearning
    api/utils

---
