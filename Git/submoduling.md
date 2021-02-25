# Git submodule

To reference a repo as a git-submodule, run this in the folder where you want it to go, e.g. `project/module_list`

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

To delete the submodule, delete the offending folder, and in the root folder `.gitmodules` delete the entry

To use a specific branch for the submodule:

  1) cd into the folder with the submodule, e.g. `project/module_list/my_submoduled_repo`
  2) `git pull`
  3) `git branch -a` to list all branches
  4) `git checkout <branch_name>`

