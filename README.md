# A Command Line Interface for cloudscale.ch

## Servers

### Create

~~~
$ cloudscale-cli server create  --flavor flex-2 --name test-rm --image centos-7 --ssh-keys "$(cat ~/.ssh/id_rsa.pub)"
~~~

### List

~~~
$ cloudscale-cli server list
~~~


### List with filter tag

~~~
$ cloudscale-cli server list --filter-tag project=gemini
~~~