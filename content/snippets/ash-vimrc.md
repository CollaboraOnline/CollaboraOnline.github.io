+++
authors = [
    "Ash"
]
title = "Ashod's tasks.json"
description = "Ashod's tasks.json"
tags = [
    "snippet",
    "ides",
    "vim",
]
+++

```bash

	" Choose a color-scheme that is readable and pleasant.
	:colorscheme murphy

	" Search highlighting.
	:set hlsearch
	:set nu
	:hi CursorLine   cterm=NONE ctermbg=black
	:hi Search ctermfg=red ctermbg=white
	:set cursorline

	set tabstop=4
	set softtabstop=0 noexpandtab
	set shiftwidth=4

	" Ignore the case when searching, unless I capitalize.
	set ignorecase
	set smartcase

	let NERDTreeIgnore = ['\.pyc$','\.o$','\.orig$','\.log$','\.gz$','^cscope.*','\~$']

	set guifont=DejaVu\ Sans\ Mono\ for\ Powerline\ 11

	" Custom word-highlighting...
	:highlight WRN ctermfg=red
	:highlight RedBG ctermfg=8 ctermbg=1
	:highlight GreenBG ctermfg=8 ctermbg=2
	:highlight KakiBG ctermfg=8 ctermbg=3
	:highlight BlueBG ctermfg=8 ctermbg=4
	:highlight MagentaBG ctermfg=8 ctermbg=5
	:highlight TealBG ctermfg=8 ctermbg=6
	:highlight WhiteBG ctermfg=8 ctermbg=7
	:highlight BlackBG ctermfg=15 ctermbg=8
	:highlight OrangeBG ctermfg=8 ctermbg=9
	:highlight DarkGreyBG ctermfg=8 ctermbg=10
	:highlight MedGreyBG ctermfg=8 ctermbg=11
	:highlight LightGreyBG ctermfg=8 ctermbg=12
	:highlight PurpleBG ctermfg=8 ctermbg=13
	:highlight WhiteBG ctermfg=8 ctermbg=15

	" Word-highlighting helpers (thanks to the internet).
	function! s:get_visual_selection()
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

	function Highlight(code)
	    let cw = expand("<cword>")
	    if len(cw) == 0
	        let sel = s:get_visual_selection()
	        return matchadd(a:code, sel)
	    else
	        return matchadd(a:code, cw)
	    endif
	endfunction

	" Use the Function keys on the keyboard to highlight all words
	" identical to the one selected or under the cursor.
	:noremap <F2> :<C-U>if exists('w:f2_match') <Bar>
	      \   silent! call matchdelete(w:f2_match) <Bar> unlet w:f2_match <Bar>
	      \ endif <Bar> let w:f2_match = Highlight("Error") <Bar>
	      \ <CR><CR>
	:noremap <F3> :<C-U>if exists('w:f3_match') <Bar>
	      \   silent! call matchdelete(w:f3_match) <Bar> unlet w:f3_match <Bar>
	      \ endif <Bar> let w:f3_match = Highlight("StatusLine") <Bar>
	      \ <CR><CR>
	:noremap <F4> :<C-U>if exists('w:f4_match') <Bar>
	      \   silent! call matchdelete(w:f4_match) <Bar> unlet w:f4_match <Bar>
	      \ endif <Bar> let w:f4_match = Highlight("Folded") <Bar>
	      \ <CR><CR>
	:noremap <F5> :<C-U>if exists('w:f5_match') <Bar>
	      \   silent! call matchdelete(w:f5_match) <Bar> unlet w:f5_match <Bar>
	      \ endif <Bar> let w:f5_match = Highlight("DiffAdd") <Bar>
	      \ <CR><CR>
	:noremap <F6> :<C-U>if exists('w:f6_match') <Bar>
	      \   silent! call matchdelete(w:f6_match) <Bar> unlet w:f6_match <Bar>
	      \ endif <Bar> let w:f6_match = Highlight("Title") <Bar>
	      \ <CR><CR>
	:noremap <F7> :<C-U>if exists('w:f7_match') <Bar>
	      \   silent! call matchdelete(w:f7_match) <Bar> unlet w:f7_match <Bar>
	      \ endif <Bar> let w:f7_match = Highlight("Identifier") <Bar>
	      \ <CR><CR>
	:noremap <F8> :<C-U>if exists('w:f8_match') <Bar>
	      \   silent! call matchdelete(w:f8_match) <Bar> unlet w:f8_match <Bar>
	      \ endif <Bar> let w:f8_match = Highlight("Statement") <Bar>
	      \ <CR><CR>
	:noremap <F9> :<C-U>if exists('w:f9_match') <Bar>
	      \   silent! call matchdelete(w:f9_match) <Bar> unlet w:f9_match <Bar>
	      \ endif <Bar> let w:f9_match = Highlight("TabLine") <Bar>
	      \ <CR><CR>
	:noremap <F12> :<C-U>if exists('w:f12_match') <Bar>
	      \   silent! call matchdelete(w:f12_match) <Bar> unlet w:f12_match <Bar>
	      \ endif <Bar> let w:f12_match = Highlight("DiffChange") <Bar>
	      \ <CR><CR>

	" Automatically highlight common words in log files for ease of
	" reading/debugging.
	:call matchadd("Error", "ERR")
	:call matchadd("Error", "ERROR")
	:call matchadd("Error", "SIG")
	:call matchadd("Error", "Assertion")
	:call matchadd("Error", "failed")
	:call matchadd("WRN", "WRN")
	:call matchadd("PurpleBG", "INF")
	:call matchadd("LightGreyBG", "TST")
	:call matchadd("TealBG", "PASS")

	" Highlight all instances of word under cursor, when idle.
	" Useful when studying strange source code.
	" Type z/ to toggle highlighting on/off.
	" Thanks to the internet.
	nnoremap z/ :if AutoHighlightToggle()<Bar>set hls<Bar>endif<CR>
	function! AutoHighlightToggle()
	  let @/ = ''
	  if exists('#auto_highlight')
	    au! auto_highlight
	    augroup! auto_highlight
	    setl updatetime=4000
	    echo 'Highlight current word: off'
	    return 0
	  else
	    augroup auto_highlight
	      au!
	      au CursorHold * let @/ = '\V\<'.escape(expand('<cword>'), '\').'\>'
	    augroup end
	    setl updatetime=500
	    echo 'Highlight current word: ON'
	    return 1
	  endif
	endfunction

	" Allow saving of files as sudo when I forgot to start vim using sudo.
	cmap w!! w !sudo tee > /dev/null %

	filetype plugin indent on

	" Remove trailing whitespace
	autocmd FileType c,cpp,python,java,php autocmd BufWritePre <buffer> %s/\s\+$//e
```
