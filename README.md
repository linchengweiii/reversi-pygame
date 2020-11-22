# Reversi Game Project
### Prerequsite
```
pip install pygame
```
### Repo structure
```
.
├── README.md
├── agent
│   └── base_agent.py
├── arena.py
├── board.py
├── env.py
├── font
│   ├── LICENSE.txt
│   └── OpenSans-Regular.ttf
├── pygamewrapper.py
├── reversi.py
├── reversi_board.py
└── utils.py
```


### Usage
```
git clone https://github.com/cwlin1998/reversi-pygame.git
cd reversi-pygame
python3 arena.py 
```
Now you can play with an AI
### Github tutorial 
[Our slide](https://docs.google.com/presentation/d/1X0YmTyj4BNnG7E8saxtG-jH9XLWm8OiFG3L21HhgRwc/edit#slide=id.gacd295469b_2_15)
###  Preparation for Team Project
1. Fork this repo and make it private.
2. Add your teamates and TA to your repo.
3. Write your member name in your README.
For example:
    ### Team members
    - Team leader:
        - name: Cheng-Wei Lin
        - school_id: r09902000
        - github: [cwlin1998](https://github.com/cwlin1998)
    - member:
        - name: Chi-Ming Chung
        - school_id: r09944021
        - github: [MarvinChung](https://github.com/MarvinChung)

## Todo:
- Write an agent for your game:
    - You need to inherit BaseAgent and write your own agent
    ```
    class MyAgent(BaseAgent):
        def step(self, obs, reward):
            // override this function
    ```
    - Put your agent in agent_folder and name it using your team leader's github id
    For example:
    ```
    ├── agent
    │   ├── wlin1998.py
    │   └── base_agent.py 
    ```
- Test your agent
    ```
    python3 arena.py --agent1 wlin1998.MyAgent --agent2 base_agent.RandomAgent
    ```
- Write your report
    - Put your report in README.md. Learn how to write markdown
    
- Work as a team and learn how to use github and read code :100: 

## Grading policy
### Learn Github (60%)
- (**10 %**) Fork our repo
    - When your fork this repo and add TAs into your repo you get 8 points.
    - You get 2 points when you add your teammates and show their name in README.md.
- (**10 %**) Create your own branch and clean our branches
    - Delete all our branches except main.
    - Create your own branches.
- (**10 %**) protect main branch 
    - Merge only when all teammember approves.
    - Main branch should be clean. No redundacy code and bug.
    - You will need to use git branch and learn how to use git rebase.
- (**10 %**) All members should collaborate together and use pull request.
    - Disccus to each other.
- (**10 %**) use git tag to do version control
    - For example: 
        - tag name: v1.0, v1.1 ....
    - TA will grade your code using the latest tag
- (**10 %**) Write the report in your README.md
    - Describe how you made your agent. Example: What algorithm you use?
    - You can write your report on top of this README.md after forking
        - For example:
            # Reversi Game Project
            ### Team members
            - Team leader:
                - name: Cheng-Wei Lin
                - school_id: r09902000
                - github: [cwlin1998](https://github.com/cwlin1998)
            - member:
                - name: Chi-Ming Chung
                - school_id: r09944021
                - github: [MarvinChung](https://github.com/MarvinChung)
            ### Report
            I don't have time therefore I submit random agent.

### Python coding (40 %) 
- (**10 %**) Your agent can run
    - You can even copy paste our RandomAgent and you get 10 points. 
- (**10 %**) Pass the baseline
    - We will test your agent agaist RandomAgent. You need to have at least 80% win rate to get 10 points.
- (**20 %**) leaderboard
    - We will test all your agents and you will fight each others.
    - Your team will get 1 point if you beat another team. Try to beat  your classmates! :punch:
    - Don't give others your code! :no_good:
    - **The leaderboard will be announced.** 
    You have one month for this HW. Good luck!

### QA
1. Put your questions in issues inside this repo.
2. **Bonus:**
    If you find bugs :beetle: in TAs' repo. you can report it with issues and fix it with pull request then you may get bonus points. :thumbsup: