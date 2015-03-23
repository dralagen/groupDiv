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


How to launch the experience
-----------------------------

Before you need to define the location of your repo with 
```
export DIVA_REPO_DIR=/path/to/repo
```
After you need to setup your repo and launch a git daemon to give access to other user
```
./setupNetworkProject.sh
```

You can configure the information of other user in users.cfg formatted as 
```
[usr1]
hostname = usr1-pc
name = Name of user 1
ue = question of usr1
```

To launch the experience just with one of this commands
```
# with diva
python2.7 ./Appli_questions.py ./users.cfg 
# without diva
python2.7 ./Appli_questions.py ./users.cfg 1
```


Documents
---------

./setUpScript.sh :
Create 3 repo on /tmp/{diva1,diva2,diva3}
and add remote in each repo with friends

./scenario.sh :
- diva1 write in diva1.txt and commit it
- diva2 pull form diva1

