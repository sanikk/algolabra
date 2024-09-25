from invoke import task

@task
def start(c):
    c.run('python main.py', pty=True)

@task
def test(c):
    c.run('pytest algolabra', pty=True)

@task
def coverage(c):
    c.run("coverage run --branch -m pytest algolabra", pty=True)

@task(coverage)
def coverage_report(c):
    c.run("coverage report")