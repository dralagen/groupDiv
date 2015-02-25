groupDiv
========

Divergence Awareness

Install
-------

- Python 2.7 with tcl/tk support (included in last version of Python)
- Python setuptools (https://pypi.python.org/pypi/setuptools)
- gitPython (http://pythonhosted.org/GitPython/0.3.2/index.html)


Configure repositories
----------------------

Add friends branches to your local repository:
```
$ git remote add friend2 /git/repositories/project3
```

For test:

Create diva1 with some files.
```
cd diva1
touch toto
git init
git add toto

git commit -am  "test"

diva1 hala$ git pull /Users/hala/tmp/diva2

git clone diva1/ diva2
git pull

git remote add diva2 /Users/hala/tmp/diva2

git push origin master
git remote show origin
```


--------
Create 6 directory:
User1 to User6


Documents
---------

./setUpScript.sh :
Create 3 repo on /tmp/{diva1,diva2,diva3}
and add remote in each repo with friends

./scenario.sh :
- diva1 write in diva1.txt and commit it
- diva2 pull form diva1

