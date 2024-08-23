import asyncio

async def worker():
    print("Asinxron ishchi")
    await asyncio.sleep(1)

async def main():
    await asyncio.gather(worker(), worker())

asyncio.run(main())





# Output:
class UpdateChecker:
    def __init__(self, github_token, repo_name, branch):
        self.github_token = github_token
        self.repo_name = repo_name
        self.branch = branch
        self.api_url = f"https://api.github.com/repos/{self.repo_name}/commits?sha={self.branch}"
        self.headers = {"Authorization": f"token {self.github_token}"}
        self.last_commit_id = None
        self.last_commit_date = None
        self.new_commits = []
        self.check_interval = 60  # seconds
        self.update_callback = None
        self.running = False
        self.lock = asyncio.Lock()
        self.loop = asyncio.get_event_loop()
        self.task = None


    def set_update_callback(self, callback):
        self.update_callback = callback

    def start(self):
        if not self.running:
            self.running = True
            self.task = self.loop.create_task()
            self.loop.run_forever()

    def stop(self):
        if self.running:
            self.running = False
            self.task.cancel()