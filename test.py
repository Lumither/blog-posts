from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style


# 自定义自动补全类
class InlineCompleter(Completer):
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for cmd in self.commands:
            if cmd.startswith(word):
                yield Completion(
                    cmd,
                    start_position=-len(word),
                    # 设置 inline 显示样式
                    display_meta="",
                    display=(f">>> {cmd} "),  # 自定义显示格式
                )


# 配置样式
style = Style.from_dict({
    "completion-menu.completion": "bg:#008888 #ffffff",
    "completion-menu.completion.current": "bg:#00aaaa #000000",
    "completion-menu.meta": "bg:#003333 #ffffff",
})

# 可用命令列表
commands = [
    "print", "prompt", "exit",
    "help", "list", "save",
    "load", "execute", "config"
]


def main():
    session = PromptSession(
        completer=InlineCompleter(commands),
        complete_in_thread=True,  # 支持异步补全
        complete_while_typing=True,  # 输入时自动触发补全
        style=style,
        vi_mode=False,  # 禁用 vi 模式
        mouse_support=False
    )

    print("Welcome to MyREPL! (type 'exit' to quit)")
    while True:
        try:
            text = session.prompt(">>> ")
            if text.strip() == "exit":
                break
            # 这里可以添加命令处理逻辑
            print(f"Processing command: {text}")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break


if __name__ == "__main__":
    main()