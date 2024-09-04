import os


def merge_files(web_file, css_file=None, script_file=None):
    if css_file:
        css = read_file(css_file)
    if script_file:
        script = read_file(script_file)
    html_file = []
    with open(web_file, "r") as f:
        for line in f.readlines():
            html_file.append(line)
            if line.find("</head>") != -1 and css_file:
                html_file = add_css(html_file, css)
                html_file = add_script(html_file, script)
    return html_file


def add_css(html_file, css):
    html_file.append("<style>")
    for line in css:
        html_file.append(line)
    html_file.append("/<style>")
    return html_file


def add_script(html_file, script):
    html_file.append("<script>")
    for line in script:
        html_file.append(line)
    html_file.append("</script>")
    return html_file


def read_file(file):
    data = []
    try:
        with open(file, "r") as f:
            for line in f.readlines():
                if line.strip() == "":
                    continue
                line = line.strip().replace('"', "'")
                data.append(line)
    except FileNotFoundError:
        print(f"Could not find: {file}")
    return data


def convert(web_file, css_file=None, script_file=None):
    _, file_name = os.path.split(web_file)
    function_name = file_name.split(".")[0]
    html_file = merge_files(web_file, css_file, script_file)
    result = []
    result.append(f"void {function_name}(WiFiClient client){{\n")
    for line in html_file:
        line = line = line.strip().replace('"', "'")
        if line == "":
            continue
        result.append(f"\tclient.println(\"{line.strip()}\");\n")
    result.append("}")
    with open(f"converted_{function_name}.txt", "w") as f:
        for line in result:
            f.write(line)

    print(f"Conversion saved on converted_{function_name}.txt")


if __name__ == "__main__":
    convert("game.html", "game.css", "game.js")
