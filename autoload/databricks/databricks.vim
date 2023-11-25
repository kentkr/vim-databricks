
function! databricks#open_buffer()
    " Calculate the height for the new buffer
    let max_height = 15
    let win_count = winnr('$')
    let max_win_height = &lines - win_count
    let buf_height = min([max_height, max_win_height])

    " Create a new empty buffer and set its height
    execute "botright " . buf_height . "new"
    " make it nonmodifiable
    setlocal readonly nomodifiable

    " return the new buffer number
    return bufnr('%')
endfunction

function! databricks#reopen_buffer(buf_num)
    " Calculate the height for buffer
    let max_height = 15
    let win_count = winnr('$')
    let max_win_height = &lines - win_count
    let buf_height = min([max_height, max_win_height])

    " Reopen at buf height
    execute "botright sb " . a:buf_num . " | resize " . buf_height
endfunction

function! databricks#run_python(python_code)
    " Escape single quotes in the Python code
    let python_code_escaped = substitute(a:python_code, "'", "\\'", "g")
    let python_code_escaped = substitute(python_code_escaped, "\\", "\\\\", "g")

    " Construct the command to run Python
    let command = 'python3 -c "' . python_code_escaped . '"'

    " Execute the Python code using system()
    let output = system(command)

    " Return result
    return output
endfunction

function! databricks#display_result(result)
    " clear buffer
    call deletebufline(g:buf_num, 1, '$')

    " show result in buf
    call setbufline(g:buf_num, 1, split(a:result, '\n'))
endfunction

function! databricks#main(cmd)
    " Open a buffer if one is not set
    if !exists('g:buf_num')
        let g:buf_num = databricks#open_buffer()
    endif

    " reopen it if its closed
    if bufwinnr(g:buf_num) == -1
        call databricks#reopen_buffer(g:buf_num)
    endif

    " run code
    let output = databricks#run_python(a:cmd)

    " display that s    
    call databricks#display_result(output)
endfunction

function! databricks#send_to_main() range
  let selected_text = @"
  " Replace special characters for proper shell command handling if needed
  let sanitized_text = shellescape(selected_text)
  echo sanitized_text

  " Call the function with the selected text as cmd argument
  call databricks#main(selected_text)
endfunction

function! databricks#get_visual_selection()
    " Why is this not a built-in Vim script function?!
    let [line_start, column_start] = getpos("'<")[1:2]
    let [line_end, column_end] = getpos("'>")[1:2]
    let lines = getline(line_start, line_end)
    if len(lines) == 0
        return ''
    endif
    let lines[-1] = lines[-1][: column_end - (&selection == 'inclusive' ? 1 : 2)]
    let lines[0] = lines[0][column_start - 1:]
    return join(lines, "\n")
endfunction

function! databricks#get_buffer_text()
    " Get all lines into a list
    let buffer_text = getline(1, '$')

    " Print or process the buffer text (example: print line by line)
    "for line in buffer_text
    "    echo line
    "endfor

    " Return the buffer text
    return join(buffer_text, "\n")
endfunction

" normal mode get all text
"nnoremap <leader>sp :call databricks#main(databricks#get_buffer_text())<CR>
" visual mode get selection - visual lines, does not work with block text
"vnoremap <leader>sp :<C-u>call databricks#main(databricks#get_visual_selection())<CR>
