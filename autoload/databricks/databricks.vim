" path of script up to autoload/
let s:plugin_path = fnamemodify(resolve(expand('<sfile>:p:h:h')), ':p')

function! databricks#open_buffer()
    " Calculate the height for the new buffer
    let max_height = 15
    let win_count = winnr('$')
    let max_win_height = &lines - win_count
    let buf_height = min([max_height, max_win_height])

    " Create a new empty buffer and set its height
    execute "botright " . buf_height . "new"

    " not a file so it cant be written
    call setbufvar('%', '&buftype', 'nofile')

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

function! databricks#clear_execution_context()
    let l:file_path = s:plugin_path . 'databricks/.execution_context'
    call delete(l:file_path)
endfunction

function! databricks#run_python(python_code)
    " Get script path
    let script_path = s:plugin_path . 'databricks/python_sdk.py'
        
    " Construct the command to run Python
    let command = 'python3 ' . shellescape(script_path) . ' --code ' . shellescape(a:python_code) . ' --profile ' . g:databricks_profile . ' --cluster_id ' . g:databricks_cluster_id

    " Execute the Python code using system()
    let output = system(command)

    " Return result
    return output
endfunction

function! databricks#display_result(result)
    " make modifiable to overwrite buf
    call setbufvar(g:buf_num, '&modifiable', 1)

    " clear buffer
    call deletebufline(g:buf_num, 1, '$')
    " show result in buf
    call setbufline(g:buf_num, 1, split(a:result, '\n'))

    " make not modifiable again
    call setbufvar(g:buf_num, '&modifiable', 0)
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

    " Return the buffer text
    return join(buffer_text, "\n")
endfunction
