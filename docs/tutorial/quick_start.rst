Quick Start
============

Get started with OpenGU in a few simple steps:

Step 1: Clone the Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/bwfan-bit/OpenGU.git
    cd OpenGU

Step 2: Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install general dependencies:

.. code-block:: bash

    pip install -r requirements.txt

For CUDA-specific dependencies, follow the instructions in the `Installation section <#installation>`_ above.

Step 3: Run the Main Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute the main script with desired parameters:

.. code-block:: bash

    python GULib-master/main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64

**Optional Arguments:**

- `--cuda <cuda_device>`: Specify GPU device (e.g., `0`).
- `--dataset_name <dataset_name>`: Choose from datasets like `cora`, `citeseer`, `pubmed`, etc.
- `--base_model <base_model>`: Select model architecture (`GCN`, `GAT`, `GIN`, `SAGE`, `MLP`, etc.).
- `--unlearning_methods <unlearning_methods>`: Choose unlearning method (`GraphEraser`, `GUIDE`, `CEU`, etc.).
- `--unlearn_task <unlearn_task>`: Type of unlearning task (`feature`, `node`, `edge`).
- `--downstream_task <downstream_task>`: Type of downstream task (`node`, `edge`).
- `--num_epochs <num_epochs>`: Number of training epochs.
- `--batch_size <batch_size>`: Batch size for training.

For a complete list of parameters, see the `Parameters` section in the Tutorial.

**Example Command:**

Run the **GCN** model using **GraphEraser** for **node-level unlearning** and **node-level downstream tasks**:

.. code-block:: bash

    python GULib-master/main.py --cuda 0 --dataset_name cora --base_model GCN --unlearning_methods GraphEraser --unlearn_task node --downstream_task node --num_epochs 100 --batch_size 64
