alias a alias
    
a gitauto 'git commit -a -m auto'
a pull 'git pull origin master'
a gush 'git commit -a -m auto; git push origin master'

a f 'find . -name \!* -print'
a lth 'ls -lt \!* | head'
a ta 'tail -2000 \!* | most'
a pd pushd
a lk "grep \!* [^,]*.{cc,c,go,py,pl,html,h,py,s,H,U,tex,java}"
a lki "grep -i \!* [^,]*.{cc,c,go,py,pl,html,h,py,s,H,U,tex,java}"
a lkw "grep -w \!* [^,]*.{cc,c,go,py,pl,html,h,py,s,H,U,tex,java}"
a k kill -9 
a ka killall -KILL
a l ls -CF
a ll "ls -alh \!*"
a llm "ls -alh \!* | m"
a m 'less -i -M -e -c'
a jup 'jupyter notebook --port=8889 --no-browser --ip=0.0.0.0'

bindkey "^[h" backward-delete-word
bindkey "^[H" backward-delete-word
bindkey "\310" backward-delete-word
bindkey "\350" backward-delete-word
bindkey "^R" i-search-back
bindkey "^S" i-search-fwd

set prompt_info = "vagrant %m:%~> "
set prompt = "$prompt_info"

