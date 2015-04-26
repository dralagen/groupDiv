groupDiv
========

The divergence awareness interface

![Divergence Awareness Interface](https://cloud.githubusercontent.com/assets/6002406/7339486/f0236322-ec70-11e4-98eb-3e80e3151b7c.png)

Install
-------

- Python 2.7 with tcl/tk support (included in last version of Python)
- Python setuptools (https://pypi.python.org/pypi/setuptools)
- gitPython (http://pythonhosted.org/GitPython/0.3.2/index.html)

How to launch
-------------

```
python2.7 ./diva.py
```

Configuration
-------------

In diva.cfg
```
my_repo =/tmp/diva
my_branch = master
friends_branch = usr1/master usr2/master
```

- `my_repo` : path of my current repository watch by groupDiv
- `my_branch` : branch watch by groupDiv
- `friends_branch` : friends branch watch by groupDiv for calculate the divergence

---

Experience 
==========

User interface

![Writing Tab](https://cloud.githubusercontent.com/assets/6002406/7339535/13f142f0-ec72-11e4-9e9e-d04c4048848a.png)
![Review Tab](https://cloud.githubusercontent.com/assets/6002406/7339537/13f28a84-ec72-11e4-9388-a75a826afe5b.png)
![Commit history](https://cloud.githubusercontent.com/assets/6002406/7339536/13f13a26-ec72-11e4-8585-8168276e9c47.png)

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

