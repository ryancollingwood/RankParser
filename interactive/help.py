commands = {
    "+": ("Add an item: +<Item>", "+Ryan",),
    "-": ("Remove an item: - <Item>", "-Ryan"),
    "=": ("Solve and display results", "="),
    "~": ("Suggest a pair for constraint specification.", "~"),
    "?": ("Debug the input, displaying how it will be tokenised: ? <statement>", "? Breakfast before Dinner"),
    "history": ("Display the history of submitted statements", "history"),
    "undo": ("Remove the most recent submitted statement", "undo"),
    "import_items": ("Import items from a text file. "
                     "Each item must appear on it's own line in the text file: "
                     "import_items <filename>",
                     "import_items exported_tasks.txt"
                     ),
    "load": ("Load a previous session: load <session_name>", "load programmer_riddle"),
    "graph": ("Generate a Graphviz diagram of the current solution: graph <filename>", "graph result.dot"),
}