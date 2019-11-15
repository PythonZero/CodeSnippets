# Install jupyter extensions
conda install -c conda-forge jupyter_contrib_nbextensions
jupyter nbextension enable codefolding/main
jupyter nbextension enable execute_time/ExecuteTime
jupyter nbextension enable notify/notify
jupyter nbextension enable jupyter-js-widgets/extension
jupyter nbextension enable nbextensions_configurator/tree_tab/main
jupyter nbextension enable collapsible_headings/main
jupyter nbextension enable toggle_all_line_numbers/main
jupyter nbextension enable codefolding/edit
jupyter nbextension enable freeze/main
jupyter nbextension enable hinterland/hinterland
jupyter nbextension enable ruler/main

pip install nb_black
