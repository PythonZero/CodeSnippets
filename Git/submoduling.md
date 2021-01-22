# Git submodule

To reference a repo as a git-submodule, run this in the folder, e.g. `project/module_list`

```bash
git submodule add <git@bitbucket.org:company/REPO_NAME>
```

To initialise all submodules, type following from `project/module_list` directory

```bash
git submodule update --init
```

To initialise specific submodules, type following from `project/module_list` directory

```bash
git submodule update --init <repo_name>
```
