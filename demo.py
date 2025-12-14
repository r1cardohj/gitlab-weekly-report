import gitlab
from openai import OpenAI

GITLAB_TOKEN = ''
GITLAB_ADDRESS = ''

# about gitlab
gl = gitlab.Gitlab(GITLAB_ADDRESS, private_token=GITLAB_TOKEN)


gl.auth()

projects = gl.projects.list(iterator=True)
for project in projects:
    pn = project.asdict()['name']
    if pn == 'grdq-be':
        commits = project.commits.list(ref_name='main', since='2025-12-10T00:00:00Z', get_all=True)
        for commit in commits:
            print(commit.asdict()['message'])



# about deepseek

DEEPSEEK_TOKEN = ''

client = OpenAI(
        api_key=DEEPSEEK_TOKEN,
        base_url='https://api.deepseek.com',
        )

response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
                {
                    "role": "system", "content": "你是一个产品经理，善于周报总结",
                },
                {
                    "role": "user", "content": "请把下面这些明细整理成周报,".join(commit.asdict()['message'] for commit in commits)
                }
            ],
        stream=False
        )

print(response.choices[0].message.content)


