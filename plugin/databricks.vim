" Title:        vim-databricks
" Description:  A plugin to send py and sql commands directly to databricks
" Maintainer:   kentkr

if !exists('g:loaded_databricks') 
    let g:loaded_databricks = 1
    runtime autoload/databricks/databricks.vim
endif

