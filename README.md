
vim-databricks is a vim plugin that allows you to develop code locally then easily 
send it to your databricks cluster/sql warehouse.

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

Set up some config information. If you do not have a `~/.databrickscfg` file go ahead and create one now.
Then add a your databricks connection information in a TOML style.

```
[my_profile]
host = <databricks host url>
token = <databricks access token>
jobs-api-version = 2.0
```

Add other config information as global variables in your `~/.vimrc` or `~/.config/nvim/init.vim` files.

```vim
" any databricks file from your ~/.databrickscfg file
let g:databricks_profile = 'my_profile'
" the databricks cluster id you want to execute commands on
let g:databricks_cluster_id = '<cluster id>'
```

Now create some mappings to run python code using `<leader>sp` (sp = send python).
The first line allows you to execute a whole script in normal mode. The second selects
lines (not blocks) to execute in visual mode.

```vim
" vim-databricks
" normal mode get all text
nnoremap <leader>sp :call databricks#main(databricks#get_buffer_text())<CR>
" visual mode get selection - visual lines, does not work with block text
vnoremap <leader>sp :<C-u>call databricks#main(databricks#get_visual_selection())<CR>
```

# Usage

Currently everytime code is ran a new "execution context" is created then deleted. That means
variables ran previously disappear. Therefore the best way to use vim-databricks, at the moment,
is to run whole scripts. 

Managing execution contexts will be the next released feature.
