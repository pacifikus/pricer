If you or your team are assigned a new issue, follow the instructions below.

1. Create a new remote branch for the issue.
    * [ ] Ensure that GitHub links the branch created to the issue.

2. Set 'In progress' issue status.
 
3. Commit and push changes required to the issue branch.
   * Follow [CodeGuidelines](CodeGuidelines.md).
   * Write concise but [good commit messages](https://cbea.ms/git-commit/).

4. Finalize the work:
    * [ ] Resolve merge conflicts if any between the issue
      branch and ``master``;
    * [ ] Ensure that all the unit tests passed;
    * [ ] Ensure that UML diagrams updated according to the code changes;
    * [ ] Ensure that existing class documentation is relevant
      for each updated class;
    * [ ] Ensure that existing documentation is relevant
      for each updated method or unit test;
    * [ ] Ensure that existing comments are relevant
      for each updated method or unit test.

5. Create a pull request from the issue branch to ``master``.

6. Set 'Under Review' issue status.

7. If changes requested by a reviewer, repeat steps 2-6.

8. When pull request is approved, merge the issue branch into ``master``.
    * [ ] Create merge commit even if fast-forward is possible; 
    * [ ] Provide detailed commit message.
        * [ ] Make commit message summary match the (updated) issue title.
        * [ ] Do not mention any issues or branch names in the merge commit
          message.
        * [ ] Try to focus on *why* and *what for*, not *what* changed.

9. Delete the local and remote issue branches.

10. Ensure that 'Done' issue status is set.
