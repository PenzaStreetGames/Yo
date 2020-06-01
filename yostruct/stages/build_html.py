def build_html(tree, style="pretty"):
    """Преобразование дерева в html-текст"""
    return tree.to_html(style=style)
