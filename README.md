
vim-databricks is a vim plugin that allows you to develop code locally then easily 
send it to your databricks cluster/sql warehouse.

> **Note** 
> This plugin is still under construction. All it can do now is open a buffer and
> print python code within it.

# Quick Start

Install with your favorite plugin manager. Here's how to do it with vim-plug. For vim add this to
your `~/.vimrc` or for nvim add it to your `~/.config/nvim/init.vim`

```vim
call plug#begin()

Plug 'kentkr/vim-databricks'

call plug#end()
```

Leave your rc script, reenter it, and run `:PlugInstall`.

Next make sure to install requirements.txt wherever your vim references python3 packages.

This needs some work. Here's a [thread for future reference](https://github.com/junegunn/vim-plug/issues/949)

```sh
pip3 install -r requirements.txt
```

Add this to your rc script to run python code using `<leader>sp` (sp = send python).
The first line allows you to execute a whole script in normal mode. The second selects
lines (not blocks) in visual mode.

```vim
" vim-databricks
" normal mode get all text
nnoremap <leader>sp :call databricks#main(databricks#get_buffer_text())<CR>
" visual mode get selection - visual lines, does not work with block text
vnoremap <leader>sp :<C-u>call databricks#main(databricks#get_visual_selection())<CR>
```

