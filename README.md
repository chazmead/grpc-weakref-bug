GRPC - Weakref and copy on MUSL based implementation issues
===

The Issue:
Repeated fields in Protocol Buffers used Weakreferences in Python, this seems to have an undesired side effect when using alpine ( possibly musl ) based distros when you attempt to deepcopy the object:

Assuming you are on an environment using the libc / package based grpcio:
```
$ ./scripts/run_local
No Weakref Issue here...
```

Now in the Alpine docker image:
```
$ ./scripts/run_docker
Sending build context to Docker daemon  31.32MB
Step 1/7 : FROM python:3.7-alpine3.10
 ---> 39fb80313465
Step 2/7 : RUN apk update && apk --no-cache add libxml2-dev python3-dev libxslt-dev g++ py3-pip
 ---> Running in d006b77a31c6
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/community/x86_64/APKINDEX.tar.gz
v3.10.2-119-gbf2d3e866c [http://dl-cdn.alpinelinux.org/alpine/v3.10/main]
v3.10.2-121-g8866800138 [http://dl-cdn.alpinelinux.org/alpine/v3.10/community]
OK: 10338 distinct packages available
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/community/x86_64/APKINDEX.tar.gz
(1/23) Installing libgcc (8.3.0-r0)
(2/23) Installing libstdc++ (8.3.0-r0)
(3/23) Installing binutils (2.32-r0)
(4/23) Installing gmp (6.1.2-r1)
(5/23) Installing isl (0.18-r0)
(6/23) Installing libgomp (8.3.0-r0)
(7/23) Installing libatomic (8.3.0-r0)
(8/23) Installing mpfr3 (3.1.5-r1)
(9/23) Installing mpc1 (1.1.0-r0)
(10/23) Installing gcc (8.3.0-r0)
(11/23) Installing musl-dev (1.1.22-r3)
(12/23) Installing libc-dev (0.7.1-r0)
(13/23) Installing g++ (8.3.0-r0)
(14/23) Installing pkgconf (1.6.1-r1)
(15/23) Installing zlib-dev (1.2.11-r1)
(16/23) Installing libxml2 (2.9.9-r2)
(17/23) Installing libxml2-dev (2.9.9-r2)
(18/23) Installing libgpg-error (1.36-r2)
(19/23) Installing libgcrypt (1.8.4-r2)
(20/23) Installing libxslt (1.1.33-r1)
(21/23) Installing libxslt-dev (1.1.33-r1)
(22/23) Installing python3 (3.7.4-r0)
(23/23) Installing python3-dev (3.7.4-r0)
Executing busybox-1.30.1-r2.trigger
OK: 280 MiB in 58 packages
Removing intermediate container d006b77a31c6
 ---> 7a342cbbb6b0
Step 3/7 : COPY ./requirements.txt /app/requirements.txt
 ---> 5c8c0737a621
Step 4/7 : RUN ["pip", "install", "-r", "/app/requirements.txt"]
 ---> Running in 283f18b157c3
Collecting grpcio==1.24.1 (from -r /app/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/0c/7b/97fce81c5f9bbe989c2f11e9d179b953f56c765af9427005e7d2f58277aa/grpcio-1.24.1.tar.gz (14.1MB)
Collecting grpcio-tools==1.24.1 (from -r /app/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/2a/46/2273fa590847a45a5cf9fdc142866a25a610d156a8bce907f386ad20469c/grpcio-tools-1.24.1.tar.gz (2.0MB)
Collecting six>=1.5.2 (from grpcio==1.24.1->-r /app/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/73/fb/00a976f728d0d1fecfe898238ce23f502a721c0ac0ecfedb80e0d88c64e9/six-1.12.0-py2.py3-none-any.whl
Collecting protobuf>=3.5.0.post1 (from grpcio-tools==1.24.1->-r /app/requirements.txt (line 2))
  Downloading https://files.pythonhosted.org/packages/ad/c2/86c65136e280607ddb2e5dda19e2953c1174f9919b557d1d154574481de4/protobuf-3.10.0-py2.py3-none-any.whl (434kB)
Requirement already satisfied: setuptools in /usr/local/lib/python3.7/site-packages (from protobuf>=3.5.0.post1->grpcio-tools==1.24.1->-r /app/requirements.txt (line 2)) (41.2.0)
Building wheels for collected packages: grpcio, grpcio-tools
  Building wheel for grpcio (setup.py): started
  Building wheel for grpcio (setup.py): still running...
  Building wheel for grpcio (setup.py): still running...
  Building wheel for grpcio (setup.py): still running...
  Building wheel for grpcio (setup.py): still running...
  Building wheel for grpcio (setup.py): still running...
  Building wheel for grpcio (setup.py): finished with status 'done'
  Created wheel for grpcio: filename=grpcio-1.24.1-cp37-cp37m-linux_x86_64.whl size=15318326 sha256=200ed13664c814c84857a0c088694a23c775969765e4b77b0c3912c1ae67edbc
  Stored in directory: /root/.cache/pip/wheels/99/fd/c5/def03996317976b1bbb570045296516dbd8c2a94002330ea75
  Building wheel for grpcio-tools (setup.py): started
  Building wheel for grpcio-tools (setup.py): still running...
  Building wheel for grpcio-tools (setup.py): still running...
  Building wheel for grpcio-tools (setup.py): still running...
  Building wheel for grpcio-tools (setup.py): still running...
  Building wheel for grpcio-tools (setup.py): still running...
  Building wheel for grpcio-tools (setup.py): still running...
  Building wheel for grpcio-tools (setup.py): still running...
  Building wheel for grpcio-tools (setup.py): finished with status 'done'
  Created wheel for grpcio-tools: filename=grpcio_tools-1.24.1-cp37-cp37m-linux_x86_64.whl size=34409225 sha256=c3c3a1ca91087d4dfad4072fd2b02e881dfc168bf9a5ee47c8e196b1fce296c3
  Stored in directory: /root/.cache/pip/wheels/bd/b3/c7/e9b594aa2b2695004c13f1de5d735b012d9d43d8694fcbcce9
Successfully built grpcio grpcio-tools
Installing collected packages: six, grpcio, protobuf, grpcio-tools
Successfully installed grpcio-1.24.1 grpcio-tools-1.24.1 protobuf-3.10.0 six-1.12.0
Removing intermediate container 283f18b157c3
 ---> 83f9b0e89f2b
Step 5/7 : COPY ./src /app/src
 ---> 05954f67ae19
Step 6/7 : WORKDIR /app/src
 ---> Running in 7d5afba470b4
Removing intermediate container 7d5afba470b4
 ---> 027c15dbe91d
Step 7/7 : CMD ["python", "main.py"]
 ---> Running in 71ee678a0d37
Removing intermediate container 71ee678a0d37
 ---> 654480f61cfe
Successfully built 654480f61cfe
Successfully tagged grpc_weakref:testing
Traceback (most recent call last):
  File "main.py", line 25, in <module>
    main()
  File "main.py", line 20, in main
    cp = copy.deepcopy(obj)
  File "/usr/local/lib/python3.7/copy.py", line 180, in deepcopy
    y = _reconstruct(x, memo, *rv)
  File "/usr/local/lib/python3.7/copy.py", line 280, in _reconstruct
    state = deepcopy(state, memo)
  File "/usr/local/lib/python3.7/copy.py", line 150, in deepcopy
    y = copier(x, memo)
  File "/usr/local/lib/python3.7/copy.py", line 240, in _deepcopy_dict
    y[deepcopy(key, memo)] = deepcopy(value, memo)
  File "/usr/local/lib/python3.7/copy.py", line 180, in deepcopy
    y = _reconstruct(x, memo, *rv)
  File "/usr/local/lib/python3.7/copy.py", line 280, in _reconstruct
    state = deepcopy(state, memo)
  File "/usr/local/lib/python3.7/copy.py", line 150, in deepcopy
    y = copier(x, memo)
  File "/usr/local/lib/python3.7/copy.py", line 220, in _deepcopy_tuple
    y = [deepcopy(a, memo) for a in x]
  File "/usr/local/lib/python3.7/copy.py", line 220, in <listcomp>
    y = [deepcopy(a, memo) for a in x]
  File "/usr/local/lib/python3.7/copy.py", line 150, in deepcopy
    y = copier(x, memo)
  File "/usr/local/lib/python3.7/copy.py", line 240, in _deepcopy_dict
    y[deepcopy(key, memo)] = deepcopy(value, memo)
  File "/usr/local/lib/python3.7/copy.py", line 180, in deepcopy
    y = _reconstruct(x, memo, *rv)
  File "/usr/local/lib/python3.7/copy.py", line 280, in _reconstruct
    state = deepcopy(state, memo)
  File "/usr/local/lib/python3.7/copy.py", line 150, in deepcopy
    y = copier(x, memo)
  File "/usr/local/lib/python3.7/copy.py", line 240, in _deepcopy_dict
    y[deepcopy(key, memo)] = deepcopy(value, memo)
  File "/usr/local/lib/python3.7/copy.py", line 159, in deepcopy
    copier = getattr(x, "__deepcopy__", None)
ReferenceError: weakly-referenced object no longer exists
```
