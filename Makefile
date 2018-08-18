all: lyx-notes.pdf  tgz

full: lyx-notes.pdf  tgz html

lyx-notes.pdf: lyx-notes.lyx
	lyx --export pdf lyx-notes.lyx
	cp  lyx-notes.pdf /home/sergdkv/public_html/lyx-notes/

tgz: 
	tar cfvz scripts.tar.gz scripts/*
	cp  scripts.tar.gz /home/sergdkv/public_html/lyx-notes/

html:
	$(MAKE) -C HTML
	cp  -r HTML/* /home/sergdkv/public_html/lyx-notes/HTML/
