class Ansi:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @classmethod
    def disable(cls) -> None:
        cls.HEADER = ''
        cls.BLUE = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.RED = ''
        cls.BOLD = ''
        cls.UNDERLINE = ''
        cls.END = ''

    @staticmethod
    def blend(color: str, text: str) -> str:
        """
        blend text with ansi color.

        example: Ansi.blend(Ansi.GREEN, 'Hello World!')
        :param color: Ansi color, see implementation for more details
        :param text: text need to be colored
        :return: string with ansi information
        """
        return Ansi.apply([color], text)

    @staticmethod
    def apply(styles: list[str], text: str) -> str:
        """
        blend text with a list of ansi colors.

        example: Ansi.list_blend([Ansi.GREEN, Ansi.UNDERLINE], 'Hello World!')
        :param styles: Ansi styles, see implementation for more details
        :param text: text need to be colored
        :return: string with ansi information
        """
        return f"{''.join(styles)}{text}{Ansi.END}"

    @staticmethod
    def fmt_prefix(styles: list[str], prefix, text: str, padding: str = " ") -> str:
        return f"{Ansi.apply(styles, prefix)}{padding}{text}"
