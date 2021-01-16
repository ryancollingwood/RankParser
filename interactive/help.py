commands = {
    "+": ("Add an item: +<Item>", "+Ryan",),
    "-": ("Remove an item: - <Item>", "-Ryan"),
    "=": ("Solve and display results", "="),
    "\\": ("Unlink an item from all other items", "\\ Ryan"),
    "~": ("Suggest a pair of items for constraint specification.", "~"),
    "?": ("Debug the input, displaying how it will be tokenised: ? <statement>", "? Breakfast before Dinner"),
    "history": ("Display the history of submitted statements", "history"),
    "undo": ("Remove the most recent submitted statement", "undo"),
    "load": ("Load a previous session: load <session_name>", "load programmer_riddle"),
    "copy": ("Copy the current session and change to it: copy <session>", "copy programmer_riddle_backup"),
    "export_items": ("Export items to a text file. Can be used in import_items: "
                     "export_items <filename>",
                     "export_items exported_items"
                     ),
    "import_items": ("Import items from a text file. "
                     "Each item must appear on it's own line in the text file: "
                     "import_items <filename>",
                     "import_items exported_tasks.txt"
                     ),
    "graph": ("Generate a Graphviz diagram of the current solution: graph <filename>", "graph result.dot"),
    "csv": ("Export the edges (start, end) with the weight: csv <filename>", "csv edges.csv"),
    "stats": ("Export graph stats (e.g. page rank) of the solution with the most support: stats <filename>", "stats graphstats"),
}
