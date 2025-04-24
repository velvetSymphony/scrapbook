## Limitations:

- Hard coded markdown headers in the code.
- Generate only once per day.
    - If you attempt to run it more than once, it will still work, it just appends it to the same log file (all the headers).
- No flexibility to add more headers/remove headers at the moment.

## Ideas/Potential solutions:

- [x] Make it config friendly, i.e enable the user to create a config file which will influence the behaviour of the tool.
    - This can be used to customise the structure of the log file.
    - Generate a sample config template (a default one).
    - And potentially other things (idk right now).

- [] Create installation script for tool. Make it system-wide (?).
- [] Enable users to edit current log file for the day or create a new log file for the day.
- [] Provide option flags for user to customise specific parts of the log file once generated.
    - If you've already generated one for the day and you've only filled out the task bit:
        - Provide user with options on what to modify/change?
        ```shell
        scrapbook -c "Learnings"
        ```
        - where `-c` is change.
        - This will change/modify the Learnings section.
    - Provide prompt for user when a log file for the day has already been generated:
    ```shell
    scrapbook 
    ```
    ```text
    You've already generated a log file for the day, would you like to edit the current log file or generate a new one?
    ```
- [] Provide default values for certain headers:
    - `Project Name` is most likely to remain same for a couple days/weeks/months.
    - Makes it easier for the user to skip through things.

- [] Put in a help function for users.
- [] Directory specific config (i.e change path names etc)
    - Hierarchical config files, so having a config file in the current directory will override the base config.
    - This is probably useful if you have multiple projects and want to manage how the directory, structure of the logs will look like per project.
- [] Enable moving between words (if that makes sense). At the moment, you can only type uni-directionally or backspace the whole sentence you're typing. You cannot for example use your arrow keys to move between words in a sentence, it prints out the ANSI codes for those keys. Find a way to move between the words easily.

## Improvements

- [x] Added a basic config file behaviour to customise headings to be used for taking notes according to projects.
    - Falls back to a default config file if no config file found for directory.
    - Can be changed per directory.

- [x] More error handling, better checks to validate config file, headings.
