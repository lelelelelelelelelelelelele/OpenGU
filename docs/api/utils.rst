Utils
=====

The `utils` module contains utility functions and classes for various purposes, including dataset operations and graph processing.

Dataset Utilities
-----------------

.. automodule:: utils.dataset_utils
    :members:
    :undoc-members:
    :special-members: __init__
    :show-inheritance:

General Utilities
-----------------

Graph Filtering Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: utils.utils.filter_edge_index_1
.. autofunction:: utils.utils.filter_edge_index_2
.. autofunction:: utils.utils.filter_edge_index_3
.. autofunction:: utils.utils.filter_edge_index

Graph Processing Class
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: utils.utils.MyGraphConv
    :members:

Logistic Regression Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: utils.utils.get_propagation
.. autofunction:: utils.utils.lr_optimize
.. autofunction:: utils.utils.lr_loss
.. autofunction:: utils.utils.lr_eval
.. autofunction:: utils.utils.lr_grad
.. autofunction:: utils.utils.lr_hessian_inv
.. autofunction:: utils.utils.ovr_lr_loss
.. autofunction:: utils.utils.ovr_lr_eval
.. autofunction:: utils.utils.ovr_lr_optimize