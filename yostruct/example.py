html(lang="en"):
    head():
        meta(charset="UTF-8")
        title("Title")
    body():
        h1(): "Header"
        p(): "Paragraph example"
        p():
            "Insert ", "(style="i")italic text", "into paragraph"
        table():
            thead(): "Someone table"
            tr():
                td(): 1
                td(): 2
                td(): 3
            tr():
                td(): 4
                td(): 5
                td(): 6
        q(): "Small idea"
        blockquote(): "Idea"